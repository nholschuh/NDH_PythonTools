import numpy as np 
import scipy as scp
import scipy.signal as signal
from collections.abc import Iterable


def fft(record,t_or_dt):
    """
    % (C) Nick Holschuh - Amherst College -- 2024 (Nick.Holschuh@gmail.com)
    % This function calculates the fft and the frequency axis for an input record
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %     record -- the timeseries to take the fft of
    %     t_or_dt -- either the delta time for the record, or the full set of times
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %     f -- the frequency axis for use in plotting
    %     spectrum -- the frequency spectrum
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%
    """

    if isinstance(t_or_dt,Iterable) == 0:
        dt = t_or_dt
    else:
        if len(t_or_dt) > 1:
            dt = np.nanmedian(np.diff(t_or_dt))
        else:
            dt = t_or_dt

    apply_window = 0
    if apply_window == 1:
        max_window_size = 100
        if len(record) < max_window_size:
            window = np.hanning(len(record))
        else:
            window = np.ones(record.shape)
            mid_index = int(max_window_size/2+1)
            hw = np.hanning(max_window_size)
            
            window[0:mid_index] = hw[:mid_index]
            window[-mid_index:] = hw[-mid_index:]
        record = record * window
        
    spectrum = scp.fft.fftshift(scp.fft.fft(record))
    f = scp.fft.fftshift(scp.fft.fftfreq(len(record),dt))

    return {'f':f,'spectrum':spectrum}

