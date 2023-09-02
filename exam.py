# Importation
import json
import os

import numpy as np
import matplotlib.pyplot as plt

import jap_data
import jap_alphabet
import jap_JPTL5_80kanji
import jap_JLPT5_vocabulary
import jap_JLPT5_sentences
import jap_JLPT5_kanji_and_basic_vocabulary
import global_functions



# Sommaire

    ## Access to the evolution's data
    ## print_mistakes => used to simplify JLPT5_bilan_evaluation
    ## Show results + plots evolution scores + difficulty
        ### Colors' choice function
        ### Main plot function
    ## Bilan evaluation => Show results + Plot evolution scores + Mistakes information

    ## Exam function

    ## Show evolution without taking the exam: get_evaluation_score_info_JLPT5(evaluation_path='JLPT5_evaluation.json'):











## Access to the evolution's data

def evaluation_data_access(path, exercises):
    '''
    Check if the evaluation data's file exists.
    If yes, access to it and return it.
    Else, create it and return it.
    '''
    if os.path.exists(path):
        with open(path, 'r') as file:
            evaluation_data = json.load(file)
    else:
        # Protection from evolution_data being erased
        evaluation_data_creation = input('Is this your first time doing the evaluation? (Y/N)')
        if evaluation_data_creation == 'Y':    
            evaluation_data = {key: [] for key in exercises}
            evaluation_data.update({'Global': []})
            evaluation_data.update({'difficulty': []})
        else:
            print('An error occured trying to open the file "JLPT5_evaluation.json"')
    
    return evaluation_data








## print_mistakes => used to simplify JLPT5_bilan_evaluation

def print_mistakes(list_mistakes, exercises):
    '''
    Simplify JLPT5_bilan_evaluation.
    Print the exam mistakes.
    '''
    # Paths specific to level 1
    paths = ['jap_alphabet.json', 'JLPT5_jap_kanji.json', 'JLPT5_fr_kanji.json', 'JLPT5_jap_vocabulary.json', 'JLPT5_fr_vocabulary.json']
    
    for i in range(len(list_mistakes)):
        if len(list_mistakes[i]) != 0:
            with open(paths[i], 'r') as file:
                data = json.load(file)
            
            print('Error(s) {}:\n'.format(exercises[i]))
            for mistake in list_mistakes[i]:
                print('{} => {}'.format(mistake, data[mistake]))
            print('')
        else:
            print('{}: perfect!'.format(exercises[i]))



def print_mistakes_level2(exercises, final_errors_resume):
    '''
    A ECRIRE
    '''
    for i in range(len(final_errors_resume)):
        if len(final_errors_resume[i]) != 0:
            print('Error(s) {}:\n'.format(exercises[i]))
            for error in final_errors_resume[i]:
                print(f'{error[0]} => {error[1]}')
        else:
            print('{}: perfect !'.format(exercises[i]))
    return None








## Show results + plots evolution scores + difficulty

    ### Little function for the colors' choice
def score_evolution_color_choice(value):
    if value < 60:
        return 'r'
    elif value < 70:
        return 'orange'
    elif value < 80:
        return 'gold'
    elif value < 90:
        return 'lawngreen'
    else:
        return 'cyan'
    

    ### Main function => show results + plots
def show_score_difficulty_evolution(data):
    '''
    ----- Can be updated for better plots -----

    This function plots two graphs.
    The first one shows the score evolution of each exercises + difficulty
    The second one shows the gloabl score evolution + the difficulty's evolution
    '''
    abscisse = range(1, len(data['Global']) + 1)
    score_colors = ['r', 'b', 'orange', 'y', 'c']
    labels = ['Ex1: alphabet', 'Ex2: Jap => Fr (Kanji)', 'Ex3: Fr => Jap (Kanji)', 'Ex4: Jap => Fr (vocabulary)', 'Ex5: Fr => Jap (vocabulary)']
    global_color = [score_evolution_color_choice(global_score) for global_score in data['Global']]

    figure = plt.figure(figsize=(20, 10))

    plt.subplot(121)
    for i in range(len(labels)):
        plt.plot(abscisse, data['Exercise {}'.format(i+1)], color=score_colors[i], label=labels[i])
    plt.plot(abscisse, data['difficulty'], color='m', linewidth=4, label='Difficulty')
    plt.legend()

    plt.subplot(122)
    plt.bar(abscisse, data['Global'], color=global_color, label='Global score')
    plt.plot(abscisse, data['difficulty'], color='m', linewidth=4, label='Difficulty')
    plt.legend()
    plt.show()

    return None










## Bilan evaluation => Show results + Plot evolution scores + Mistakes information

