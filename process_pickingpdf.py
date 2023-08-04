################ This is the import statement required to reference scripts within the package
import os,sys,glob
ndh_tools_path_opts = [
    '/mnt/data01/Code/',
    '/home/common/HolschuhLab/Code/'
]
for i in ndh_tools_path_opts:
    if os.path.isfile(i): sys.path.append(i)
################################################################################################


def process_pickingpdf(fn,):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    %     This function does the standard load, transformation, and plotting
    %     that is common in the CReSIS radar analysis workflow
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 
    pass