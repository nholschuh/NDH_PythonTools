import numpy as np
import tqdm


def delay_doppler(radar_data, window_size=150, target_ind=0, ind_spacing=50, spacing_ind0_or_dist1=1, deg0_or_rad1=0, return_fft=1, airborne0_or_groundbased1=0, center_freq=0):
    """
    % (C) Peter Klisewicz - Amherst College - 2025
    %     Nick Holschuh - Amherst College - 2025 (Nick.Holschuh@gmail.com)
    % This function uses a complex radar image and computes the delay-doppler spectrum
    % from the data. 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %      radar_data - original radar data loaded with ndh.radar_load
    %      target ind - A specific index in the radar image. If 0, calculate over a rolling window
    %      window_size - The number of samples to include in the fft
    %      deg 
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    c = 299792458
    perm=3.15

    distance = radar_data['distance']
    dist_step = np.median(np.diff(distance))
    radar_image = radar_data['Data']

    if center_freq == 0:
        try:
            system_center_f = radar_data['param_sar']
            try:
                system_center_f = system_center_f['radar']['wfs'][0]['fc']
                print('Center Frequency:',system_center_f)
            except:
                raise ValueError("The parameter structure you've provided didn't have the center frequency in the expected location.")
        except:
            try:
                system_center_f = radar_data['param_qlook']
                try:
                    system_center_f = system_center_f['radar']['wfs'][0]['fc']
                    print('Center Frequency:',system_center_f)
                except:
                    raise ValueError("The parameter structure you've provided didn't have the center frequency in the expected location.")
            except:
                try:
                    system_center_f = radar_data['param_array']
                    try:
                        system_center_f = system_center_f['radar']['wfs'][0]['fc']
                        print('Center Frequency:',system_center_f)
                    except:
                        raise ValueError("The parameter structure you've provided didn't have the center frequency in the expected location.")
                except:
                    try:
                        fs = []
                        for ind0,param in enumerate(radar_data['param_radar'][()]):
                            if isinstance(param,type(np.ndarray([]))):
                                for ind1,subparam in enumerate(param):
                                    if isinstance(subparam,int):
                                        if np.all([subparam > 5e7, subparam < 2e9]):
                                            fs.append(subparam)
                                    
                                    for ind2,subparam2 in enumerate(subparam):
                                        if isinstance(subparam2,int):
                                            if np.all([subparam2 > 5e7, subparam2 < 2e9]):
                                                fs.append(subparam2)
                        fs = np.unique(fs)
                        system_center_f = np.mean(fs)
                        print('Center Frequency:',system_center_f)
                                   
                    except:
                        raise ValueError('Can\'t find the right parameter structure in the file.')
    else:
        system_center_f = center_freq

    if spacing_ind0_or_dist1 == 1:
        ind_spacing = int(ind_spacing/dist_step)
    
    if target_ind == 0:
        target_inds = np.arange(0,len(distance),ind_spacing).astype(int)
    else:
        target_inds = [target_ind]

    #GET SPACIAL SEPARATION BETWEEN OBSERVATIONS
    ind_window = int(window_size/dist_step/2)

    ki = np.where(np.all([target_inds > ind_window, target_inds < len(distance)-ind_window],axis=0))[0]
    
    slopes = np.zeros([len(radar_image[:,0]),len(ki)])
    if return_fft == 1:
        at_volume = np.zeros([len(ki),len(radar_image[:,0]),2*ind_window])
    else:
        at_volume = []

    
    for ind0,target_ind in enumerate(tqdm.tqdm(target_inds[ki])):
        #GET INDICES TO ANALYZE
        track_lower_ind = target_ind-ind_window
        track_higher_ind = target_ind+ind_window
        if ind0 == 0:
            wavenum = np.fft.fftfreq(track_higher_ind - track_lower_ind, d=dist_step)
            wavenum = np.fft.fftshift(wavenum)
            wavenum_axis = wavenum
            dx_axis = wavenum*system_center_f/c
            slope_axis = np.arcsin(dx_axis)
            
    
    
        ### PERFORM FFT
        fft = np.fft.fft(radar_image[:,track_lower_ind:track_higher_ind], axis=1)
        fft = np.fft.fftshift(fft, axes=1)
        fft_dB = 10*np.log10(abs(fft)**2)
    
        ### DETERMINE WAVENUMS FOR FFT
        angl_wavenum = 2*np.pi*wavenum
    
        ### SELECT MAX WAVENUMS
        max_inds = np.argmax(fft_dB, axis=1)
        max_array = np.zeros_like(fft_dB, 'float64')
        max_array[np.arange(fft_dB.shape[0]), max_inds] = 1
    
        ### CALCULATE SLOPE FROM WAVENUM
        delt_delx = wavenum[max_inds]*system_center_f/c
        slope = np.arcsin(delt_delx)

        if return_fft == 1:
            at_volume[ind0,:,:] = fft_dB
        slopes[:,ind0] = slope
        
    if deg0_or_rad1 == 0:
        slopes = slopes*360/(2*np.pi)
        slope_axis = slope_axis*360/(2*np.pi)

    data_pi = target_inds[ki]
    
    return {'distance':distance[data_pi], 'doppler_data':at_volume ,'slopes': slopes, 'slope_axis': slope_axis, 'wavenumber_axis': wavenum_axis, 'Time':radar_data['Time'],'x':radar_data['x'][data_pi],'y':radar_data['y'][data_pi],'Surface':radar_data['Surface'][data_pi],'Bottom':radar_data['Bottom'][data_pi]}



    