def JLPT5_bilan_evaluation(list_mistakes, success_rates, final_errors_resume=None):
    '''
    "list_mistakes" is a list. The ith element is the list of the mistakes at exercise "i".
    "success_rates" is quite the same, but for success_rates.
    "difficulty" is needed since this bilan also measure the difficulty improvement.

    To adapt it to JLPT4+, you need to change:
    - "paths"'s value
    - evaluation_data_access's input
    - evaluation_data['difficulty'] if difficulty == 'max'
    '''
    # Value to modify for JLPT4+
    path = 'JLPT5_evaluation.json'

    # Compute the individual exercise points
    exercises_points = [10, 20, 20, 25, 25]
    scores = [(success_rates[i] * exercises_points[i]/100) for i in range(len(list_mistakes))]
    total_score = np.sum(scores)

    # Guidlines
    exercises = [f'Exercise {i+1}' for i in range(len(list_mistakes))]

    # Print scores + success rates
    print('\n\nIndividual scores:\n\n')
    for i in range(5):
        print(f'{exercises[i]}: {int(success_rates[i])}% => {int(scores[i])} points.')
    print('\n\nFinal result: {}/100'.format(int(np.sum(scores))))

    # Access to evaluation data
    evaluation_data = evaluation_data_access(path, exercises)

    # Update evaluation data
    for i, key in enumerate(exercises):
        evaluation_data[key].append(success_rates[i])
    evaluation_data['Global'].append(total_score)
    # --- I think there will be around 1000 words => "/10" ---
    evaluation_data['difficulty'].append(len(jap_data.JLPT5_voc_fr)/10)

    # Save update
    with open(path, 'w') as file:
        json.dump(evaluation_data, file, indent=4)
    
    # Show the scores / difficulty evolutions throught plots
    show_score_difficulty_evolution(evaluation_data)

    # Print mistakes for each exercise
    if final_errors_resume == None:
        print_mistakes(list_mistakes, exercises)
    else:
        print_mistakes_level2(exercises, final_errors_resume)

    return None


















## The exam function!
def exam_JLPT5(size_vocabulary=3, size_kanji=3, size_alphabet=12, size_sentences=2):
    '''
    This exam has five exercices (for any level of difficulty).

    Those exercices depend on the difficulty knowledge:
    - If difficulty knowledge is lower than 40, then level 1 exam is chosen
    - If difficulty knowledge is between 40 and 75, then level 2 exam is chosen
    - Else, level 3 exam is chosen
    
    '''

    # Auto-update, if needed
    global_functions.json_auto_update('JLPT5_fr_vocabulary.json', 'JLPT5_jap_vocabulary.json', jap_data.JLPT5_voc_fr, jap_data.JLPT5_voc_jap)

    # Get difficulty
    try:
        with open('JLPT5_evaluation.json', 'r') as file:
            data = json.load(file)
    except IOError as e:
        print(f'{e}: impossible to open the file')
    
    difficulty = data['difficulty'][-1]

    # Depending on current difficulty level, choose adapted exam level
    if difficulty < 40:
        exam_JLPT5_level1(size_vocabulary, size_kanji, size_alphabet)
    
    else:
        exam_JLPT5_level2(size_vocabulary, size_kanji, size_sentences)

    # elif difficulty < 85:
    #     exam_JLPT5_level2(size_vocabulary, size_kanji, size_sentences)
    
    #     if difficulty > 70:
    #         return 'Think about coding exam level 3'
    
    # # WRITE THIS PART WHEN WE REACH DIFFICULTY 75 
    # else:
    #     return 'exam_JLPT5_level_3 needs to be created'
    # #     exam_JLPT5_level3(??)
    
    return None





