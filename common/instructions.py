import yaml

class Instructions:
    def __init__(self, language):

        pathformat = f'languages/{language}/' + '{}'
        filepath = f'languages/{language}/instructions.yaml'

        with open(filepath, 'r') as stream:
            instructions = yaml.safe_load(stream)
        
        for key in instructions.keys():
            instructions[key] = list(map(pathformat.format, instructions[key]))
        self.instructions = instructions

    def get_instructions(self, task):
        return self.instructions[task]

    def get_instruction_page_count(self, task):
        return len(self.instructions[task])
