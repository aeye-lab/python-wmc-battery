from common.config import load_config

class ExperimentMessages:
    def __init__(self, language, encoding,
                 filepath_pattern='languages/{language}/ExpMessages.txt'):

        filepath = filepath_pattern.format(language=language)
        with open(filepath, mode='r', encoding=encoding) as f:
            lines = f.readlines()

        lines = [line.rstrip('\n') for line in lines]

        self.begin_practice = lines[1]
        self.begin_task = lines[2]
        self.continue_trial = lines[3]
        self.experiment_break = lines[4]
        self.task_end = lines[5]
        self.end = lines[7]
        self.draw_dots = lines[10]
        self.next_trial = lines[11]