def exam_JLPT5_level1(size_vocabulary=3, size_kanji=3, size_alphabet=12):
    '''
    This exam has five exercises.
    First one is about alphabet. It only worth 10 points because it's the easiest.
    Exercise 2 is about kanji (from Japanese to French). It worths 20 points. There are 80 differents kanjis
    Exercise 3 is also about kanji but from French to Japanese, 20 points too.
    Exercise 4 & 5 are about vocabulary. This vocabulary is quite large: ---------(255 right now)---------
    In the end, you have a recap of your performance with plots and details.
    Good luck!
    '''
    # Introduction sentence to medium difficulty JLPT5
    print('JLPT 5, medium difficulty yookoso')

    # PART 1: Alphabets test (by default, size=12)
    list_mistakes_ex1, success_rate_ex1 = jap_alphabet.JLPT5_alphabet(size=size_alphabet)

    # PART 2: JLPT5 Kanji test (jap => fr)
    list_mistakes_ex2, success_rate_ex2 = jap_JPTL5_80kanji.JLPT5_kanji(size=size_kanji, direction=0)

    # PART 3: JLPT5 Kanji test (fr => jap)
    list_mistakes_ex3, success_rate_ex3 = jap_JPTL5_80kanji.JLPT5_kanji(size=size_kanji, direction=1)

    # PART 4: JLPT5 vocabulary test (jap => fr)
    list_mistakes_ex4, success_rate_ex4 = jap_JLPT5_vocabulary.JLPT5_vocabulary(size=size_vocabulary, direction=0)
    # PART 5: JLPT5 vocabulary test (fr => jap)
    list_mistakes_ex5, success_rate_ex5 = jap_JLPT5_vocabulary.JLPT5_vocabulary(size=size_vocabulary, direction=1)

    # Plot progress & recap mistakes
    list_mistakes = [list_mistakes_ex1, list_mistakes_ex2, list_mistakes_ex3, list_mistakes_ex4, list_mistakes_ex5]
    success_rates = [success_rate_ex1, success_rate_ex2, success_rate_ex3, success_rate_ex4, success_rate_ex5]
    JLPT5_bilan_evaluation(list_mistakes, success_rates)

    return None




def exam_JLPT5_level2(size_vocabulary=3, size_kanji=3, size_sentences=2):
    '''
    With level 2, there are also five exercises.
    Exercice 1 is about sentences. It's a new exercises using vocabulary in sentences contexte
    Exercise 2 and 3 are similar to the exercise 2 and 3 from level 1, but we had some vocabulary kanji in it
    Exercice 4 and 5 are the same than those from level 1. 

    Objective: substitude list_mistake by final_errors_resume and adapt JLPT5_bilan_evaluation.
    Maybe start with another JLPT5_bilan_evaluation, like level_2

    Good luck for level 2! You are coming closer to being able to use Japanese in real life :)
    '''
    # PART 1: Sentences test. There are 5*size_sentences sentences to translate from Fr -> Jap and same from Jap -> Fr
    list_mistakes_ex1, success_rate_ex1, final_errors_resume_ex1 = jap_JLPT5_sentences.JLPT5_sentences(size=size_sentences)

    # PART 2: JLPT5 Kanji + Basic vocabulary test (Jap => Fr)
    list_mistakes_ex2, success_rate_ex2, final_errors_resume_ex2 = jap_JLPT5_kanji_and_basic_vocabulary.JLPT5_Exercice23_evaluation(size=size_kanji, direction=0)

    # PART 3: JLTP5 Kanji + Basic vocabulary test (Fr => Jap)
    list_mistakes_ex3, success_rate_ex3, final_errors_resume_ex3 = jap_JLPT5_kanji_and_basic_vocabulary.JLPT5_Exercice23_evaluation(size=size_kanji, direction=1)

    # PART 4: JLPT5 vocabulary test (jap => fr)
    list_mistakes_ex4, success_rate_ex4, final_errors_resume_ex4 = jap_JLPT5_vocabulary.JLPT5_vocabulary(size=size_vocabulary, direction=0)

    # PART 5: JLPT5 vocabulary test (fr => jap)
    list_mistakes_ex5, success_rate_ex5, final_errors_resume_ex5 = jap_JLPT5_vocabulary.JLPT5_vocabulary(size=size_vocabulary, direction=1)

    # Plot progress & recap mistakes
    list_mistakes = [list_mistakes_ex1, list_mistakes_ex2, list_mistakes_ex3, list_mistakes_ex4, list_mistakes_ex5]
    success_rates = [success_rate_ex1, success_rate_ex2, success_rate_ex3, success_rate_ex4, success_rate_ex5]
    final_errors_resume = [final_errors_resume_ex1, final_errors_resume_ex2, final_errors_resume_ex3, final_errors_resume_ex4, final_errors_resume_ex5]
    JLPT5_bilan_evaluation(list_mistakes, success_rates, final_errors_resume)

    return None







## Show evolution without taking the exam

def get_evaluation_score_info_JLPT5(evaluation_path='JLPT5_evaluation.json'):
    '''
    This function doesn't work if the user never took an evaluation yet.
    Else, it plots the scores evolution for each exercise (with the difficulty) and
    the global exam score evolution with the difficulty.

    "evaluation_path" is the path to the evaluation results: "JLPT5_evaluation.json" here
    '''
    # Check if path exists
    if os.path.exists(evaluation_path):
        with open(evaluation_path, 'r') as file:
            data = json.load(file)
        
        show_score_difficulty_evolution(data)

    # Else error message
    else:
        print(f'There was a problem trying to reach {evaluation_path}\' file.')

    return None
