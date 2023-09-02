# Importations
import json
import numpy as np

import jap_data
import global_functions




# SOMMAIRE


# 1] json manipulation

    ## json creation from JLPT5 - vocabulary

    ## json file modification (from global_functions)

    ## json auto-update (inside each fonction that call vocabulary) (from global_functions)



# 2] Information representation


    ## Get information about our knowledge (from global_functions)

    ## Show scores / level (from global_functions)



# 3] Training


    ## Train with the JLPT5's vocabulary
        ### Check parameters
        ### Questions and correction presentation
        ### Specific_vocabulary_JLPT5() trains in one translation direction
        ### vocabulary_training_JLPT5() trains in both translation direction

    ## Train on worst score words



# 4] Evaluation

    ## JLPT5 vocabulary evaluation: JLPT5_vocabulary(size, direction)


            ##### TO CODE #####


        ### This function returns the list of the mistakes and the success rate


            ##### TO CODE #####




# TO-DO LIST
'''
- Place auto-update in every functions that call the json's file wisely (not twice for a function)
- Code evaluation function
- Save evaluation results
- Plot evaluation scores/difficulty evolution
- Finish "get_score_info()"
'''




## json creation from JLPT5 - vocabulary
'''
JLPT5_vocabulary_json_creation()'s input are the path to two new json's file:
- first one has key that are kanji and values are on/kun-yumi + french translation
- second one has key that are on/kun-yumi + french and values are kanji

This function initializes all scores and level respectivly to 0 and 1.
'''

## json creations from JLPT5 - Kanjis
def JLPT5_vocabulary_json_creation(path_1, path_2):
    # Get data from external file
    vocabulary_jap, vocabulary_fr = jap_data.JLPT5_voc_jap, jap_data.JLPT5_voc_fr

    # data preparation (jap -> fr)
    data_jap_to_fr = {}
    for i, element in enumerate(vocabulary_jap):
        data_jap_to_fr[element] = [0, 1, vocabulary_fr[i]]
    
    # data preparation (fr -> jap)
    data_fr_to_jap = {}
    for i, element in enumerate(vocabulary_fr):
        data_fr_to_jap[element] = [0, 1, vocabulary_jap[i]]

    # json creation
    with open(path_1, 'w') as file:
        json.dump(data_jap_to_fr, file, indent=4)
    
    with open(path_2, 'w') as file:
        json.dump(data_fr_to_jap, file, indent=4)

    return None





## json's file modification.
'''
To modify a value => "global_functions.jap_JLPT_update_value(path, key, value)"
This function accesses the key and change the value to the one given as input

To modify a key => "global_functions.jap_JLPT_update_key(path, key, new_key)"
This function keeps a value and modify a key to the new_key input parameter.

Possible paths:
- 'jap_alphabet.json'
- 'JLPT5_jap_kanji.json' & 'JLPT5_fr_kanji.json'
- 'JLPT5_jap_vocabulary.json' & 'JLPT5_fr_vocabulary.json'
'''
### Example: "global_functions.jap_JLPT_update_value('JLPT5_jap_kanji.json', key, value)"  ###







## json auto-update (inside each fonction that call vocabulary)
'''
"json_auto_update(path, list_name, list_translation)" is in global_functions module

This function is used when we are building our vocabulary/kanjis.
It can be used if you want to add specific words in your learning_list.
It takes three parameters:
- "path": represents the path of the json file to update
- "list_name": represents the actual list name used to update our file
- "list_translation": represents the list translations of "list_name"
'''
### Example: # global_functions.json_auto_update('JLPT5_jap_vocabulary.json', 'JLPT5_fr_vocabulary.json', jap_data.JLPT5_voc_jap, jap_data.JLPT5_voc_fr) ###





## Get information about our knowledge
'''
To get information about our knowledge we call the global function:
        "global_functions.get_knowledge_info(path, 20)"
- "path" can be "JLPT5_jap_vocabulary.json" or "JLPT5_fr_vocabulary.json"
- "lowest_scores_size" reprensents the number of lowest scores words we want to get

This functions returns a list that contains:
- [0]: The mean score
- [1]: The mean level
- [2]: The list of the "lowest_scores_size" lowest scores
- [3]: The number of words for each level: {1: x1, 2: x2, ..., 4: x4}
'''
### Example: global_functions.get_knowledge_info('JLPT5_jap_vocabulary.json', 20)




## Show scores / level
'''
There are also a global functions for this.
- show_level(path, title='Bar presentation')
    => it plots the levels with a bar plot
- show_score(path, title='Bar presentation', specific_range='max', max_value=25)
    => it plots the scores (limited by max_value) that can be on a specific range like [100, 200] with a bar plot too
'''
# Example: global_functions.show_score('JLPT5_fr_vocabulary.json', 'Score presentation')







## Train with the JLPT5's vocabulary


    ### Check parameters
    
