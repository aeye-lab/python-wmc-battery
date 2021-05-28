class Instructions:
    def __init__(self, language):
        self.instructions = {
            'init': [
                f'languages/{language}/instructions/InitInstruct.jpg'
            ],
            'mu': [
                f'languages/{language}/instructions/MUInstruct1.jpg',
                f'languages/{language}/instructions/MUInstruct2.jpg',
                f'languages/{language}/instructions/MUInstruct3.jpg',
            ],
            'os': [
                f'languages/{language}/instructions/OSInstruct1.jpg',
                f'languages/{language}/instructions/OSInstruct2.jpg',
            ],
            'ss': [
                f'languages/{language}/instructions/SSInstruct1.jpg',
                f'languages/{language}/instructions/SSInstruct2.jpg',
            ],
            'sstm': [
                f'languages/{language}/instructions/SSTMInstruct1.jpg',
                f'languages/{language}/instructions/SSTMInstruct2.jpg',
            ],
        }

        if language.startswith('Chinese'):
            self.instructions['mu'] = self.instructions['mu'][:-1]

    def get_instructions(self, task):
        return self.instructions[task]

    def get_instruction_page_count(self, task):
        return len(self.instructions[task])
