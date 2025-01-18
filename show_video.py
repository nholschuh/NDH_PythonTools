from IPython.display import HTML 

def show_video(videoname):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This function displays a video inline in a jupyter notebook
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %    videoname -- the array that you want to collapse onto the new spacing
    %    spacing -- the gap between sequential values
    %    shift -- the offset from 0 to round to
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
    
    ################ This is the import statement required to reference scripts within the package
    import os,sys,glob
    ndh_tools_path_opts = [
        '/mnt/data01/Code/',
        '/home/common/HolschuhLab/Code/'
    ]
    for i in ndh_tools_path_opts:
        if os.path.isdir(i): sys.path.append(i); correction_root_dir=i;

    import NDH_Tools as ndh
    ################################################################################################

    if videoname[0] == '/':
        videoname = ndh.absolute_to_relative_path(videoname)
    
    return HTML("""
    <div align="middle">
    <video width="80%" controls>
          <source src="""+videoname+""" type="video/mp4">
    </video></div>""")   