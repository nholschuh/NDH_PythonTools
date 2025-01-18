import numpy as np 
import scipy as scp
import scipy.signal as signal


def spectrogram(series,t,window,window_overlap_frac=5,plot_info=0):
    """
    % (C) Nick Holschuh - Amherst College -- 2024 (Nick.Holschuh@gmail.com)
    % This function calculates the spectrogram of an input time series
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
    dt = np.nanmedian(np.diff(t))
    sample_f = 1/dt
    window_overlap = int(window/window_overlap_frac)
    spectrogram_f, spectrogram_t, spec = signal.spectrogram(series, fs=sample_f, nperseg=window, noverlap=window_overlap)
    spec_out = scp.fft.fftshift(spec,axes=0)

    spectrogram_f = np.fft.fftfreq(window, d=dt*2)
    spectrogram_f = scp.fft.fftshift(spectrogram_f,axes=0)

    if plot_info == 1:
        print("plt.figure(figsize=(10,5))")
        print("plt.imshow(np.abs(spec['spectrogram']),extent=[np.min(spec['t']),np.max(spec['t']),")
        print("                                               np.min(spec['f']),np.max(spec['f'])],")
        print("           origin='lower')")
        print("plt.gca().set_aspect('auto')")
        print("plt.xlabel('Time during pulse')")
        print("plt.ylabel('Frequency')")

    return {'f':spectrogram_f,'t':spectrogram_t,'spectrogram':spec_out,'sample_f':sample_f}