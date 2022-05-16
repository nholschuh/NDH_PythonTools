import numpy as np


def lp(input_array):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % This function converts amplitude data to power (in dB) -- ie, log power
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     input_array -- amplitude data to convert
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %      output -- log-power data
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 
    output = np.log10(input_array**2)
    
    return output
    
