import numpy as np

def heading(input_x,input_y):
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
    
    out_angles = np.arctan2(np.diff(input_y),np.diff(input_x))
    out_angles = np.concatenate([np.array([out_angles[0]]),out_angles])
    return out_angles
