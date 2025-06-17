from email import generator
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def DraftEmail(subject=None, emailto=None, body=[], fname='DraftEmail.eml',emailfrom='nholschuh@amherst.edu'):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This function produces a .eml file that can be added to drafts in 
    % Thunderbird to evventually be sent
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %% 
    """

    ################################## Print an example email if you aren't sure how to structure things.
    if len(body) == 0:
        html_data = """\
        \"\"\"
<html>
    <head></head>
    <body>
        <p> Hi Nick</p>
        <p> Congratulations on finishing the first part of the exam process! Below, I provide instructions for part two: exam revisions.</p><p> Your original responses to each question could fall into one of three categories: <p>
        <ul>
          <li><em>Minor Revisions</em> -- it's clear you were thinking about things correctly, but your answer is imprecise or could otherwise be refined.</li>
          <li><em>Major Revisions</em> -- an important idea was missing in your response.</li>
        </ul>
        \"\"\"
        """
        print(html_data)

    else:
        if fname[-3:] != 'eml':
            fname = fname+'.eml'
    
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = emailfrom
        msg['To'] = emailto
    
        if '<' in body:
            part = MIMEText(body, 'html')
        else:
            part = MIMEText(body, 'plain')
        msg.attach(part)
    
        with open(fname, 'w') as outfile:
            gen = generator.Generator(outfile)
            gen.flatten(msg)



