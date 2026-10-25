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
    %     print_corrections -- 0, 1 or 2. 1 prints the full block per student, 2 prints the
    %                          compact one-line form ("Name -- Corrections: value"). Both run
    %                          in roster order, the order the original export lists them in.
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

    # Merge on Email, not SID -- SID is blank for students without one, and pandas treats
    # NaN as a joinable key, so every no-SID student in one file matches every no-SID
    # student in the other (10 of each here turned 37 rows into 127).
    grades2_reordered = grades1[['Email']].merge(grades2, on='Email', how='left')
    assert len(grades2_reordered) == len(grades1), 'Email is not a unique key in one of the two exports'

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
                # Students who never submitted have blank question scores; those count as zeros,
                # so a missing revision gives no correction rather than a NaN final score.
                scores_array.append(grades[key].fillna(0).to_list())
                
            if 'First ' in key:
                first_names = grades[key]
            if 'Last ' in key:
                last_names = grades[key]
            if 'Email' in key:
                email = grades[key]
            if 'Total' in key:
                score_points = grades[key]
            if 'Max Points' in key:
                max_score = grades[key].dropna().iloc[0]
        
        score_percentage = np.array(score_points)/max_score
        scores_array = np.array(scores_array,dtype=float).T
        
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
    final_total = original_total+correction_total
    final_total_percent = final_total/original_max*100

    # First name plus last initial -- two students sharing a first name would otherwise
    # land on the same bar, and .to_numpy() keeps this positional alongside sort_order
    first_names = np.array(grades_dicts[0]['First_Names'].to_list())
    last_names = np.array(grades_dicts[0]['Last_Names'].to_list())
    bar_labels = np.array([f'{x} {y[0]}.' for x,y in zip(first_names,last_names)])

    ###### A student who still totals zero after corrections never handed anything in. They are
    ###### dropped from the figure and the summary statistics, where six automatic zeros drag the
    ###### mean down and pin the range to the full scale, but they stay in the printout below.
    submitted = final_total > 0

    plot_labels = bar_labels[submitted]
    plot_total = original_total[submitted]
    plot_correction = correction_total[submitted]
    plot_percent = original_total_percent[submitted]
    plot_final_percent = final_total_percent[submitted]

    sort_order = np.argsort(plot_total)[::-1]

    ###### Letter grades on the usual cutoffs, as a percentage of the total possible
    grade_floors = np.array([90,80,70,60,0])
    grade_names = ['A','B','C','D','F']

    before_counts = np.zeros(len(grade_names),dtype=int)
    after_counts = np.zeros(len(grade_names),dtype=int)
    for ind0,floor in enumerate(grade_floors):
        ceiling = 200 if ind0 == 0 else grade_floors[ind0-1]   # nothing sits above an A
        before_counts[ind0] = np.sum((plot_percent >= floor)&(plot_percent < ceiling))
        after_counts[ind0] = np.sum((plot_final_percent >= floor)&(plot_final_percent < ceiling))

    ###### The summary statistics are reported as a percentage of the total possible
    before_range = np.max(plot_percent)-np.min(plot_percent)
    after_range = np.max(plot_final_percent)-np.min(plot_final_percent)

    if summary_plot_flag == 1:
        # Open a wide figure as ParseGradescopeGrades does -- at the default size a full
        # roster's worth of names on the x axis overlaps into an unreadable smear
        plt.figure(figsize=(20,5))

        ############### Per-student scores, with the corrections stacked on the original
        ax = plt.subplot(1,4,(1,3))

        # The first layer sits at the bottom (no 'bottom' parameter needed)
        ax.bar(plot_labels[sort_order], plot_total[sort_order], label='Original Score')

        # The second layer sits on top of group1
        ax.bar(plot_labels[sort_order], plot_correction[sort_order], bottom=plot_total[sort_order], label='Corrections',color='orange')
        plt.xticks(rotation=45, ha='right') # 'ha' aligns the right edge of the text to the tick mark

        plt.axhline(original_max,c='black')
        for val in np.arange(0.5,1,0.1):
            plt.axhline(original_max*val,ls=':',c='black')
            plt.ylabel('Final Score')
        plt.legend()

        ############### How the letter grade distribution moves once the corrections are applied
        plt.subplot(1,4,4)
        bar_x = np.arange(len(grade_names))
        plt.bar(bar_x-0.2,before_counts,width=0.4,label='Before')
        plt.bar(bar_x+0.2,after_counts,width=0.4,label='After',color='orange')

        for x,before,after in zip(bar_x,before_counts,after_counts):
            plt.text(x-0.2,before,str(before),ha='center',va='bottom')
            plt.text(x+0.2,after,str(after),ha='center',va='bottom')

        plt.xticks(bar_x,grade_names)
        plt.xlabel('Letter Grade')
        plt.ylabel('Number of Students')
        plt.ylim(0,np.max(np.concatenate([before_counts,after_counts]))*1.25)
        plt.legend(loc='upper left')

        # Monospace keeps the before/after columns lined up under one another. The count says how
        # many students the statistics cover, since the non-submitters are not among them.
        plt.title('%d submissions (%d excluded)\nMean:   %5.1f%% -> %5.1f%% (%+0.1f)\nMedian: %5.1f%% -> %5.1f%% (%+0.1f)\nRange:  %5.1f%% -> %5.1f%% (%+0.1f)' % (
                  np.sum(submitted),np.sum(~submitted),
                  np.mean(plot_percent),np.mean(plot_final_percent),np.mean(plot_final_percent)-np.mean(plot_percent),
                  np.median(plot_percent),np.median(plot_final_percent),np.median(plot_final_percent)-np.median(plot_percent),
                  before_range,after_range,after_range-before_range),
                  fontfamily='monospace',fontsize=9,loc='left')

        plt.tight_layout()

    ###### Pad the names and right-align the numbers to a width taken from the widest entry, so every
    ###### value lands in the same character column and a copy-pasted block stays in register
    name_strings = ['%s %s' % (x,y) for x,y in zip(first_names,last_names)]
    name_width = int(np.max([len(x) for x in name_strings]))               # int() -- %*s rejects np.int64

    # Pad on the integer part rather than the whole field: scores carry two decimals and
    # corrections three, so equal field widths would still leave the decimal points a column apart
    int_width = int(np.max([len(str(int(x))) for x in np.concatenate([original_total,final_total,correction_total])]))
    score_width = int_width+3                                              # the '.' and two decimals
    correction_width = int_width+4                                         # the '.' and three decimals

    if print_corrections == 1:
        for ind0,total in enumerate(original_total):
            print(name_strings[ind0])
            print ('--------------------------------')
            # 'Corrections:' is padded out to the width of 'Original Score:' so the two columns agree
            print('Original Score: %*.2f \t Final Score: %*.2f' % (score_width,total,score_width,final_total[ind0]))
            print('Corrections:    %*.3f' % (correction_width,correction_total[ind0]))
            print(' ')

    if print_corrections == 2:
        for ind0,name in enumerate(name_strings):
            print('%-*s -- Corrections: %*.3f' % (name_width,name,correction_width,correction_total[ind0]))