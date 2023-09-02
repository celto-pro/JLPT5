# IMPORTATIONs
import numpy as np
import json
import os

import jap_data
import global_functions






# SOMMAIRE



# 1] JSON MANIPULATION
    
    ## JSON FILE CREATION
    ## JSON FILE MODIFICATION (GLOBAL_FUNCTIONS)
    ## JSON AUTO-UPDATE (GLOBAL_FUNCTIONS)


# 2] INFORMATION REPRESENTATION

    ## GET INFORMATION ABOUT OUR KNOWLEDGE
    ## SHOW SCORES / LEVELS


# 3] TRAINING

    ## TRAIN WITH THE JLPT5'S SENTENCES
        ### CHECK PARAMETERS
        ### QUESTIONS AND CORRECTIONS PRESENTATIONS
        ### Specific_sentences_JLPT5() TRAINS IN ONE TRANSLATION DIRECTION
        ### sentences_training_JLPT5() TRAINS IN BOTH TRANSLATION DIRECTIONS

    ## TRAIN ON WORST SCORE SENTENCES


# 4] EVALUATION

    ## Prepare the errors resume for the end of the test
    ## Update scores and level from the success/fail list
    ## JLPT5 SENTENCES EVALUATION: JLPT5_sentences(size)













# 1] JSON MANIPULATION
    
    ## JSON FILE CREATION
def JLPT5_sentences_json_creation(path_1, path_2):
    # Get sentences from jap_data
    sentences_jap, sentences_fr = jap_data.JAP_SENTENCES, jap_data.FR_SENTENCES

    # Check size
    if len(sentences_jap) != len(sentences_fr):
        return 'ValueError: number of sentences (jap and fr) doesn\'t match'

    # json preparation
    sentences_jap_to_fr, sentences_fr_to_jap = {}, {}
    for i, element in enumerate(sentences_jap):
        sentences_jap_to_fr[element] = [0, 1, sentences_fr[i]]
    
    for i, element in enumerate(sentences_fr):
        sentences_fr_to_jap[element] = [0, 1, sentences_jap[i]]
    
    # json creation
    if not os.path.exists(path_1):
        with open(path_1, 'w') as file:
            json.dump(sentences_jap_to_fr, file, indent=4)
    
    if not os.path.exists(path_2):
        with open(path_2, 'w') as file:
            json.dump(sentences_fr_to_jap, file, indent=4)

    return None







    ## JSON FILE MODIFICATION (GLOBAL_FUNCTIONS)

'''
To modify a value => "global_functions.jap_JLPT_update_value(path, key, value)"
This function accesses the key and change the value to the one given as input

To modify a key => "global_functions.jap_JLPT_update_key(path, key, new_key)"
This function keeps a value and modify a key to the new_key input parameter.

Possible paths:
- 'jap_alphabet.json'
- 'JLPT5_jap_kanji.json' & 'JLPT5_fr_kanji.json'
- 'JLPT5_jap_vocabulary.json' & 'JLPT5_fr_vocabulary.json'
- 'JLPT_jap_sentences.json' & 'JLPT5_fr_sentences.json'
'''
### Example: "global_functions.jap_JLPT_update_value('JLPT5_jap_sentences.json', '時間の問題だ', '(じかん の mondai da) ce n\'est qu\'une question de temps')"  ###





    ## JSON AUTO-UPDATE (GLOBAL_FUNCTIONS)

'''
"json_auto_update(path, list_name, list_translation)" is in global_functions module

This function is used when we are building our vocabulary/kanjis/sentences.
It can be used if you want to add specific words in your learning_list.
It takes three parameters:
- "path": represents the path of the json file to update
- "list_name": represents the actual list name used to update our file
- "list_translation": represents the list translations of "list_name"
'''
### Example: # global_functions.json_auto_update('JLPT5_jap_sentences.json', 'JLPT5_fr_sentences.json', jap_data.JAP_SENTENCES, jap_data.FR_SENTENCES) ###























# 2] INFORMATION REPRESENTATION

    ## GET INFORMATION ABOUT OUR KNOWLEDGE

'''
To get information about our knowledge we call the global function:
        "global_functions.get_knowledge_info(path, 20)"
- "path" can be "JLPT5_jap_sentences.json" or "JLPT5_fr_sentences.json"
- "lowest_scores_size" reprensents the number of lowest scores words we want to get

This functions returns a list that contains:
- [0]: The mean score
- [1]: The mean level
- [2]: The list of the "lowest_scores_size" lowest scores
- [3]: The number of words for each level: {1: x1, 2: x2, ..., 4: x4}
'''
### Example: global_functions.get_knowledge_info('JLPT5_jap_sentences.json', 20) ###




    ## SHOW SCORES / LEVELS

