from itertools import product, permutations
import os
import random

import numpy as np
import pandas as pd

from psychopy.visual import Rect, Polygon
from psychopy.event import Mouse

from tasks.generic_task import GenericTask, GenericTrial
from tasks.spatial_short_term_memory_scorer import SpatialShortTermMemoryScorer

class SpatialShortTermMemoryGrid:
    def __init__(self, window, n_rows, n_cols, cell_height, cell_width):
        self.window = window
        self.n_rows = n_rows
        self.n_cols = n_cols

        self.init_cells(window, n_cols, n_rows, cell_height, cell_width)

    def init_cells(self, window, n_cols, n_rows, cell_height, cell_width):
        self.cells = [[0 for _ in range(self.n_cols)]
                      for _ in range(self.n_rows)]
        
        grid_height = cell_height * self.n_rows
        grid_width = cell_width * self.n_cols

        top_row = grid_height / 2 - cell_height / 2
        left_col = -grid_width / 2 - cell_width / 2

        self.position_map = {
            (row, col): (0, 0)
            for col in range(self.n_cols)
            for row in range(self.n_rows)
        }

        for row, col in product(range(self.n_rows), (range(self.n_cols))):
            cell_position = (left_col + (col + 1) * cell_width,
                             top_row - row * cell_height)
            self.position_map[(row, col)] = cell_position

            if window is not None:  # None only for testing
                this_cell = Rect(
                    win=window, name=f'cell_{row}_{col}',
                    width=cell_width,
                    height=cell_height,
                    ori=0, pos=cell_position,
                    lineWidth=1, lineColor='black', lineColorSpace='rgb',
                    fillColor=[1,1,1], fillColorSpace='rgb',
                    opacity=1, depth=-1.0, interpolate=True)
                self.cells[row][col] = this_cell

    def get_grid_positions(self):
        row_col_product = product(range(self.n_rows), range(self.n_cols))
        grid_positions = [(row, col) for row, col in row_col_product]

        return grid_positions

    def get_position_map(self):
        return self.position_map

    def show(self, show=True):
        if self.window is None:  # None only for testing
            return
        
        for row in range(self.n_rows):
            for col in range(self.n_cols):
                self.cells[row][col].setAutoDraw(show)


class SpatialShortTermMemoryTrial(GenericTrial):
    def __init__(self, sequence, grid):
        super().__init__()

        self.sequence = sequence
        self.grid = grid
        self.current_dot = -1
        self.was_pressed = None
        self.init_cell_selection(grid)
        self.init_dot_reserve(grid.window, n_dots=len(sequence)+1)
        self.response_dots = None
        self.response_time = None

    def init_dot_reserve(self, window, n_dots):
        self.dot_reserve = []
        for i in range(n_dots):
            if window is not None:  # None only for Testing
                dot = Polygon(
                    win=window, name=f'selected_dot_{i}',
                    edges=128, size=(0.04, 0.04),
                    ori=0, pos=[0,0],
                    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
                    fillColor='black', fillColorSpace='rgb',
                    opacity=1, depth=-1.0, interpolate=True)
                dot.setAutoDraw(False)
                self.dot_reserve.append(dot)

    def init_cell_selection(self, grid):
        self.cell_selection = {
            (row, col): None
            for col in range(grid.n_cols)
            for row in range(grid.n_rows)
        }

    def get_presentation_count(self):
        return len(self.sequence)

    def get_next_presentation(self):
        assert self.current_dot + 1 < len(self.sequence)
        self.current_dot += 1
        dot_row, dot_col = self.sequence[self.current_dot]
        return self.grid.get_position_map()[(dot_row, dot_col)]

    def get_pressed_coordinates(self, mouse):
        for row, col in self.grid.get_grid_positions():
            if mouse.isPressedIn(shape=self.grid.cells[row][col]):
                return row, col
        return None

    def process_mouse_event(self, mouse):
        is_pressed = any(v != 0 for v in mouse.getPressed())

        if is_pressed and not self.was_pressed:
            self.update_selected_dots(mouse)
            self.was_pressed = True
        elif not is_pressed:
            self.was_pressed = False
            
    def selected_required_count(self):
        return self.get_selected_cell_count() == self.get_presentation_count()
    
    def update_selected_dots(self, mouse):
        grid_coordinates = self.get_pressed_coordinates(mouse)
        if grid_coordinates is None:
            return
        row, col = grid_coordinates

        if not self.is_cell_selected(row, col):
            if self.get_selected_cell_count() < self.get_presentation_count():
                self.select_cell(row, col)
        else:
            self.deselect_cell(row, col)

    def is_cell_selected(self, row, col):
        return self.cell_selection[(row, col)] is not None

    def select_cell(self, row, col):
        dot = self.dot_reserve.pop()
        dot.pos = self.grid.position_map[(row, col)]
        dot.setAutoDraw(True)
        self.cell_selection[(row, col)] = dot

    def deselect_cell(self, row, col):
        dot = self.cell_selection[(row, col)]
        dot.setAutoDraw(False)
        self.dot_reserve.append(dot)
        self.cell_selection[(row, col)] = None

    def get_selected_cells(self):
        return [(row, col) for (row, col), dot in self.cell_selection.items()
                if dot is not None]

    def get_selected_cell_count(self):
        return len(list(filter(None, self.cell_selection.values())))

    def save_response(self, response_time):
        self.response_dots = self.get_selected_cells()
        self.response_time = response_time

    def finish(self):
        dots = list(filter(None, self.cell_selection.values()))
        for dot in dots:
            dot.setAutoDraw(False)
            self.dot_reserve.append(dot)
        for coordinate in self.cell_selection.keys():
            self.cell_selection[coordinate] = None


