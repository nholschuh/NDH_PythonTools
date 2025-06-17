import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from email import generator
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def ParseGradescopeGrades(ex_file,summary_plot_flag=1,emails_flag=1,
                          subject_pre = '[Geol 341] -- Assessment One Revision Guidance -- ',
                          email_path = 'Final_RevisionsEmails',major_minor_thresh=[0.5,0.75],revision_flag=1):
    """
    % (C) Nick Holschuh - Amherst College -- 2025 (Nick.Holschuh@gmail.com)
    %
    %     This function takes an exported gradescope excel file and 
    %     generates summary statistics for the assignment. It can also
    %     draft emails for guided exam revision.
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     ex_file -- the filename to parse
    %     summary_plot_flag -- 0 or 1, indicating whether or not you would like summary statistics plotted
    %     emails_flag -- 0 or 1, indicating whether or not to generate emails to send to the students
    %     subject_pre -- The prefix to the email subject line
    %     email_path -- The directory to write the emails into
    %     major_minor_thresh -- This sets the percentage thresholds for major revisions and minor revisions
    %     revision_flag -- 0 or 1, indicating whether or not to include in the email a link to a revisions document.
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %     A dictionary including the summary information for the excel file
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Helpful String: summary_plot_flag=summary_plot_flag, emails_flag=emails_flag, subject_pre= subject_pre, email_path=email_path, major_minor_thresh=major_minor_thresh, revision_flag=revision_flag
    """ 

    grades = pd.read_excel(ex_file)
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
    
    if summary_plot_flag == 1:
        plt.figure(figsize=(15,5))
        plt.subplot(1,2,1)
        plt.plot(question_name,question_total,ls=':',c='black',label='Total Possible')
        plt.plot(question_name,question_mean,'o',c='blue',label='Average')
        plt.plot(question_name,question_median,'.',c='red',label='Median')
        plt.xticks(rotation=90);
        plt.legend()
        plt.ylim(0,np.max(question_total)+1)
        plt.ylabel('Score')
        
        plt.subplot(1,2,2)
        plt.hist(score_percentage*100,np.arange(0,102,2),color='blue')
        plt.xlim(np.min([50,np.min(score_percentage)*100]),100)
        plt.xlabel('Score %')
        plt.ylabel('Count')
        vals = np.arange(0,100,10)
        counter = 0
        for val in vals[::-1]:
            plt.axvline(val,ls=':',c='black')
            if val > 40:
                plt.text(val+5,2,str(np.sum(score_percentage>(val/100))-counter))
            counter = np.sum(score_percentage>(val/100))
        
        plt.title('Mean: %0.2f%%' % (np.mean(score_percentage)*100))
            
    
    if emails_flag == 1:
        results_path = email_path
        results_folder_exist = os.path.exists(results_path)
        if results_folder_exist == 0:
            os.makedirs(results_path)
        
        ###############################
        ##### We loop through the students
        for ind1,i in enumerate(first_names):
            
            subject_line =  subject_pre+first_names[ind1]+' '+last_names[ind1]+'.'
        
            running_total = 0
            response_category = []
            question_list = []
        
            #############################
            ### Then we loop through the questions, and identify which are specific problems
            for ind2,j in enumerate(question_name):
                question_list.append(j)
                
                if scores_array[ind1][ind2] >= question_total[ind2]*major_minor_thresh[1]:
                    response_category.append(2)
                elif scores_array[ind1][ind2] >= question_total[ind2]*major_minor_thresh[0]:
                    response_category.append(1)
                elif scores_array[ind1][ind2] <= question_total[ind2]*major_minor_thresh[0]:
                    response_category.append(0)
                    
            response_category = np.array(response_category)
        
            email_fname = 'ResponesFile_'+first_names[ind1]+'_'+last_names[ind1]+'.eml'
        
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject_line
            msg['From'] = 'nholschuh@amherst.edu'
            msg['To'] = email[ind1]
            #msg['To'] = ''
        
            html_data = """\
            <html>
                <head></head>
                <body>
                    <p> Hi """+first_names[ind1]+""",</p>
                    <p> Congratulations on finishing the first part of the exam process! Below, I provide instructions for part two: exam revisions.</p><p> Your original responses to each question could fall into one of three categories: <p>
                    <ul>
                      <li><em>Great</em> -- you got the major idea, and no revisions required.</li>
                      <li><em>Minor Revisions</em> -- it's clear you were thinking about things correctly, but your answer is imprecise or could otherwise be refined.</li>
                      <li><em>Major Revisions</em> -- an important idea was missing in your response.</li>
                    </ul>
                    <p> Your job now is to update your responses to the questions that require minor or major revisions. You can find a copy of your submitted exam (and your original responses) on gradescope.
                    """
        
            if revision_flag == 1:
                html_data =  html_data+ """
                        The <a href="https://docs.google.com/document/d/1QsXjHgx_21fgcZi90TsWc8IB0gNv0syBF5tUfCQH8JA/edit?usp=sharing">template for your revisions can be found here,</a> and once you've filled it out, 
                        it can be submitted through Moodle.</p>
                 """
        
        
            total_opts_length = 0
            for j in 2-np.arange(3):
                    opts = np.where(response_category == j)[0]
                
                    if len(opts) > 0:
                        
                        if j == 2:
                            html_data = html_data+'<p><b><u> Great -- you got (essentially) full credit for: </u></b></p>'
                        elif j == 1:
                            html_data = html_data+'<p><b><u> Minor Revisions: </u></b></p>'
                        elif j == 0:
                            html_data = html_data+'<p><b><u> Major Revisions: </u></b></p>'
        
                        html_data = html_data+'<p>'
                        for k in opts:
                            fill_str = question_list[k].split(' ')
                            html_data = html_data+fill_str[1]+', '
        
                        html_data = html_data[:-2]
                        html_data = html_data+'</p>'
        
                        total_opts_length = total_opts_length+len(opts)
        
            if total_opts_length == 0:
                html_data = html_data+'<nr><p><b> Amazing job on the exam! You do not require any revisions -- any issues you had in your responses were small. </b></p><br>'
                    
            
            html_data = html_data+"""<p> If you have any questions, don't hesitate to reach out! And remember, I encourage you to work together, talk with your peers, and come to office hours if you are struggling to understand
            what is wrong in your responses.</p><p>Nick</p> <br><em> I apologize if this email doesn't use the preferred form of your name, I generated them programmatically using information from Gradescope...</em></body></html>"""
        
            part = MIMEText(html_data, 'html')
            msg.attach(part)
        
            if len(response_category) > 0:
                outfile_name = os.path.join(results_path, email_fname)
                with open(outfile_name, 'w') as outfile:
                    gen = generator.Generator(outfile)
                    gen.flatten(msg)
    
    return {'First_Names': first_names, 'Last_Names': last_names, 'Email':email, 'final_score': score_points, 'max_possible_score': max_score, 'scores_array': scores_array, 'question_names':question_name, 'question_value': question_total, 'question_mean_score':question_mean}