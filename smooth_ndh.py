from scipy import signal
import numpy as np

def smooth_ndh(input_array,smooth_window):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % Convolution based smoothing function -- both 1d and 2d
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %    input_array -- The dataset to be smoothed
    %    smooth_window -- an integer value that defines the smoothing window size
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    %    new_data -- the smoothed data
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    if isinstance(smooth_window,int) == 1:
        if len(input_array.shape) == 2:
            smoothing_kernel = np.ones((smooth_window, smooth_window))
        elif len(input_array.shape) == 1:
            smoothing_kernel = np.ones((smooth_window))
            
        smoothing_kernel = smoothing_kernel/np.prod(smoothing_kernel.shape)
    else:
        smoothing_kernel = smooth_window
    
    first_out = signal.fftconvolve(input_array, smoothing_kernel, mode = 'same')
    scalar = signal.fftconvolve(np.ones(input_array.shape), smoothing_kernel, mode = 'same')
    out_data = first_out / scalar;

    
    return out_data