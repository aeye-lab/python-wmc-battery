mu_default_config = {
    'allowed_keys': [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'num_0', 'num_1', 'num_2', 'num_3', 'num_4',
        'num_5', 'num_6', 'num_7', 'num_8', 'num_9'
    ],
    'frames': {
        'width': 0.25,
        'height': 0.25,
        'locations': {
            2: [(-0.25, 0), (0.25, 0)],
            3: [(-0.4, 0), (0, 0), (0.4, 0)],
            4: [(-0.25, 0.175), (0.25, 0.175), (-0.25, -0.175),
                (0.25, -0.175)],
            5: [(-0.4, 0.175), (0, 0.175), (0.4, 0.175), (-0.25, -0.175),
                (0.25, -0.175)],
            6: [(-0.4, 0.175), (0, 0.175), (0.4, 0.175), (-0.4, -0.175),
                (0, -0.175), (0.4, -0.175)],
        },
    },
    'trials': {
        'set_sizes': [3, 4, 3, 4, 5, 4, 5, 3, 5, 3, 3, 5, 4, 4, 5],
        'n_operations': [3, 4, 6, 5, 5, 3, 2, 2, 3, 5, 4, 4, 6, 2, 6],
    },
    'practice': {
        'set_sizes': [2, 3],
        'n_operations': [4, 3],
    },
    'max_set_size': 6, # this is only relevant for the result file. changing it won't work with the R-script!
}


os_default_config = {
    'alphabet': ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
                 'n', 'p', 'r', 's', 't', 'v', 'w', 'x', 'z'],
    'trials': {
        'n_trials_per_condition': 3,
        'list_lengths': [4, 5, 6, 7, 8],
        'shuffle': True,
    },
    'practice': {
        'n_trials_per_condition': 1,
        'list_lengths': [3, 4, 5],
        'shuffle': False,
    },
    'equations': {
        'operators': ['+', '-'],
        'operand_left_min': 1,
        'operand_left_max': 10,
        'operand_right_min': 1,
        'operand_right_max': 10,
        'valid_result_min': 1,
        'valid_result_max': 20,
    },
    'key_map': {
        False: 'left',
        True: 'right',
    },
    'max_list_length': 8, # this is only relevant for the result frame. changing it won't work with the R-script!
}    
    

ss_default_config = {
    'alphabet': ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
                 'n', 'p', 'r', 's', 't', 'v', 'w', 'x', 'z'],
    'trials': {
        'n_trials_per_condition': 3,
        #'list_lengths': [4, 5, 6, 7, 8],
        'list_lengths': [3, 4, 5, 6],
        'shuffle': True,
    },
    'practice': {
        'n_trials_per_condition': 1,
        'list_lengths': [2, 3, 4],
        #'list_lengths': [3, 4, 5],
        'shuffle': False,
    },
    'key_map': {
        False: 'left',
        True: 'right',
    },
    'max_list_length': 8, # this is only relevant for the result frame. changing it won't work with the R-script!
}


sstm_default_config = {
    'grid': {
        'n_rows': 10,
        'n_cols': 10,
    },
    'cell': {
        'height':  0.075,
        'width': 0.075,
    },
    'dots': {
        'padding': 1,
    },
    'practice': [[(1, 4), (5, 7)], [(3, 3), (0, 1)]],
    'trials': {
        'n_dots_list': range(2, 7),
        'n_far': 3,
        'n_near': 3,
    },
    'date_format': '%Y/%m/%d %H:%M',
}


class WMCConfig:
    def __init__(self, language):
        self.language = language

        self.memory_update = mu_default_config
        self.operation_span = os_default_config
        self.sentence_span = ss_default_config
        self.spatial_short_term_memory = sstm_default_config
