class ExperimentMessages:
    def __init__(self, language):
        filepath =  f'languages/{language}/ExpMessages.txt'
        with open(filepath, mode='r', encoding='ISO-8859-1') as f:
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