def check_parameters_JLPT5_vocabulary(size, difficulty, direction, weight, training_position):
    # Compute vocabulary total size
    with open('JLPT5_fr_vocabulary.json', 'r') as file:
        data = json.load(file)
    vocabulary_size = len(data)

    # Check difficulty (that has to be lower than vocabulary_size)
    if difficulty != 'max':
        if 10*difficulty > vocabulary_size:
            raise ValueError('"difficulty" has to be an integer lower or equal to {} or "max".'.format(vocabulary_size//10))
    
    # Check size (that has to be lower or equal to difficulty)
    if size != 'max':
        if difficulty != 'max':
            if size > difficulty:
                raise ValueError('"size" has to be lower or equal to "difficutly"')
        else:
            if 10*size > vocabulary_size:
                raise ValueError('"size" has to be an integer lower or equal to {} or "max"'.format(vocabulary_size//10))
    else:
        # If size == 'max', we limit it to difficulty.
        size = difficulty
        print('"size" has been limited to difficulty.')
    
    # Check direction
    if direction not in [0, 1, 'jap => fr', 'fr => jap']:
        raise ValueError('"direction" has to be 0, "jap => fr",  1 or "fr => jap".')

    # Check weight
    if (weight in [1, "on"]) and (difficulty != 'max'):
        raise ValueError('You can only turn weights "on" (1) if difficulty="max"')

    # Training_position is None by default but it can be a list to focus
    # on specific range of the vocabulary list: "training_position=[36, 247]"
    if training_position != None:
        if type(training_position) != list:
            raise ValueError('If "training_position" isn\'t None, then it has to be a list of 2 elements.')
        elif len(training_position) != 2:
            raise ValueError('"training_position" is None or a list of two elements.')
        # If training_position is a list of two elements
        else:
            if (type(training_position[0]) != int) or (type(training_position[1]) != int):
                raise ValueError('"training_position" values has to be integer.')
            elif difficulty != 'max': 
                if (training_position[0] < 1) or (training_position[1] > 10*difficulty):
                    raise ValueError('"training_position" values have to be among 1 and 10 * difficutly: {}'.format(10*difficulty))
            else:
                if (training_position[0] < 1) or (training_position[1] > vocabulary_size):
                    raise ValueError('"training_position" values have to be between 1 and vocabulary_size: {}'.format(vocabulary_size))
    
    return size






    ### Questions and correction presentation


def JLPT5_vocabulary_questions_presentation(data_test, direction):
    # Create guidlines titles for questions
    guidlines = ['Kanji\'s vocabulary to kun/on yumi + french',
                'kun/on yumi + french to kanji\'s vocabulary']
    
    # Classical presentation
    if direction in [0, 'jap => fr']:
        print('\nVocabulary\'s exercise: ' + guidlines[0] + '.\n')
    else:
        print('\nVocabulary\'s exercise: ' + guidlines[1] + '.\n')

    # Print question tests (with jumps every ten questions)
    jump = 0
    for key in data_test.keys():
        if jump %10 == 0:
            print(f'\n Questions {jump+1} to {jump + 10}:\n')
        print(key)
        jump += 1
    
    return None



def JLPT5_vocabulary_correction_presentation(data_test, direction):
    '''
    We can decide to show only the correction or the correction + score
    by comment/uncomment the end of the function (read the comments)
    '''

    # Presentation
    print('\nCorrection time.\n')
    input('Press any key to see the correction')

    # Create guidlines titles for corrections
    translation_guidlines = ['Japanese\'s to French',
                             'French\'s to Japanese']
    
    # Classical presentation
    if direction in [0, 'jap => fr']:
        print('\n' + translation_guidlines[0] + ':\n')
    else:
        print('\n' + translation_guidlines[1] + ':\n')
    
    # Print corrections (with jumps every ten answers)
    jump = 0
    returned_corrections = []
    for key, value in data_test.items():
        if jump %10 == 0:
            print(f'\n Answers {jump+1} to {jump + 10}:\n')
        # Showing only the traduction
        # print(f'{key} => {value[2]}')

        # Showing the traduction + score
        print(f'{key} => {value}')
        returned_corrections.append([key, value])
        jump += 1

    return returned_corrections





    ### Specific_vocabulary_JLPT5() trains in one translation direction
    
def specific_vocabulary_JLPT5(training_size=3, difficulty='max', direction=0, weight='off', training_position=None):
    '''
    10*"training_size" represents the number of questions asked. It can be an integer or 'max'.
    "difficulty" reprensents the size of the questions' pool. It can be an integer or 'max'.
    "direction": 0 means "jap => fr"; 1 means "fr => jap"
    "weight":
        - "on" or 1: takes in consideration knowledge to ask unknown kanji
        - "off" or 0: takes uniformly random questions
    "training_position" is a list that targets a range of specific kanjis
    
    Remark: "difficulty" has to be higher than max("training_position")

    The function returns data_test, ready for use. Here is the returned value format:
    {question: [score, level, answer] for question in selected_questions}
    '''

    # Check input parameters (6 cases)
    try:
        training_size = check_parameters_JLPT5_vocabulary(training_size, difficulty, direction, weight, training_position)
    except ValueError as e:
        print(f'{e}: parameters\' error.')

    # Get vocabulary's data
    try:
        if direction in [0, 'jap => fr']:
            with open('JLPT5_jap_vocabulary.json', 'r') as file:
                data = json.load(file)
        else:
            with open('JLPT5_fr_vocabulary.json', 'r') as file:
                data = json.load(file)
    except IOError as e:
        print(f'{e}: impossible to open the file')

    # Data limitation if training_position is a list
    if training_position != None:
        data = {key: data[key] for i, key in enumerate(list(data.keys())) if i in range(training_position[0], training_position[1] + 1)}

    # kanjis' selection (weighted or not depending on weight input value)
    data_test = global_functions.JLPT_questions_selection(training_size, difficulty, data, weight)

    # Japanese vocabulary => on/kun yumi + french questions' presentation
    JLPT5_vocabulary_questions_presentation(data_test, direction)

    # Correction
    JLPT5_vocabulary_correction_presentation(data_test, direction)

    return None







    ### vocabulary_training_JLPT5() trains in both translation direction

def vocabulary_training_JLPT5(training_size=3, difficulty='max', weight='off', training_position=None):
    '''
        "training_size"*10 represents the number of questions
        "difficulty": is a number between 1 and ?? which represents
        the (number of kanjis)*10 in which we are sampling.
        "weights" can be 0 (or "off") or 1 (or "on").
    '''
    # First training: from Japanese to French
    specific_vocabulary_JLPT5(training_size, difficulty, direction=0, weight=weight, training_position=training_position)

    # Second training: from French to Japanese
    specific_vocabulary_JLPT5(training_size, difficulty, direction=1, weight=weight, training_position=training_position)
    
    return None





## Train on worst score words
'''
This function is just a combination of previous functions.
- "path" is naturally the path to the json's file we want to train with
- "direction" can be [0, "jap => fr", 1, "fr => jap"]
- "size" is the number of element we want to train on.
'''
def worst_score_words_training(path, direction, size):
    # Get the worst score words
    data = global_functions.get_knowledge_info(path, size)[4]

    # Questions' presentation
    JLPT5_vocabulary_questions_presentation(data, direction)

    # Correction
    JLPT5_vocabulary_correction_presentation(data, direction)























## JLPT5 vocabulary evaluation: JLPT5_vocabulary(size, direction)

def resume_preparation(list_mistakes, corrections):
    '''
    Instead of looking for correction in the end, resume_preparation catches the
    mistakes in list_mistakes and get the correction we prepared for the exercise.
    Return a list. Each element of this list is a list of two elements:
    - the mistake
    - its correction
    '''
    final_errors_resume = []
    for element in corrections:
        if element[0] in list_mistakes:
            final_errors_resume.append(element)

    return final_errors_resume




def JLPT5_vocabulary(size, direction):   
    '''
    "size" will determine how long is the test.
    There are 10*size number of questions for each exercises.

    CARE: this function does only one direction, need to call it again for the other direction translation
    '''
    # Auto-update (if necessary)
    global_functions.json_auto_update('JLPT5_jap_vocabulary.json', 'JLPT5_fr_vocabulary.json', jap_data.JLPT5_voc_jap, jap_data.JLPT5_voc_fr)

    # Get vocabulary's data
    try:
        if direction in [0, 'jap => fr']:
            with open('JLPT5_jap_vocabulary.json', 'r') as file:
                data = json.load(file)
        else:
            with open('JLPT5_fr_vocabulary.json', 'r') as file:
                data = json.load(file)
    except IOError as e:
        print(f'{e}: impossible to open the file')
    
    # Select data for the test
    data = global_functions.JLPT_questions_selection(size, difficulty='max', data=data, weight="on")

    # Questions' presentation
    JLPT5_vocabulary_questions_presentation(data, direction)

    # Correction' presentation
    returned_corrections = JLPT5_vocabulary_correction_presentation(data, direction)

    # Get potential mistakes
    number_mistakes, list_mistakes = global_functions.get_mistakes()
    
    # Add 'S' for success and 'F' for fail to all test we did: [[question_1, 'F'], [question_2, 'S'], ...]
    SF_list = global_functions.success_fail_list(data, list_mistakes)

    # Update scores & level + update json's file
    path = 'JLPT5_jap_vocabulary.json' if direction in [0, 'jap => fr'] else 'JLPT5_fr_vocabulary.json'
    global_functions.update_scores(path, SF_list)
    
    # Preparation for final errors presentation
    final_errors_resume = resume_preparation(list_mistakes, returned_corrections)

    # Return the mistakes list and the success rate (among 0 and 1)
    return list_mistakes, np.round(100*(10*size - number_mistakes)/(10*size), 1), final_errors_resume