# PRESENTATION
'''
This python's file merges the JLPT5 kanjis with the 100 last vocabulary words.
It uses the actual json files.
'''



# Importations
import global_functions

import numpy as np
import json
import os






# SOMMAIRE
# 1] DATA PREPARATION

    ## Merge JLPT5 kanjis and 100 vocabulary words
    ## Choose 10*test_size words between the previous selection, using global_functions


# 2] DATA PRESENTATION

    ## Questions presentation
    ## Answers presentation


# 3] TRAINING PART

    ###############    TO CODE   ###############


# 4] EVALUATION









# 1] JSON MANIPULATIONS

    ## Merge JLPT5 kanjis and 100 vocabulary words
def get_kanji_voc_elements(direction, voc_size=100):
    '''
    To make exercises 2 and 3 harder, this function add 100 vocabulary words to
    the JLPT5 kanji list. The choice of the selected vocabulary words is explain
    in the comments.
    The returned data have the format: [question: [score, level, answer, 'kanji'/'vocabulary']]
    The last element of the list value depends on the file the question is from. 
    '''

    # Get info from json files
    if direction in [0, 'jap => fr']:
        try:
            with open('JLPT5_jap_kanji.json', 'r') as file:
                data_kanji = json.load(file)
            with open('JLPT5_jap_vocabulary.json', 'r') as file:
                data_vocabulary = json.load(file)
        except IOError as e:
            print(f'{e}: impossible to open the file')
        
    elif direction in [1, 'fr => jap']:
        try:
            with open('JLPT5_fr_kanji.json', 'r') as file:
                data_kanji = json.load(file)
            with open('JLPT5_fr_vocabulary.json', 'r') as file:
                data_vocabulary = json.load(file)
        except IOError as e:
            print(f'{e}: impossible to open the file')
    
    # Select 100 specific vocabulary words.
    # If difficulty is between 40 and 50 (between 400 and 500 vocabulary words) => we select words from 300-399
        ## Get difficulty
    evaluation_path = 'JLPT5_evaluation.json'
    try:
        with open(evaluation_path, 'r') as file:
            data_evaluation = json.load(file)
    except IOError as e:
        print(f'{e}: No access to the file {evaluation_path}.')
    
    
        ## To select 300-399, we need an adjusted difficulty
    adjusted_difficulty = (int(data_evaluation['difficulty'][-1]//10)-1)*100


        ## Selection of the vocabulary
    vocabulary_range = list(range(adjusted_difficulty, adjusted_difficulty + voc_size))
    data_vocabulary_selected = {}
    for i, (key, value) in enumerate(data_vocabulary.items()):
        if i in vocabulary_range:
            data_vocabulary_selected[key] = value
    
    # Merge the datas (the {**dict1, **dict2} syntax is a short way to merge dictionaries in Python) 
    data = {**{key: value + ['kanji'] for key, value in data_kanji.items()}, **{key: value + ['vocabulary'] for key, value in data_vocabulary_selected.items()}}

    return data





    ## Choose 10*test_size words between the previous selection, using global_functions
def JLPT5_kanji_and_vocabulary_questions_selection(test_size, direction):
    '''
    DESCRIPTION HERE
    '''
    # Get the data
    data = get_kanji_voc_elements(direction)

    # Select test_size elements from our data
    data_test = global_functions.JLPT_questions_selection(test_size, difficulty=max, data=data, weight='on')

    return data_test








# 2] INFORMATION REPRESENTATION

    ## GET INFORMATION ABOUT OUR KNOWLEDGE

def JLPT5_Exercise23_medium_questions_presentation(data_test, direction):
    # Create guidlines titles for questions
    guidlines = ['Exercise 2, difficulty medium: jap => fr',
                 'Exercise 3, difficulty medium: fr => jap']
    
    # Classical presentation
    if direction in [0, 'jap => fr']:
        print(guidlines[0] + '.\n')
    else:
        print(guidlines[1] + '.\n')

    # Print question tests (with jumps every ten questions)
    jump = 0
    for key in data_test.keys():
        if jump %10 == 0:
            print(f'\n Questions {jump+1} to {jump + 10}:\n')
        print(key)
        jump += 1
    
    return None



def JLPT5_Exercise23_medium_correction_presentation(data_test, direction):
    # Presentation
    print('\nCorrection time.\n')
    input('Press any key to see the correction')

    # Create guidlines titles for corrections
    translation_guidlines = ['Japanese to French',
                             'French to Japanese']
    
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
        print(f'{key} => {value[2]}')
        returned_corrections.append([key, value])
        jump += 1

    return returned_corrections





    ## SHOW SCORES / LEVELS


            ##### TO CODE #####



# 3] TRAINING

    ## Train with the JLPT5's vocabulary


            ##### TO CODE #####



        ### Check parameters


            ##### TO CODE #####



        ### Questions and correction presentation


            ##### TO CODE #####



        ### Specific_vocabulary_JLPT5() trains in one translation direction


            ##### TO CODE #####



        ### vocabulary_training_JLPT5() trains in both translation direction


            ##### TO CODE #####




    ## Train on worst score words


            ##### TO CODE #####




# 4] EVALUATION

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



def JLPT5_Exercice23_evaluation(size, direction):
    '''
    We could add a function that check parameters
    We could also add a new parameter than select the number of vocabulary words
    It's 100 by default, you can change it manually for now inside get_kanji_voc_elements

    This function merge JLPT5_kanjis_data and a number of new vocabulary words to increase
    the difficulty of exercises 2 and 3.  
    '''
    # Get merged data
    data = get_kanji_voc_elements(direction)

    # Select test_size elements from our data using global_functions
    data_test = global_functions.JLPT_questions_selection(size, difficulty='max', data=data, weight='on')
    
    # Questions presentation
    JLPT5_Exercise23_medium_questions_presentation(data_test, direction)

    # Answers
    returned_corrections = JLPT5_Exercise23_medium_correction_presentation(data_test, direction)

    # Get potential mistakes
    number_mistakes, list_mistakes = global_functions.get_mistakes()

    # Add 'S' for success and 'F' for fail to all test we did: [[question_1, 'F'], [question_2, 'S'], ...]
    SF_list = global_functions.success_fail_list(data_test, list_mistakes)

    # Split the SF_list into two list, that depends on if the element comes from kanji or vocabulary
    kanji_SF_list = [element for element in SF_list if data_test[element[0]][-1] == 'kanji']
    vocabulary_SF_list = [element for element in SF_list if data_test[element[0]][-1] == 'vocabulary']

    # Clean the precision 'kanji' or 'vocabulary' since it's not necessary anymore before update our file
    data_test = {key: value[:-1] for key, value in data_test.items()}

    # Update scores & level + update json's file
    kanji_path = 'JLPT5_jap_kanji.json' if direction in [0, 'jap => fr'] else 'JLPT5_fr_kanji.json'
    vocabulary_path = 'JLPT5_jap_vocabulary.json' if direction in [0, 'jap => fr'] else 'JLPT5_fr_vocabulary.json'
    global_functions.update_scores(kanji_path, kanji_SF_list)
    global_functions.update_scores(vocabulary_path, vocabulary_SF_list)

    # Preparation for final errors presentation
    final_errors_resume = resume_preparation(list_mistakes, returned_corrections)

    # Return the mistakes list and the success rate (among 0 and 1)
    return list_mistakes, np.round(100*(10*size - number_mistakes)/(10*size), 1), final_errors_resume