class SpatialShortTermMemoryTrialFactory:
    def __init__(self, grid, padding):
        self.grid = grid
        grid_positions = self.grid.get_grid_positions()
        self.valid_positions = self.shrink_grid(grid_positions, padding)

    def generate(self, n_dots_list, n_far, n_near):
        trials = []
        for n_dots in n_dots_list:
            for _ in range(n_far):
                sequence = self.generate_far_stimuli(n_dots)
                trial = SpatialShortTermMemoryTrial(sequence, self.grid)
                trials.append(trial)

            for _ in range(n_near):
                sequence = self.generate_near_stimuli(n_dots)
                trial = SpatialShortTermMemoryTrial(sequence, self.grid)
                trials.append(trial)

        assert random.shuffle(trials) is None
        return trials

    def generate_far_stimuli(self, n_dots, min_distance=3):
        '''
        sequence = [None for _ in range(n_dots)]
        sequence[0] = random.choice(self.valid_positions)

        for i in range(1, n_dots):
            for _i in range(1000):
                sequence[i] = random.choice([p for p in self.valid_positions
                                         if p not in sequence])
                dot_distances = self.compute_dot_distances(sequence[:i+1])

                if np.min(dot_distances) <= min_distance:
                    sequence[i] = None
                else:
                    break
        '''

        sequence = [None for _ in range(n_dots)]
        sequence[0] = random.choice(self.valid_positions)

        spot = self.create_spot(sequence[0], min_distance-1, False)
        valid_positions = [p for p in self.valid_positions if p not in spot]

        for _i in range(10000):
            sequence = random.sample(valid_positions, n_dots)
            dot_distances = self.compute_dot_distances(sequence)

            if np.min(dot_distances) >= min_distance:
                break
        return sequence

    def generate_near_stimuli(self, n_dots, max_distance=2):
        '''
        for i in range(1, n_dots):
            for _i in range(1000):
                sequence[i] = random.choice([p for p in self.valid_positions
                                         if p != sequence[i-1]])
                dot_distances = self.compute_dot_distances(sequence[:i+1])

                if np.max(dot_distances) > max_distance:
                    sequence[i] = None
                else:
                    break

            assert sequence[i] is not None, f'{_i} {sequence} {n_dots}'
        '''
        origin_candidates = self.shrink_grid(self.valid_positions,
                                             by=max_distance)
        sequence = [None for _ in range(n_dots)]
        sequence[0] = random.choice(origin_candidates)

        spot = self.create_spot(sequence[0], 2 * max_distance, False)
        for _i in range(10000):
            sequence[1:] = random.sample(spot, n_dots - 1)
            dot_distances = self.compute_dot_distances(sequence)

            if np.max(dot_distances) <= 2 * max_distance:
                break
        return sequence

    def compute_dot_distances(self, dots, drop_diagonal=True):
        n_dots = len(dots)
        distances = [[0 for _ in range(n_dots)] for _ in range(n_dots)]

        for i, j in product(range(n_dots), range(n_dots)):
            dot_i, dot_j = dots[i], dots[j]
            dist_horizontal = abs(dots[i][0] - dots[j][0])
            dist_vertical = abs(dots[i][1] - dots[j][1])
            distances[i][j] = max(dist_horizontal, dist_vertical)

        distances = np.array(distances)
        if drop_diagonal:
            diagonal = np.eye(distances.shape[0], dtype=bool)
            distances = distances[~diagonal].reshape(distances.shape[0], -1)
            
        return distances

    def shrink_grid(self, positions, by):
        cols = [position[0] for position in positions]
        rows = [position[1] for position in positions]

        min_col, max_col = min(cols), max(cols)
        min_row, max_row = min(rows), max(rows)
        
        origin_rows = list(range(min_col + by, max_col - by + 1))
        origin_cols = list(range(min_row + by, max_row - by + 1))

        shrinked_grid = [position for position in product(origin_rows,
                                                          origin_cols)]
        return shrinked_grid

    def create_spot(self, origin, size, include_origin=False):
        origin_row, origin_col = origin
        grid_cols = list(range(origin_col - size // 2,
                               origin_col + size // 2 + 1))
        grid_rows = list(range(origin_row - size // 2,
                               origin_row + size // 2 + 1))

        spot = list(product(grid_rows, grid_cols))
        if not include_origin:
            spot = [p for p in spot if p != origin]
        return spot


class SpatialShortTermMemoryTask(GenericTask):
    def __init__(self, window, seed, experiment_data, config):
        super().__init__()
        random.seed(seed)
        self.name = 'SSTM'
        
        self.config = config

        self.grid = SpatialShortTermMemoryGrid(
            window=window,
            n_rows=config['grid']['n_rows'],
            n_cols=config['grid']['n_cols'],
            cell_height=config['cell']['height'],
            cell_width=config['cell']['width'])

        self.date_format = config['date_format']
        
        self.init_trials(config)
        self.scorer = SpatialShortTermMemoryScorer(self.trials, experiment_data)

    def init_trials(self, config):
        trial_factory = SpatialShortTermMemoryTrialFactory(
            grid=self.grid,
            padding=config['dots']['padding'])

        practice_dot_sequences = config['practice']
        self.practice_trials = [SpatialShortTermMemoryTrial(dot_sequence,
                                                            self.grid)
                                for dot_sequence in practice_dot_sequences]

        self.trials = trial_factory.generate(
            n_dots_list=config['trials']['n_dots_list'],
            n_far=config['trials']['n_far'],
            n_near=config['trials']['n_near'])

    def write_results(self, filepath):
        dirpath = os.path.dirname(filepath)
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)

        self.scorer.compute_scores()

        self.scorer.trial_scores['Score'] = pd.to_numeric(
            self.scorer.trial_scores['Score'], downcast='integer')
        self.scorer.trial_scores['NumDot'] = pd.to_numeric(
            self.scorer.trial_scores['NumDot'], downcast='integer')

        with open(filepath, 'w') as f:
            f.write(f'{self.scorer.date} Spatual Short-Term Memory Task data\n')

        self.scorer.trial_scores.to_csv(filepath, mode='a', sep=' ',
                                        float_format='%.3f')
        
        with open(filepath, 'a') as f:
            f.write('\n')
            f.write('------------------------------------------\n')
            f.write('\n')

        self.scorer.dot_scores.to_csv(filepath, mode='a', sep=' ')

    def write_overall_results(self, filepath):
        dirpath = os.path.dirname(filepath)
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)

        max_possible_score = sum([len(trial.sequence)*2-2
                                  for trial in self.trials])

        with open(filepath, 'a') as f:
            f.write(f'SubID Score Date Time {max_possible_score}\n')
            f.write(f'{self.scorer.subject_id} '
                    f'{self.scorer.trial_scores.Score.sum()} '
                    f'{self.scorer.date.strftime(self.date_format)}\n')
