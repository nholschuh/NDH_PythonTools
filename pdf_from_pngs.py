import os

def pdf_from_pngs(imdir,pdfname):
    """
    % (C) Nick Holschuh - Amherst College -- 2024 (Nick.Holschuh@gmail.com)
    % 
    %    This function calls the imagemagick command "convert" to make a pdf from pngs in a directory
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     imdir -- You must provide this with a directory containing pngs
    %     pdfname -- The name of the file to write
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 
    
    frames = '%s/*.png' % (imdir)

    os.system("convert -adjoin "+frames+" -gravity center -scale '90<x770<' "+pdfname)