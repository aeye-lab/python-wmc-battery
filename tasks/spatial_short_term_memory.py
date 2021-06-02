from itertools import product, permutations
import os
import random

import numpy as np
import pandas as pd

from psychopy.visual import Rect, Polygon
from psychopy.event import Mouse

from tasks.generic_task import GenericTask, GenericTrial


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
            cell_position = (left_col + col * cell_width,
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
        self.init_dot_reserve(grid.window, n_dots=6)
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


class SpatialShortTermMemoryScorer:
    def __init__(self, trials, experiment_data):
        self.trials = trials
        self.experiment_data = experiment_data
        
        self.init_dot_scores(trials)
        self.init_trial_scores(trials, experiment_data)
        self.date = experiment_data.extraInfo['datetime']
        
    def init_dot_scores(self, trials):
        columns = ['ResRow', 'ResCol',
                   'TrasfResRow', 'TrasfResCol',
                   'AnsRow', 'AnsCol', 'Score']
        index_names = ['InTrial#', 'Dot']
        # index values start with 1
        index_tuples = [(trial_id + 1, dot_id + 1)
                        for trial_id, trial in enumerate(trials)
                        for dot_id in range(len((trial.sequence)))]
        index = pd.MultiIndex.from_tuples(index_tuples,
                                          names=index_names)

        self.dot_scores = pd.DataFrame(index=index,
                                       columns=columns,
                                       data=-1, dtype=int)
        
        dot_scores_ans = [(row, col) for trial in trials
                          for row, col in trial.sequence]
        self.dot_scores['AnsRow'] = [ds[0] for ds in dot_scores_ans]
        self.dot_scores['AnsCol'] = [ds[1] for ds in dot_scores_ans]

    def init_trial_scores(self, trials, experiment_data):
        self.subject_id = experiment_data.extraInfo['Subject ID']
        
        columns = ['Score', 'RT', 'NumDot']
        index_names = ['ID', 'Trial']
        # index values start with 1
        index_tuples = [(self.subject_id, trial_id + 1)
                        for trial_id in range(len((trials)))]
        index = pd.MultiIndex.from_tuples(index_tuples,
                                          names=index_names)

        self.trial_scores = pd.DataFrame(index=index,
                                         columns=columns,
                                         data=-1)
        self.trial_scores['NumDot'] = [len(t.sequence) for t in trials]
        self.trial_scores['RT'] = 0.1

    def compute_trial_scores(self, trial_id):
        trial = self.trials[trial_id]
            
        trial_score = self.trial_scores.loc[self.subject_id, trial_id + 1].copy()
        trial_score.loc['RT'] = trial.response_time
        trial_dot_scores = self.dot_scores.loc[trial_id + 1, :]
        trial_score.loc['Score'] = trial_dot_scores['Score'].sum()
        self.trial_scores.loc[self.subject_id, trial_id + 1] = trial_score


    def compute_dot_scores(self, trial_id):
        def are_neighbours(a, b):
            if abs(a[0] - b[0]) > 1:
                return False
            elif abs(a[1] - b[1]) > 1:
                return False
            else:
                return True

        class ScoreCandidate:
            def __init__(self, correct, response):
                self.correct = correct
                self.response = response

                # offset between first correct dot and first response dot
                offset = tuple(a - b for a, b in zip(correct[0], response[0]))
                self.shifted_response = [
                    tuple(a + b for a, b in zip(response_dot, offset))
                    for response_dot in response
                ]
                self.offset = offset
                
        trial = self.trials[trial_id]
        response_dots = trial.response_dots
        correct_dots = trial.sequence
            
        candidates = []
        for j in range(len(correct_dots)):
            corr_candidate = correct_dots.copy()
            if j > 0: # swap first positions
                corr_candidate[0] = correct_dots[j]
                corr_candidate[j] = correct_dots[0]

            for k in range(len(response_dots)):
                resp_candidate = response_dots.copy()
                if k > 0: # swap first positions
                    resp_candidate[0] = response_dots[k]
                    resp_candidate[k] = response_dots[0]

                for resp_candidate_perm in permutations(resp_candidate[1:]):
                    resp_candidate_perm = ([resp_candidate[0]]
                                           + list(resp_candidate_perm))
                    candidate = ScoreCandidate(corr_candidate,
                                               resp_candidate_perm)
                    candidates.append(candidate)

                    #if candidate.shifted_response[0] == (5,9):
                        #print('#', candidate.shifted_response)
                    #if candidate.shifted_response == [(5,9), (3,9), (9,6), (4,2), (7,9)]:
                    #    #print(candidate.shifted_response)
        
        best_trial_score = -1
        best_dot_score_list = None
        best_candidate = None
        for resp_candidate in candidates:
            shifted_resp = resp_candidate.shifted_response
            #print('§', shifted_resp[0])
            dot_permutations = permutations(correct_dots)
            for corr_dots_perm in dot_permutations:

                # calculate dot scores
                dot_scores = []
                for resp_dot, corr_dot in zip(shifted_resp, corr_dots_perm):
                    if resp_dot == corr_dot:
                        dot_score = 2
                    elif are_neighbours(resp_dot, corr_dot):
                        dot_score = 1
                    else:
                        dot_score = 0
                    dot_scores.append(dot_score)

                #print('%', shifted_resp[0])
                #if shifted_resp[0][0] == 5:
                #print('$', shifted_resp, corr_dots_perm, dot_score)


                # save candidate if best up to now
                trial_score = sum(dot_scores)
                if trial_score > best_trial_score:
                    best_trial_score = trial_score
                    best_dot_score_list = dot_scores
                    resp_candidate.correct = corr_dots_perm
                    best_candidate = resp_candidate

        # we now have found the best candidate with a corresponding permutation
        # now save the information into the dot score data frame
        # remember, trial ids start with 1 for legacy reasons
        self.dot_scores.loc[trial_id + 1, 'Score'] = best_dot_score_list
        
        correct_dots_rows = [dot[0] for dot in best_candidate.correct]
        correct_dots_cols = [dot[1] for dot in best_candidate.correct]
        self.dot_scores.loc[trial_id + 1, 'AnsRow'] = correct_dots_rows
        self.dot_scores.loc[trial_id + 1, 'AnsCol'] = correct_dots_cols

        response_rows = [dot[0] for dot in best_candidate.response]
        response_cols = [dot[1] for dot in best_candidate.response]
        self.dot_scores.loc[trial_id + 1, 'ResRow'] = response_rows
        self.dot_scores.loc[trial_id + 1, 'ResCol'] = response_cols

        shifted_response = best_candidate.shifted_response
        shifted_resp_rows = [dot[0] for dot in shifted_response]
        shifted_resp_cols = [dot[1] for dot in shifted_response]
        self.dot_scores.loc[trial_id + 1, 'TrasfResRow'] = shifted_resp_rows
        self.dot_scores.loc[trial_id + 1, 'TrasfResCol'] = shifted_resp_cols

    def compute_scores(self):
        for trial_id, _ in enumerate(self.trials):
            self.compute_dot_scores(trial_id)
            self.compute_trial_scores(trial_id)
        

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
        self.scorer = SpatialShortTermMemoryScorer(self.trials,
                                                   experiment_data)

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

    def start_new_trial(self):
        super().start_new_trial()
        self.grid.show(True)
        return self.current_trial

    def start_new_practice_trial(self):
        super().start_new_practice_trial()
        self.grid.show(True)
        return self.current_practice_trial

    def finish_trial(self):
        self.grid.show(False)
        super().finish_trial()

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
