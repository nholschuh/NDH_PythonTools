
def deconstruct_pdf(pdf_name,deconstruct_dir):
    """
    % (C) Nick Holschuh - Amherst College -- 2024 (Nick.Holschuh@gmail.com)
    %
    %     This function extracts annotations from nadir radargrams made on an iPad
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 

    import os
    
    print('Starting the pdf deconstruction for: '+pdf_name)
    os_cmd = 'convert -quality 20 -density 144 %s %s/%s' % (pdf_name,deconstruct_dir,'Frame_%03d.png')
    os.system(os_cmd)

    return(pdf_name)