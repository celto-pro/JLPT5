# Importations
import os
import json
import random
import numpy as np
import matplotlib.pyplot as plt





# Global functions

    ## json's file modification
        ### Update value: jap_JLPT_update_value(path, key, value)
        ### update key: jap_JLPT_update_key(path, key, new_key)
    
    ## json auto-update

    ## Questions selection
        ### JLPT weight's function
            ### Returns 1, 2, 3 or 4 with decreasing probability
        ### Adjusting weights/levels + question selection
            ### If lvl 4 is random selected but no word has lvl 4 then
            ### lvl 4 is changed to 3, etc. And lvl 1 to lvl 2 if no lvl 1
            ### Questions selection from adapted weights/levels
        ### data_test returned (it can be weighted or not)
    
    ## Scoring functions
        ### Check mistakes
            ### Returns number_mistakes, list_mistakes
        ### Success/Fail list
            ### This function returns a list in the format:
            ###[[question_1, 'F'], [question_2, 'S'], [question_3, 'S'], ...]
    
    ## Get json's file info (about score/level/evaluation scores)
        ### Get knowledge info
        ### From knowledge info, show some useful statistics

    ## Graphics
        ### Level bar presentation
        ### Score bar presentation
            #### Color selection, necessary for the bar plot
            #### Limits data to a specific range of words
            #### bar plot function. Change the default title if needed.





## json's file modification
'''
This function changes the value of an element
of the jap_alphabet.json file asking the key
and the new value.

Possible paths:
- 'jap_alphabet.json'
- 'JLPT5_jap_kanji.json' & 'JLPT5_fr_kanji.json'
- 'JLPT5_jap_vocabulary.json' & 'JLPT5_fr_vocabulary.json'
- 'JLPT_jap_sentences.json' & 'JLPT5_fr_sentences.json'
'''
### Example: "global_functions.jap_JLPT_update_value('JLPT5_jap_sentences.json', '時間の問題だ', '[XX, YY, (じかん の mondai da) ce n\'est qu\'une question de temps'])"  ###

def jap_JLPT_update_value(path, key, value):
    '''
    This function updates the "value"
    of the "key" given as inputs.
    '''
    # Get data
    if os.path.exists(path):
        with open(path, 'r') as file:
            data = json.load(file)

        # data update
        data[key] = value

        # Saving modification
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)
    
    else:
        return f'{path} does not exists'

    return None



def jap_JLPT_update_key(path, key, new_key):
    '''
    This function updates the key
    (substitutes previous key/value to new_key/value)
    '''
    # Get data
    with open(path, 'r') as file:
        data = json.load(file)
    
    # data update
    data[new_key] = data[key]
    data.pop(key)

    # Saving modification
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

    return None





## json auto-update (inside each fonction that call vocabulary)

def json_auto_update(path, reverse_path, list_name, list_translation):
    '''
    This function checks if an update is needed.
    If so, ask the user if (s)he wants to proceed.

    "path": represents the path of the json file to update
    "list_name": represents the actual list name used to update our file
    "list_translation": represents the list translations of "list_name"
    Use example: "global_functions.json_auto_update('JLPT5_fr_vocabulary.json', 'JLPT5_jap_vocabulary.json', jap_data.JLPT5_voc_fr, jap_data.JLPT5_voc_jap)"
    '''
    # Check list size, it has to be the same => raise an ValueError exception if there are different.
    if len(list_name) != len(list_translation):
        continue_function = input('The dictionaries (French and Japanese) doesn\'t have the same lenght, do you want to continue? Press Y or N: ')
        if continue_function == 'Y':
            return None
        else:
            raise ValueError('The dictionary sizes aren\'t the same. Program stopped!')

    # Access to json's file
    with open(path, 'r') as file:
        data = json.load(file)
    
    # Check if there is a possible update
    update_names = []
    possible_update = 0

    for i, name in enumerate(list_name):
        if name not in data.keys():
            possible_update = 1
            update_names.append([name, i])
    
    # If an update is available, ask the user if he is willing to do it (this prevent update's mistakes)
    if possible_update == 1:
        print('The json\'s file will be updated, adding the following words:')
        for name in update_names:
            print(name[0])
        check = input('Do you want to proceed? Y/N')

        if check == 'Y':
            # Update our data
            for name in update_names:
                data[name[0]] = [0, 1, list_translation[name[1]]]
            
            # Update our data in reverse translation direction
            with open(reverse_path, 'r') as file:
                reverse_data = json.load(file)
            
            for name in update_names:
                reverse_data[list_translation[name[1]]] = [0, 1, name[0]]
        
            # Save the update over the json file
            with open(path, 'w') as file:
                json.dump(data, file, indent=4)

            with open(reverse_path, 'w') as file:
                json.dump(reverse_data, file, indent=4)
    
    return None








