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
    return HTML("""
    <div align="middle">
    <video width="80%" controls>
          <source src="""+videoname+""" type="video/mp4">
    </video></div>""")   