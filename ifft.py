import numpy as np 
import scipy as scp
import scipy.signal as signal


def ifft(spectrum,f_or_df):
    """
    % (C) Nick Holschuh - Amherst College -- 2024 (Nick.Holschuh@gmail.com)
    % This function calculates the ifft and the time axis for an input spectrum
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %     spectrum -- the spectrum to take the ifft of
    %     f_or_df -- either the delta f for the record, or the full set of frequencies
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %     f -- the frequency axis for use in plotting
    %     spectrum -- the frequency spectrum
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%
    """

    if len(f_or_df) > 1:
        df = np.nanmedian(np.diff(f_or_df))
    else:
        df = f_or_df

    #samp_freq = (1/dt);
    #df = samp_freq/len(record);
    
    spectrum = scp.fft.ifft(scp.fft.fftshift(spectrum))
    t = scp.fft.fftshift(scp.fft.fftfreq(len(spectrum),df))

    return {'t':t,'series':spectrum}
