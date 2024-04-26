import numpy as np

def heading(input_x,input_y):
    """
    % (C) Nick Holschuh - Amherst College - 2024 (Nick.Holschuh@gmail.com)
    % This function calculates the heading of a line (in radians) relative to 
    % a horizontal line (or a line pointing in the x direction)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    % input_x -- array of x coordinates for the path of interest
    % input_y -- array of y coordinates for the path of interest
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    % out_angles -- heading of the line, in radians. Should be same shape as
    %               input line.
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
    
    out_angles = np.arctan2(np.diff(input_y),np.diff(input_x))
    out_angles = np.concatenate([np.array([out_angles[0]]),out_angles])
    return out_angles
