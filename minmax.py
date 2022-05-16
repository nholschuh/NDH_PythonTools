import numpy as np


def minmax(input_array):
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
    output = [np.min(input_array),np.max(input_array)]
        
    return output
    