'''
There are also a global functions for this.
- show_level(path, title='Bar presentation')
    => it plots the levels with a bar plot
- show_score(path, title='Bar presentation', specific_range='max', max_value=25)
    => it plots the scores (limited by max_value) that can be on a specific range like [100, 200] with a bar plot too
'''
### Example: global_functions.show_score('JLPT5_fr_sentences.json', 'Score presentation') ###



















# 3] TRAINING

        ### Check parameters

def check_parameters_JLPT5_sentences(training_size, difficulty, direction, weight, training_position):
    '''
    Remark: "training_size" has to be 'max' or to be lower than "difficulty"
    '''

    # Get vocabulary total size
    path1, path2 = 'JLPT5_jap_sentences.json', 'JLPT5_fr_sentences.json'
    if os.path.exists(path1):
        with open(path1, 'r') as file:
            data = json.load(file)
    vocabulary_size = len(data)

    # Check difficulty: has to be lower than vocabulary_size
    if difficulty != 'max':
        if 10*difficulty > vocabulary_size:
            difficulty = 'max'
            print('Warning: care about "difficulty"\'s value. It has been changed to "max".')
        
    # Check training_size: has to be 'max' or to be lower than vocabulary_size
    if training_size != 'max':
        if difficulty != 'max':
            if training_size > difficulty:
                training_size = 'max'
                print('Warning: care about "training_size"\'s value. It has been changed to "max".')
        else:
            if 10*training_size > vocabulary_size:
                training_size = 'max'
                print('Warning: care about "training_size"\'s value. It has been changed to "max".')
    
    else:
        training_size = difficulty
        print('"training_size" has been limited to "difficulty".')

    # Check direction
    if direction not in [0, 1, 'jap => fr', 'fr => jap']:
        raise ValueError('"direction" has to be an element of [0, "jap => fr", 1, "fr => jap"].')
    
    # Check weight
    if (weight in [1, "on"]) and (difficulty != 'max'):
        raise ValueError('You can only turn weights "on" (1) if difficulty="max"')


    # Training_position is None by default but it can be a list to focus
    # on specific range of the vocabulary list: "training_position=[36, 247]"
    if training_position != None:
        if type(training_position) != list:
            training_position = None
            raise ValueError('If "training_position" isn\'t None, then it has to be a list of 2 elements.')
        elif len(training_position) != 2:
            training_position = None
            raise ValueError('"training_position" is None or a list of two elements.')
        # If training_position is a list of two elements
        else:
            if (type(training_position[0]) != int) or (type(training_position[1]) != int):
                training_position = None
                raise ValueError('"training_position" values has to be integer.')
            elif difficulty != 'max': 
                if (training_position[0] < 1) or (training_position[1] > 10*difficulty):
                    training_position = None
                    raise ValueError('"training_position" values have to be among 1 and 10 * difficutly: {}'.format(10*difficulty))
            else:
                if (training_position[0] < 1) or (training_position[1] > vocabulary_size):
                    training_position = None
                    raise ValueError('"training_position" values have to be between 1 and vocabulary_size: {}'.format(vocabulary_size))

    return training_size, difficulty, training_position








    ### Questions and correction presentation

def JLPT5_sentences_questions_presentation(data_test, direction):
    # Create guidlines titles for questions
    guidlines = ['Japanese\'s sentences to kun/on yumi + french',
                'kun/on yumi + french to kanji\'s sentences']
    
    # Classical presentation
    if direction in [0, 'jap => fr']:
        print('\Sentences\'s exercise: ' + guidlines[0] + '.\n')
    else:
        print('\Sentences\'s exercise: ' + guidlines[1] + '.\n')

    # Print question tests (with jumps every ten questions)
    jump = 0
    for key in data_test.keys():
        if jump %10 == 0:
            print(f'\n Questions {jump+1} to {jump + 10}:\n')
        print(key)
        jump += 1
    
    return None



