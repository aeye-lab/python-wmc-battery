from dotmap import DotMap
import yaml

def load_config(filepath):
    with open(filepath, 'r') as stream:
        return yaml.safe_load(stream)

class WMCConfig:
    def __init__(
            self, language,
            memory_update_config_path='config/memory_update.yaml',
            operation_span_config_path='config/operation_span.yaml',
            sentence_span_config_path='config/sentence_span.yaml',
            spatial_short_term_memory_config_path='config/spatial_short_term_memory.yaml',
            language_config_path='config/languages.yaml',
    ):
        self.language = language

        self.memory_update = DotMap(load_config(
            memory_update_config_path))
        self.operation_span = DotMap(load_config(
            operation_span_config_path))
        self.sentence_span = DotMap(load_config(
            sentence_span_config_path))
        self.spatial_short_term_memory = DotMap(load_config(
            spatial_short_term_memory_config_path))
