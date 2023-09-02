import json
import numpy as np

import jap_data
import global_functions









# SOMMAIRE

## Alphabet to json (json creation)
## json's file modification


## Get information about our knowledge


    #####  TO CODE #####


## Show scores / level (on specific range of the vocabulary list)


    #####  TO CODE #####



## Alphabet's training
## JPTL5 alphabet





'''
Remark. When we build the json file "jap_alphabet.json", there are only 210 elements.
The reason is that there are some repetitions in romanjis ("ji", "zu") and "ヘ" is
both a hiragana and a katakana.

The format of the json file is as follow:
key: [score, level, [translation_1, translation_2]]

The score increases by 1 each time the player gets a correct answer and decreases with bad answer
There are several steps in scores (5, 10, 20). Exceed those steps make the level increases.
Negative scores is possible.
'''

# Alphabet to json: json's file creation from romanji/hiragana/katakana
def alphabet_json_creation(path):
    # Get data from alphabet
    romanji, hiragana, katakana = jap_data.romanji, jap_data.hiragana, jap_data.katakana
    
    # data preparation
    data = {}
    for i, element in enumerate(romanji):
        if element not in data.keys():
            data[element] = [0, 1, [hiragana[i], katakana[i]]]
    for i, element in enumerate(hiragana):
        if element not in data.keys():
            data[element] = [0, 1, [romanji[i], katakana[i]]]
    for i, element in enumerate(katakana):
        if element not in data.keys():
            data[element] = [0, 1, [romanji[i], hiragana[i]]]
    
    # json creation
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

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
### Example: "global_functions.jap_JLPT_update_value(path, key, value)"  ###








## S'entraîner à l'alphabet
'''
The training function's name is: alphabet_training(training_size, specificity)
training_size: number of questions nombre de questions par sens de traduction
specificity: permet de s'entraîner sur un sens spécifique de traduction. Par défaut "all", sinon 1, 2 ou 3.

La fonction alphatbet_training s'appuie sur les fonctions
- alphabet_training_selection: selects the elements that will be given as questions/answers
- alphabet_questions_presentation: prints the titles and the questions.
- alphabet_correction_presentation: prints the corrections
'''


def alphabet_training_selection(training_size=12):
    '''
    This function selects the romanji/hiragana/katakana
    for training (as random without weight)

    Output format : [{'re': [lvl, points, ['hiragana', 'katakana']]}, {...}, {...}]
    '''
    # Get data
    with open('jap_alphabet.json', 'r') as file:
        data = json.load(file)
    
    # Splitting data into our three kinds of alphabet
    keys = list(data.keys())
    romanji_json = {keys[i]: data[keys[i]] for i in range(69)}  # Romanji selection
    hiragana_json = {keys[i]: data[keys[i]] for i in range(69, 140)}  # Hiragana selection
    katakana_json = {keys[i]: data[keys[i]] for i in range(140, 210)}  # Katakana selection

    # Random selection of data without weight
    romanji_test = {key: romanji_json[key] for key in np.random.choice(list(romanji_json.keys()), training_size, replace=False)}
    hiragana_test ={key: hiragana_json[key] for key in np.random.choice(list(hiragana_json.keys()), training_size, replace=False)}
    katakana_test ={key: katakana_json[key] for key in np.random.choice(list(katakana_json.keys()), training_size, replace=False)} 

    # Output format : [{'re': [lvl, points, ['hiragana', 'katakana']]}, {...}, {...}]
    return [romanji_test, hiragana_test, katakana_test]




def alphabet_questions_presentation(training_test, specificity='all'):
    # Create guidlines titles for questions
    guidlines = ['Romanji to hiragana & katakana',
                'Hiragana to romanji & katakana',
                'Katakana to romanji & hiragana']

    # If we want to do the classical training
    print('\nAlphabet training: Romanji, Hiragana, Katakana\n')
    if specificity == 'all':
        for i in range(3):
            print('\n' + f'{i+1}. ' + guidlines[i] + '\n')
            for key in training_test[i].keys():
                print(key)
    
    # If we want to train on a specific kind of translation
    else:
        print('\n' + f'{specificity}. ' + guidlines[specificity-1] + '\n')
        for key in training_test[specificity-1].keys():
            print(key)




def alphabet_correction_presentation(training_test, specificity='all'):
    # Presentation
    print('\nCorrection time.\n')
    input('Press any key to see the correction')

    # Create guidlines titles for corrections
    translation_guidlines = ['Romanji\'s translation',
                             'Hiragana\'s translation',
                             'Katakana\'s translation']
    
    # If we did the classical test, then we print all the corrections
    if specificity == 'all':
        for i in range(3):
            print('\n' + f'{i+1}. ' + translation_guidlines[i] + '\n')
            for key, value in training_test[i].items():
                print(f'{key} => {value[2]}')
    
    # Else, we print only the specific correction
    else:
        print('\n' + f'{specificity}. ' + translation_guidlines[specificity-1] + '\n')
        for key, value in training_test[specificity-1].items():
            print(f'{key} => {value[2]}')
    return None




def alphabet_training(training_size, specificity='all'):
    # Check training_size and specificity input values
    if training_size not in range(1, 70):
        raise ValueError('"training_size" parameter has to be between 1 and 69')
    if specificity not in ['all', 1, 2, 3]:
        raise ValueError('"specificity" parameter has to be "all", "1", "2" or "3"')
    
    # Get selected values for training
    training_test = alphabet_training_selection(training_size)

    # Show questions
    alphabet_questions_presentation(training_test, specificity)

    # Show corrections
    alphabet_correction_presentation(training_test, specificity)











## JPTL5 alphabet

'''
"JLPT5_alphabet" is a function that is call by the JLPT5 test.
The output is close to the alphabet_training function, but it computes your success rate and remember your errors.
So, it's basically the same function for the users, but with memory to know which translation you know and you don't know.

"JLPT5_alphabet" calls the function update_scores which update the scores/levels in the json's file.
'''



def JLPT5_alphabet(size=12):
    
    # Get selected values for training
    alphabet_test = alphabet_training_selection(size)

    # Show questions
    alphabet_questions_presentation(alphabet_test)

    # Show corrections
    alphabet_correction_presentation(alphabet_test)

    # Check mistakes
    number_mistakes, list_mistakes = global_functions.get_mistakes()

    # Add 'S' for success and 'F' for fail to all test we did
    SF_list = []
    for translation_sens in alphabet_test:
        SF_list.extend(global_functions.success_fail_list(translation_sens, list_mistakes))

    # Update scores & level + update json's file
    global_functions.update_scores('jap_alphabet.json', SF_list)

    # Return the mistakes list and the success rate (among 0 and 1)
    return list_mistakes, np.round(100*(3*size - number_mistakes)/(3*size), 1)