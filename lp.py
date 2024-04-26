import numpy as np


def lp(input_array,amp0_or_power1=1):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % This function converts amplitude data to power (in dB) -- ie, log power
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     input_array -- data to convert
    %     amp0_or_power1 -- default=1. If the original data are in amplitude,
    %                       to convert to log power you need to square them.
    %                       This flag determines whether or not the values
    %                       are squared
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %      output -- log-power data
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 
    if amp0_or_power1 == 0:
        output = 10*np.log10(input_array**2)
    elif amp0_or_power1 == 1:
        output = 10*np.log10(input_array)
        
    
    return output
    
