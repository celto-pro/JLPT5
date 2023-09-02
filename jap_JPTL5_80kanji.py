import json
import numpy as np

import jap_data
import global_functions




# SOMMAIRE

## json creations from JLPT5 - Kanjis

## json file modification


## Get information about our knowledge


    #####  TO CODE #####


## Show scores / level (on specific range of the vocabulary list)


    #####  TO CODE #####



## Train with the JLPT5's 80 Kanji
    ### Check parameters
    ### Questions and correction presentation
    ### specific_kanjis_JLPT5() trains in one translation direction
    ### kanjis_training_JLPT5() trains in both translation direction

## JLPT5 Kanjis evaluation: JLPT5_kanji(size, direction)
    ### This function returns the list of the mistakes and the success rate




'''
JLPT5_kanji_json_creation's input are the path to two json's file:
- first one has key that are kanji and values that are translation
- second one has key that are french+on/kun-yumi and values are kanji

This function initializes all scores and level respectivly to 0 and 1.
'''

## json creations from JLPT5 - Kanjis
def JLPT5_kanji_json_creation(path_1, path_2):
    # Get data from external file
    kanji_jap, kanji_fr = jap_data.JLPT5_kanji_jap, jap_data.JLPT5_kanji_fr

    # data preparation (jap -> fr)
    data_jap_to_fr = {}
    for i, element in enumerate(kanji_jap):
        data_jap_to_fr[element] = [0, 1, kanji_fr[i]]
    
    # data preparation (fr -> jap)
    data_fr_to_jap = {}
    for i, element in enumerate(kanji_fr):
        data_fr_to_jap[element] = [0, 1, kanji_jap[i]]

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
- ??
'''
### Example: "global_functions.jap_JLPT_update_value('JLPT5_jap_kanji.json', key, value)"  ###










## S'entraîner avec les 80 kanjis du JLPT5

'''
There are two different training functions for the JLPT5 80's kanjis
kanjis_training_JLPT5 which is similar to exam's one => Ask training_size*10 questions in both translation sens
"specific_kanjis_training_JLPT5" which is the same as "kanjis_training_JLPT5" but with only one translation direction
'''


'''
specific_kanjis_training_JLPT5 depends on several functions:
- check_parameters_JPTL5_kanji that can raise ValueError
- JLPT5_kanjis_questions_presentation and JLPT5_kanjis_correction_presentation for presentation
- global_functions.JLPT_questions_selection that selects the questions (weighted or not)
'''

def check_parameters_JPTL5_kanji(training_size, difficulty, direction, weight):
    '''
    This function helps the main function to be shorter and check all parameter values
    '''
    if (difficulty != 'max') and (difficulty not in list(range(1, 11))):
        raise ValueError('difficulty parameter has to be a number between 1 and 10 or "max"')
    if (training_size != 'max') and (training_size not in list(range(1, 11))):
        raise ValueError('training_size parameter has to be a number between 1 and 10 or "max"')
    if direction not in [0, 1, 'jap => fr', 'fr => jap']:
        raise ValueError('direction parameter has to be 0 (jap => fr) or 1 (fr => jap)')
    if weight not in [0, 'off', 1, 'on']:
        raise ValueError('"weight" parameter has to be 0, 1 or "off" or "on".')
    if (weight in [1, "on"]) and (difficulty != 'max'):
        raise ValueError('You can only turn weights "on" if difficulty="max"')
    ## In order not to have several time the same question, we need training_size > difficulty
    error = 'training_size input value has to be higher than difficulty input value'
    if (training_size == 'max') and (difficulty != 'max'):
        raise ValueError(error)
    elif (training_size in range(1, 11)) and (difficulty in range(1, 11)):
        if training_size > difficulty:
            raise ValueError(error)
    
    return None


def JLPT5_kanjis_questions_presentation(data_test, direction):
    # Create guidlines titles for questions
    guidlines = ['Kanji to kun/on yumi + fr',
                'kun/on yumi + fr to kanji']
    
    # Classical presentation
    if direction in [0, 'jap => fr']:
        print('\nKanji\'s exercise: ' + guidlines[0] + '.\n')
    else:
        print('\nKanji\'s exercise: ' + guidlines[1] + '.\n')

    # Print question tests (with jumps every ten questions)
    jump = 0
    for key in data_test.keys():
        if jump %10 == 0:
            print(f'\n Questions {jump+1} to {jump + 10}:\n')
        print(key)
        jump += 1
    
    return None


def JLPT5_kanjis_correction_presentation(data_test, direction):
    # Presentation
    print('\nCorrection time.\n')
    input('Press any key to see the correction')

    # Create guidlines titles for corrections
    translation_guidlines = ['Kanji\'s to French',
                             'French\'s to Kanji']
    
    # Classical presentation
    if direction in [0, 'jap => fr']:
        print('\n' + translation_guidlines[0] + ':\n')
    else:
        print('\n' + translation_guidlines[1] + ':\n')
    
    # Print corrections (with jumps every ten answers)
    jump = 0
    for key, value in data_test.items():
        if jump %10 == 0:
            print(f'\n Answers {jump+1} to {jump + 10}:\n')
        print(f'{key} => {value[2]}')
        jump += 1

    return None




    ### Specific_kanjis_training_JLPT5() trains in one translation direction
def specific_kanjis_JLPT5(training_size=3, difficulty='max', direction=0, weight='off'):
    '''
    "10*training_size" represents the number of questions
    "difficulty" represents the number of different kanjis that can be chosen (times 10)
    its value is between 1 and 10 ('max' and 10 are the same)
    "direction": 0 means "jap => fr"; 1 means "fr => jap"
    "weight" is 0 (or "off") if we don't take in consideration the scores values else 1 (or "on")

    data_test format: {question: [score, level, answer] for question in selected_questions}
    '''
    
    # Check input parameters (6 cases)
    check_parameters_JPTL5_kanji(training_size, difficulty, direction, weight)

    # Get kanjis' data
    try:
        if direction in [0, 'jap => fr']:
            with open('JLPT5_jap_kanji.json', 'r') as file:
                data = json.load(file)
        else:
            with open('JLPT5_fr_kanji.json', 'r') as file:
                data = json.load(file)
    except IOError as e:
        print(f'{e}: impossible to open the file')

    # kanjis' selection (weighted or not depending on weight input value)
    data_test = global_functions.JLPT_questions_selection(training_size, difficulty, data, weight)

    # (kanjis => on/kun yumi) questions' presentation
    JLPT5_kanjis_questions_presentation(data_test, direction)

    # correction
    JLPT5_kanjis_correction_presentation(data_test, direction)

    return data_test









    ### kanjis_training_JLPT5() trains in both translation direction
def kanjis_training_JLPT5(training_size=3, difficulty='max', weight="off"):
    '''
    "training_size"*10 represents the number of questions
    "difficulty": is a number between 1 and ?? which represents
    the (number of kanjis)*10 in which we are sampling.
    "weights" can be 0 (or "off") or 1 (or "on").
    '''
    # First training: from Kanji to French
    data_test = specific_kanjis_JLPT5(training_size, difficulty, direction=0, weight=weight)
    
    # Second training: from French to Kanji
    data_test = specific_kanjis_JLPT5(training_size, difficulty, direction=1, weight=weight)








## JLPT5 Kanjis

'''
Here is the evaluation function.
We need to call it for both side of translation changing direction from 0 to 1.
'''

def JLPT5_kanji(size, direction):
    '''
    "size" will determine how long is the test.
    There are 10*size number of questions for each exercises.

    CARE: this function does only one direction, need to call it again for other direction translation
    '''
    # Get selected data. If direction == 0: from Japanese to French else from French to Japanese
    data = specific_kanjis_JLPT5(training_size=size, difficulty='max', direction=direction, weight=1)

    # Get potential mistakes
    number_mistakes, list_mistakes = global_functions.get_mistakes()
    
    # Add 'S' for success and 'F' for fail to all test we did: [[question_1, 'F'], [question_2, 'S'], ...]
    SF_list = global_functions.success_fail_list(data, list_mistakes)

    # Update scores & level + update json's file
    path = 'JLPT5_jap_kanji.json' if direction in [0, 'jap => fr'] else 'JLPT5_fr_kanji.json'
    global_functions.update_scores(path, SF_list)

    # Return the mistakes list and the success rate (among 0 and 1)
    return list_mistakes, np.round(100*(10*size - number_mistakes)/(10*size), 1)