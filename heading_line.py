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
    % (C) Nick Holschuh - Amherst College - 2024 (Nick.Holschuh@gmail.com)
    %
    % This function creates a line with a defined heading relative to a given 
    % point or curve. For use, primarily, in designing geophysical surveys
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    % in_x -- This can be one of two options:
    %         1: a single point, x. In this case, the output line is drawn
    %            starting at that point, with a line pointing at a "turn" angle relative
    %            to the direction defined by "heading"
    %         2: an array of x coordinates along a line. In this case, the output
    %            lines are defined at a given angle relative to the trajectory of
    %            the input lines.
    % in_y -- same as in_x
    % distance -- how far the new line should extent from the source
    % turn -- the angle relative to the heading to direct the new line
    % heading -- only used if a point is supplied for in_x or in_y. See above.
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    % heading_line_x - x coordinate for the new lines.
    % heading_line_y - y coordinate for the new lines
    % heading_out - The direction (angle) of the new lines
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
