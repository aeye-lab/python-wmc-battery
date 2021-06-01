from dotmap import DotMap
import yaml

def load_config(filepath):
    with open(filepath, 'r') as stream:
        return DotMap(yaml.safe_load(stream))

class WMCConfig:
    def __init__(
            self, language,
            memory_update_config_path='config/memory_update.yaml',
            operation_span_config_path='config/operation_span.yaml',
            sentence_span_config_path='config/sentence_span.yaml',
            spatial_short_term_memory_config_path='config/spatial_short_term_memory.yaml',
            language_config_path_pattern='languages/{language}/config.yaml',
    ):
        self.memory_update = load_config(
            memory_update_config_path)
        self.operation_span = load_config(
            operation_span_config_path)
        self.sentence_span = load_config(
            sentence_span_config_path)
        self.spatial_short_term_memory = load_config(
            spatial_short_term_memory_config_path)

        language_config_path = language_config_path_pattern.format(
            language=language)
        language_config = load_config(language_config_path)

        self.experiment_messages = language_config.experiment_messages
        self.merge_language_config(language_config)

    def merge_language_config(self, language_config):
        pass

