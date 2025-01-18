import astropy.time
import numpy as np

def gps_timeconvert(gpstime,startime=-315964800):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    % This function converts ICESat-2 times to decimal year values
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     gpstime -- The deltatime value from an ATL06 or ATL11 file
    %     starttime -- This is a deltatime value assuming a 1970 reference fram
    %                  (true for CReSIS data). Adjust to 0 for a time relative to 01/05/1980
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %      This function will output those time values as decimal years
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    xover_t = astropy.time.Time(startime+gpstime,format='gps')
    output = xover_t.byear
    
    return output