## Question selection

    ### JLPT weight's function
'''
    This function returns a number among 1 and 4
    that represents the lvl of an element.
    It's harder to get lvl 4, so lvl 4 are less likely to be returned.

    This function is used as many time as needed (10*training_size)
    to get a list of lvl to be chosen.
'''
def JLPT_weight_function():
    random_number = random.random()
    if random_number < 20/37:
        return 1
    elif random_number < 30/37:
        return 2
    elif random_number < 35/37:
        return 3
    else:
        return 4


    ### Adjusting weights/levels + questions selection
'''
    After the choice of weights, there might be some impossible situation.
    For example, what if 2 level 4 words have to be chosen but no word has
    level 4 yet? Then we need to choose 2 lvl 3 indeed, and if there is not
    enough level 3, then level 2 etc.
    Same goes for lake of level 1 => level 2 => etc.

    Uncomment to understand what is happening.
    data_split are the kanji split by level of knowledge.
'''

def JLPT_weighted_questions(size, data):
    # Select the levels of the questions 
    index = {1: 0, 2: 0, 3: 0, 4: 0}
    for _ in range(10*size):
        index[JLPT_weight_function()] += 1
    
    # print('Index chosen based on level:', index)

    # Adjust the levels chosen
    ## Check actual number of word's level + split data by level
    level = {1: 0, 2: 0, 3: 0, 4: 0}
    data_lvl1, data_lvl2, data_lvl3, data_lvl4 = {}, {}, {}, {}
    data_split = [data_lvl1, data_lvl2, data_lvl3, data_lvl4]

    for key, value in data.items():
        level[value[1]] += 1
        data_split[value[1]-1][key] = value
    
    # print('Actual level of knowledge:', level)
    
    ## Adjust index, so it fits with level
    for i in range(4, 1, -1):
        if index[i] > level[i]:
            index[i-1] += index[i] - level[i]
            index[i] = level[i]
    
    for i in range(1, 4):
        if index[i] > level[i]:
            index[i+1] += index[i] - level[i]
            index[i] = level[i]
    
    # print('Adapted index:', index)

    ## Get the question from data_split based on index
    data_test = {key: data_lvl1[key] for key in np.random.choice(list(data_lvl1.keys()), index[1], replace=False)}
    for i in range(1, 4):
        data_test.update({key: data_split[i][key] for key in np.random.choice(list(data_split[i].keys()), index[i+1], replace=False)})
    
    return {key: data_test[key] for key in random.sample(list(data_test.keys()), len(data_test))}  # ".shuffle" doesn't return a list





def JLPT_questions_selection(training_size, difficulty, data, weight):
    # If weight is "off" we take 10*training_size uniformly random questions
    # taking in consideration the difficulty
    if weight in [0, 'off']:
        if difficulty != 'max':
            data_test = {key: data[key] for key in np.random.choice(list(data.keys())[:10*difficulty], 10*training_size, replace=False)}
        elif training_size != 'max':
            data_test = {key: data[key] for key in np.random.choice(list(data.keys()), 10*training_size, replace=False)}
        else:
            data_test = {key: data[key] for key in np.random.shuffle(list(data.keys()))}
    
    # else, it's not uniform choice
    else:
        data_test = JLPT_weighted_questions(size=training_size, data=data)

    return data_test







## Scoring functions

    ### Check mistakes
