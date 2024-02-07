import numpy as np

################ This is the import statement required to reference scripts within the package
import os,sys,glob
ndh_tools_path_opts = [
    '/mnt/data01/Code/',
    '/mnt/l/mnt/data01/Code/',
    '/home/common/HolschuhLab/Code/'
]
for i in ndh_tools_path_opts:
    if os.path.isdir(i): sys.path.append(i)
################################################################################################

import NDH_Tools as ndh

def heading_line(in_x,in_y,distance,turn,heading=np.pi/2):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This function applies a bandpass filter on an input series.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    % data -- the input array to be filtered
    % times -- the array defining the axis of variability that describes "data"
    % lowcut -- the frequency that defines the high-pass transition
    % highcut -- the frequency that defines the low-pass transition
    % order -- the order that defines the butterworth filter
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    % y -- the filtered dataset
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
    if len(in_x) > 1:
        heading_in = ndh.heading(in_x,in_y)
    else:
        heading_in = np.array([heading]);
        
    heading_out = heading_in+turn

    dx = np.cos(heading_out)*distance
    dy = np.sin(heading_out)*distance
    heading_line_x = np.expand_dims(in_x,1)+np.expand_dims(dx,1)
    heading_line_y = np.expand_dims(in_y,1)+np.expand_dims(dy,1)
    
    return heading_line_x, heading_line_y, heading_out