def JLPT5_sentences_corrections_presentation(data_test, direction):
    '''
    If direction in [0, 'jap => fr'] then we'll also print romanji.
    Else, it's a classical correction presentation
    returns a list of two elements: the key and the traduction
    '''

    # Presentation
    print('\nCorrection time.\n')
    input('Press any key to see the correction.')

    # Create guidlines titles for corrections
    translation_guidlines = ['Japanese\'s to French',
                             'French\'s to Japanese']
    
    # Classical presentation
    if direction in [0, 'jap => fr']:
        print('\n' + translation_guidlines[0] + ':\n')
    else:
        print('\n' + translation_guidlines[1] + ':\n')
    
    # Print corrections (with jumps every ten answers)
    returned_corrections = []
    if direction in [0, 'jap => fr']:
        # Get romanji corrections
        romanji_corrections = [jap_data.ROMANJI_SENTENCES[jap_data.JAP_SENTENCES.index(key)] for key in data_test.keys() if key in data_test.keys()]

        # Print corrections
        jump = 0
        for i, (key, value) in enumerate(data_test.items()):
            if jump%10 == 0:
                print(f'\nAnswers {jump+1} to {jump+10}:\n')
            print(f'{key} => {romanji_corrections[i]}\n{value[2]}\n')
            returned_corrections.append([key, f'({romanji_corrections[i]}) {value}\n'])
            jump += 1
    else:
        jump = 0
        for key, value in data_test.items():
            if jump%10 == 0:
                print(f'\nAnswers {jump+1} to {jump+10}:\n')
            print(f'{key} => {value[2]}')
            returned_corrections.append([key, value])
            jump += 1

    return returned_corrections










    ## Train with the JLPT5's sentences

        ### Specific_sentences_JLPT5() trains in one translation direction

def specific_sentences_JLPT5(training_size=1, difficulty='max', direction=0, weight='off', training_position=None):
    '''
    10*training_size represents the number of questions asked. It can be an integer or 'max'
    'difficulty' represents the size of the questions' pool. It can be an integer or 'max'
    'direction': 0 means 'jap => fr', 1 means 'fr => jap'
    'weight':
        - 'on' or 1: takes in consideration knowledge to ask unkown sentences
        - 'off' or 0: takes uniformly random questions
    'training_position' is a list that targets a range of specific sentences [20, 35]

    remark: '10*difficulty' has to be higher than max('training_position')

    The function returns data_test, ready for use. Here is the returned value format:
    {question: [score, level, answer] for question in selected_questions}
    '''

    # Check input parameters
    try:
        training_size, difficulty, training_position = check_parameters_JLPT5_sentences(training_size, difficulty, direction, weight, training_position)
    except ValueError as e:
        print(f'{e}: paramters\' error.')

    # Get sentences's data
    path1, path2 = 'JLPT_jap_sentences.json', 'JLPT5_fr_sentences.json'
    if os.path.exists(path1) and os.path.exists(path2):
        try:
            if direction in [0, 'jap => fr']:
                with open(path1, 'r') as file:
                    data = json.load(file)
            else:
                with open(path2, 'r') as file:
                    data = json.load(file)
        except IOError as e:
            print(f'{e}: impossible to open the file')
    
    # Data limitation if training_position isn't None
    if training_position != None:
        data = {key: data[key] for i, key in enumerate(list(data.keys())) if i in range(training_position[0], training_position[1] + 1)}

    # Sentences' selection (weighted or not depending on weight input value)
    data_test = global_functions.JLPT_questions_selection(training_size, difficulty, data, weight)

    # Japanese vocabulary => on/kun yumi + french questions' presentation
    JLPT5_sentences_questions_presentation(data_test, direction)

    # Correction
    JLPT5_sentences_corrections_presentation(data_test, direction)

    return None




        ### sentences_training_JLPT5() trains in both translation direction

def sentences_training_JLPT5(training_size=1, difficulty='max', weight='off', training_position=None):
    '''
    "training_size"*10 represents the number of questions
    "difficulty"*10 represents the size of the sentences pool we are sampling on
    "weight" can be 0 or "off" or 1 or "on"
    '''
    # First training: from Japanese to French
    specific_sentences_JLPT5(training_size, difficulty, direction=0, weight=weight, training_position=training_position)

    # Second training: from French to Japanese
    specific_sentences_JLPT5(training_size, difficulty, direction=1, weight=weight, training_position=training_position)

    return None




    ## Train on worst score words

def worst_score_sentences_training(path, direction, size):
    '''
    This function is just a combination of previous functions.
    - "path" is naturally the path to the json's file we want to train with
    - "direction" can be [0, "jap => fr", 1, "fr => jap"]
    - "size" is the number of element we want to train on.
    '''
    # Get the worst score sentences
    data = global_functions.get_knowledge_info(path, size)[4]

    # Questions' presentation
    JLPT5_sentences_questions_presentation(data, direction)

    # Correction
    JLPT5_sentences_corrections_presentation(data, direction)

    return None


















# 4] EVALUATION

    ## Prepare the errors resume for the end of the test

def resume_preparation(list_mistakes, correction_1, correction_2):
    '''
    Instead of looking for correction in the end, resume_preparation catches the
    mistakes in list_mistakes and get the correction we prepared for the exercise.
    Return a list. Each element of this list is a list of two elements:
    - the mistake
    - its correction
    '''
    final_errors_resume = []
    for element in correction_1:
        if element[0] in list_mistakes:
            final_errors_resume.append(element)

    for element in correction_2:
        if element[0] in list_mistakes:
            final_errors_resume.append(element)

    return final_errors_resume



    ## Update scores and level from the success/fail list