def get_mistakes():
    # Ask if there are mistakes
    while True:
        try:
            number_mistakes = int(input('\nHow many mistakes did you make? '))
            break  # If input is valid, break the loop
        except ValueError as e:
            print('\nYou are supposed to enter an integer value: your number of mistakes...')

    list_mistakes = []

    if number_mistakes == 0:
        print('\nPerfect! Great job :)\n')

    # Save mistakes if there is any
    else:
        print('\nWrite down all your mistake(s)\n')
        while len(list_mistakes) < number_mistakes:
            new_mistake = input('Enter your mistake: ')

            # Protection against wrong paste*
            if new_mistake != 'mistake':
                list_mistakes.append(new_mistake)
            else:
                if len(list_mistakes) >= 1:
                    list_mistakes = list_mistakes[:-1]
                else:
                    list_mistakes = []
    
    return number_mistakes, list_mistakes


    ### Success/Fail list
'''
    This function returns a list in the format:
    [[question_1, 'F'], [question_2, 'S'], [question_3, 'S'], ...]

    It is used to upgrade the scores/level
'''
def success_fail_list(data, list_mistakes):
    SF_list = []
    for test in data.keys():
        if test in list_mistakes:
            SF_list.append([test, 'F'])
        else:
            SF_list.append([test, 'S'])
    return SF_list


    ### Update scores and level from the success/fail list
def update_scores(path, key_list):
    '''
    Inputs: - json's file path to modify
            - list with format [key, 'S'/'F']
    This function updates the scores and lvl
    for all the key given as inputs depending
    on success ('S') or fail ('F')
    '''
    # Get json's data
    try:
        with open(path, 'r') as file:
            data = json.load(file)
    except IOError as e:
        print('Impossible to access the file:', e)

    # Update scores & level
    for key in key_list:

        # Check if the user entered a wrong error
        if key[0] not in data.keys():
            print(f'Warning: you entered a wrond mistake: {key[0]}')
        
        # If everything is fine
        else:
            # Get actual score, level of the loop key
            score, level = data[key[0]][0], data[key[0]][1]

            # If we succeed, it's easy, score gets +1
            if key[1] == 'S':
                score += 1
            
            # Else, depending on our actual level, score decreases
            else:
                if level == 1:
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
            data[key[0]] = [score, level, data[key[0]][2]]
    
    # Save the update to the json's file
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

    return None













    
## Get json's file info (about score/level/evaluation scores)

    ### Get knowledge info
def get_knowledge_info(knowledge_path, lowest_scores_size=20):
    '''
    get_knowledge_info is used by get_score_info() and show_score_level()

    This function returns a list that contains:
    - [0]: The min score
    - [1]: The max score
    - [2]: The mean score
    - [3]: The mean level
    - [4]: The list of the "lowest_scores_size" lowest scores
    - [5]: The number of words for each level: {1: x1, 2: x2, ..., 4: x4}
    '''
    # Get data
    with open(knowledge_path, 'r') as file:
        knowledge_data = json.load(file)

    # Create lowest scores list
    if lowest_scores_size > len(knowledge_data):
        raise ValueError(f'"lowest_scores_size" has to be smaller than the number of words: {len(knowledge_data)}.')
    else:
        # Sort scores
        scores = [value[0] for value in knowledge_data.values()]
        sorted_scores = sorted(scores)
        
        # Get all words with lowest scores - check size - if not enough, get all words with second lowest scores, etc.
        lowest_score_list = {}
        while len(lowest_score_list) < lowest_scores_size:
            lowest_score_list.update({key: value for key, value in knowledge_data.items() if value[0] == sorted_scores[0]})
            sorted_scores.remove(sorted_scores[0])
        
        # If we got too many words, we keep the "lowest_scores_size" first
        if len(lowest_score_list) > lowest_scores_size:
            lowest_score_list = {key: value for i, (key, value) in enumerate(lowest_score_list.items()) if i < lowest_scores_size}

    # Create number of words for each level
    level_words = {1:0, 2:0, 3:0, 4:0}
    for value in knowledge_data.values():
        level_words[value[1]] += 1
    
    # Compute mean score and level
    mean_score = np.mean([value[0] for value in knowledge_data.values()])
    mean_level = np.sum([i*level_words[i] for i in range(1, 5)])/np.sum([level_words[i] for i in range(1, 5)])

    # Compute min/max score
    min_score = np.min([value[0] for value in knowledge_data.values()])
    max_score = np.max([value[0] for value in knowledge_data.values()])

    return min_score, max_score, mean_score, mean_level, lowest_score_list, level_words 




    ### From knowledge info, show some useful statistics
