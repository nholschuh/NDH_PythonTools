import astropy.time
import numpy as np

def is2_timeconvert(ATL06_deltat):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    % This function converts ICESat-2 times to decimal year values
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     ATL06_deltat -- The deltatime value from an ATL06 or ATL11 file
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %      This function will output those time values as decimal years
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    dt_scaler=1.198800018000000e+09
    xover_t = astropy.time.Time(dt_scaler+ATL06_deltat,format='gps')
    output = xover_t.byear
    
    return output