def update_sentences_scores(path_1, path_2, key_list):
    '''
    Inputs: - json's file paths to modify
            - list with format [key, 'S'/'F']
    This function updates the scores and lvl
    for all the key given as inputs depending
    on success ('S') or fail ('F')
    '''
    # Get json's data
    with open(path_1, 'r') as file:
        data_jap = json.load(file)

    with open(path_2, 'r') as file:
        data_fr = json.load(file)
    
    # Update scores & levels
    for key in key_list:

        # Check if the user entered a wrong error
        if key[0] not in data_jap.keys() and key[0] not in data_fr.keys():
            print(f'Warning: wrong mistake entered: {key}')

        # If everything is fine,
        else:
            # Get actual score and level for the loop key
            if key[0] in data_jap.keys():
                score, level = data_jap[key[0]][0], data_jap[key[0]][1]
            
            else:
                score, level = data_fr[key[0]][0], data_fr[key[0]][1]

            # If we succeed, it's easy, score gets +1
            if key[1] == 'S':
                score += 1
            
            # Else, depending on our actual level, score decreases more or less
            else:
                if level == 1 :
                    score -= 2
                elif level == 2:
                    score -= 3
                elif level == 3:
                    score -= 5
                else:
                    score -= 20
            
            # Now that score has been updated, we adapt the level to the new score
            if score <= 5:
                level = 1
            elif score < 10:
                level = 2
            elif score < 20:
                level = 3
            else:
                level = 4

            # Update our data
            if key[0] in data_jap.keys():
                data_jap[key[0]] = [score, level, data_jap[key[0]][2]]
            
            else:
                data_fr[key[0]] = [score, level, data_fr[key[0]][2]]
        
    # Save the upadte to the json's file
    with open(path_1, 'w') as file:
        json.dump(data_jap, file, indent=4)
    
    with open(path_2, 'w') as file:
        json.dump(data_fr, file, indent=4)

    return None






    ## JLPT5 sentences evaluation: JLPT5_sentences(size)

def JLPT5_sentences(size):
    '''
    "size" represents the number of questions of this exercise.
    10*"size" in one direction (Jap => Fr) and 10*"size" in the other direction
    return the list of mistakes, the success rate and the corrections of the mistakes made
    '''
    path_1, path_2 = 'JLPT5_jap_sentences.json', 'JLPT5_fr_sentences.json'
    if not os.path.exists(path_1) or not os.path.exists(path_2):
        return 'file does not exists yet, use "JLPT5_sentences_json_creation()" function to create your json file.'
    
    # Auto-update (if necessary)
    global_functions.json_auto_update(path_1, path_2, jap_data.JAP_SENTENCES, jap_data.FR_SENTENCES)

    # Get sentences' data
    try:
        with open(path_1, 'r') as file:
            data_jap = json.load(file)
        
        with open(path_2, 'r') as file:
            data_fr = json.load(file)
        
    except IOError as e:
        print(f'{e}: impossible to open file')
    
    # Select data for the test
    data_jap = global_functions.JLPT_questions_selection(size, difficulty='max', data=data_jap, weight='on')
    data_fr = global_functions.JLPT_questions_selection(size, difficulty='max', data=data_fr, weight='on')

    # Questions' presentation
    JLPT5_sentences_questions_presentation(data_jap, 0)

    # Corrections' presentation
    returned_corrections_1 = JLPT5_sentences_corrections_presentation(data_jap, 0)

    # Questions' presentation
    JLPT5_sentences_questions_presentation(data_fr, 1)

    # Corrections' presentation
    returned_corrections_2 = JLPT5_sentences_corrections_presentation(data_fr, 1)

    # Get potential mistake(s)
    number_mistakes, list_mistakes = global_functions.get_mistakes()

    # Add 'S' for success and 'F' for fail to all test we did: [[question_1, 'F'], ...]
    SF_list = global_functions.success_fail_list(data_jap, list_mistakes)
    SF_list.extend(global_functions.success_fail_list(data_fr, list_mistakes))

    # Update scores & level + update json's file
    update_sentences_scores(path_1, path_2, SF_list)

    # Preparation for final errors presentation
    final_errors_resume = resume_preparation(list_mistakes, returned_corrections_1, returned_corrections_2)

    # Return the mistakes list and the success rate (among 0 and 1)
    return list_mistakes, np.round(100*(20*size - number_mistakes)/(20*size), 1), final_errors_resume