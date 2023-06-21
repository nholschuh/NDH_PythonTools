import numpy as np


def box_from_corners(xs,ys):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % This function prints out the minimum and maximum values of an array
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     input_array -- array of data to analyze
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %      output -- the min and max in a 1x2 array
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 
    x_array = np.array([xs[0],xs[1],xs[1],xs[0],xs[0]])
    y_array = np.array([ys[1],ys[1],ys[0],ys[0],ys[1]])
    
    box = np.stack([x_array,y_array]).T
        
    return box
    
