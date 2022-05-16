import numpy as np

def interpNaN(y):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    % Fills in NaN values using a linear interpolator
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    % y -- 1d numpy array with possible NaNs
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    % y -- 1d numpy array with the NaNs replaced by interpolated values
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %% Following: https://stackoverflow.com/questions/6518811/interpolate-nan-values-in-a-numpy-array
    """

    if isinstance(y,type(np.array([]))) == 0:
        if isinstance(y,type([])):
            y = np.array(y)
        else:
            y = np.array([y])
        
        
    nans = np.isnan(y)
    x = lambda z: z.nonzero()[0]
    y[nans] = np.interp(x(nans), x(~nans), y[~nans])
    return y