def show_means(knowledge_path):
    '''
    Simple presentation of the scores/level
    '''
    min_score, max_score, mean_score, mean_level, lowest_score_list, level_words = get_knowledge_info(knowledge_path)
    print(f'The min score is {min_score}.')
    print(f'The mean score is {np.round(mean_score, 2)}.')
    print(f'The max score is {max_score}.')
    print(f'The mean level is {np.round(mean_level, 2)}.')
    print(f'Here is global word levels: {level_words}')
    return None








## Graphics

'''
In this part, there are many functions to plot our data:
- show_level(path, title) that represents the level of a json file (as a bar plot)
- show_score(path, title='Bar presentation', specific_range, max_value): represents the knowledge scores of a json file (more precise than show_level)
- ???? that represents the evolution of the evaluation score and difficulty together and alone.
'''

    ### Level bar presentation
def show_level(path, title='Bar presentation'):
    '''
    "path" should be a json file with format {key: [score, level, value]}
    "title" is recommended to be "Alphabet/Kanji/Vocabulary score presentation"
    '''
    # Get knowledge info
    levels = get_knowledge_info(path)[5]

    # Plot our info as a bar diagram
    plt.bar(list(levels.keys()), levels.values(), color=['r', 'orange', 'green', 'cyan'])
    plt.title('\n' + title + '\n\nTotal words {}, repartition: {}'.format(np.sum(list(levels.values())), levels) + '\n')
    plt.show()
    return None




    ### Score bar presentation
        #### color selection, necessary for the bar plot
def color_choice(score_value):
    if score_value <= 5:
        return 'r'
    elif score_value < 10:
        return 'orange'
    elif score_value < 20:
        return 'green'
    else:
        return 'cyan'



        #### Limits data to a specific range of words
def specific_range_selection(data, specific_range):
    if (type(specific_range) != list) or (len(specific_range) != 2):
        raise ValueError('"specific_range" has to be "max" or a list of two elements.')

    elif (specific_range[0] < 1) or (specific_range[1] > len(data)):
        raise ValueError(f'"specific_range" values has to be between 1 and {len(data)}')
    
    else:
        return {key: data[key] for i, key in enumerate(list(data.keys())) if i in range(specific_range[0]-1, specific_range[1])}



        #### bar plot function. Change the default title if needed.
def show_score(path, title='Bar presentation', specific_range='max', max_value=25):
    '''
    "path" should be a json file with format {key: [score, level, value]}
    "title" is recommended to be "Alphabet/Kanji/Vocabulary score presentation"
    "specific_range" helps to focus on a specific range of words. For instance, start at word 100
    "max_value" helps focusing on the range (1, max_value) on the bar plot
    '''
    # Get data
    with open(path, 'r') as file:
        data = json.load(file)

    # Modify "data" if the user wants to focus on a specific range
    if specific_range != 'max':
        data = specific_range_selection(data, specific_range)

    # Create a dictionary from the scores
    scores = {}
    for value in data.values():

        # Score limitation
        if max_value != None:
            if value[0] > max_value:
                value[0] = max_value

        # Fill scores
        if value[0] in scores:
            scores[value[0]] += 1
        else:
            scores[value[0]] = 1
    
    # Prepare colors
    colors = [color_choice(score) for score in list(scores.keys())]

    # Plot our info as a bar diagram
    plt.bar(list(scores.keys()), scores.values(), color=colors)
    plt.title('\n' + title + '\n\nTotal words {}'.format(np.sum(list(scores.values()))) + '\n')
    plt.show()
    return None

