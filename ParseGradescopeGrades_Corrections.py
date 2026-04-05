import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def ParseGradescopeGrades_Corrections(original_fn,revisions_fn,correction_frac=0.5,summary_plot_flag=1, print_corrections=1):
    """
    % (C) Nick Holschuh - Amherst College -- 2025 (Nick.Holschuh@gmail.com)
    %
    %     This function takes a pair of gradescope exports and calculates
    %     the points given for corrections
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     original_fn -- the filename for the original score
    %     revisions_fn -- the filename for the revised score
    %     correction_frac -- 0 to 1, indicating the fraction of points to return
    %     summary_plot_flag -- 0 or 1, indicating whether or not to generate the bar chart with summaries
    %     print_corrections -- 0 or 1, indicating whether or not to print the corrections scores
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %     Nothing
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 
    
    grades1 = pd.read_excel(original_fn)
    grades2 = pd.read_excel(revisions_fn)

    grades2_reordered = grades1[['SID']].merge(grades2, on='SID', how='left')

    grades_list = [grades1, grades2_reordered]
    grades_dicts = []
    for grades in grades_list:
        grade_keys = grades.keys()
        question_name = []
        question_total = []
        question_mean = []
        question_median = []
        question_std = []
        
        scores_array = []
        
        first_names = []
        last_names = []
        email = []
        
        for ind0,key in enumerate(grade_keys):
            if 'pts' in key:
                pt_val = eval(key.split('(')[1].split(' ')[0])
                question_name.append(key.split('(')[0])
                question_total.append(pt_val)
                question_mean.append(grades[key].mean())
                question_median.append(pd.Series(grades[key]).quantile(0.5))
                question_std.append(grades[key].std())
                scores_array.append(grades[key].to_list())
                
            if 'First ' in key:
                first_names = grades[key]
            if 'Last ' in key:
                last_names = grades[key]
            if 'Email' in key:
                email = grades[key]
            if 'Total' in key:
                score_points = grades[key]
            if 'Max Points' in key:
                max_score = grades[key][0]
        
        score_percentage = np.array(score_points)/max_score
        scores_array = np.array(scores_array).T
        
        grades_dicts.append({'First_Names': first_names, 'Last_Names': last_names, 'Email':email, 'final_score': score_points, 
                             'max_possible_score': max_score, 'scores_array': scores_array, 'question_names':question_name, 
                             'question_value': question_total, 'question_mean_score':question_mean})
    

    ###### The total value of their corrections is the difference between their score on the revisions and their original score, times a scalar
    correction = np.max(np.array([grades_dicts[0]['scores_array'],grades_dicts[1]['scores_array']]),axis=0)-grades_dicts[0]['scores_array']
    correction = correction*correction_frac
    correction_total = np.sum(correction,axis=1)

    original_max = grades_dicts[0]['max_possible_score']
    original_score = grades_dicts[0]['scores_array']
    original_total = np.sum(original_score,axis=1)
    original_total_percent = np.sum(original_score/original_max*100,axis=1)
    #final_total = np.sum(final_score/21*100,axis=1)

    sort_order = np.argsort(original_total)[::-1]

    if summary_plot_flag == 1:
        # The first layer sits at the bottom (no 'bottom' parameter needed)
        ax = plt.gca()
        ax.bar(grades_dicts[0]['First_Names'][sort_order], original_total[sort_order], label='Original Score')
        
        # The second layer sits on top of group1
        ax.bar(grades_dicts[0]['First_Names'][sort_order], correction_total[sort_order], bottom=original_total[sort_order], label='Corrections',color='orange') 
        plt.xticks(rotation=45, ha='right') # 'ha' aligns the right edge of the text to the tick mark
    
        plt.axhline(original_max,c='black')
        for val in np.arange(0.5,1,0.1):
            plt.axhline(original_max*val,ls=':',c='black')
            plt.ylabel('Final Score')

    if print_corrections == 1:
        for ind0,total in enumerate(original_total):
            print('%s %s' % (grades_dicts[0]['First_Names'][ind0],grades_dicts[1]['Last_Names'][ind0]))
            print ('--------------------------------')
            print('Original Score: %0.2f \t Final Score: %0.2f' % (total, total+correction_total[ind0]))
            print('Corrections: %0.3f' % correction_total[ind0])
            print(' ')