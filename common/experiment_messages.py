from dotmap import DotMap
import yaml

class ExperimentMessages(DotMap):
    def __init__(self, language, encoding):
        filepath = f'languages/{language}/experiment_messages.yaml'
        with open(filepath, mode='r', encoding=encoding) as stream:
            super().__init__(yaml.safe_load(stream))
