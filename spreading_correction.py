def spreading_correction(flight_elev, twtt, bed_power_dB=[]):
    """
    % (C) Nick Holschuh - Amherst College - 2024 (Nick.Holschuh@gmail.com)
    % This takes in flight elevation and two way travel time values to calculate the 
    % geometric correction for return power. The result is in dB, and should be
    % subtracted from the power value for the observed bed
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    % flight_elev -- 
    % twtt --
    % bed_power_dB -- 
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    % output_dict -- 
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%
    """
    import xarray as xr
    import numpy as np

    ############## Here, we make sure the input objects are the correct type
    if isinstance(flight_elev,type(np.array([]))) == 0:
        if isinstance(flight_elev,list) == 0:
            flight_elev = np.array([flight_elev])
        else:
            flight_elev = np.array(flight_elev)
            
    if isinstance(twtt,type(np.array([]))) == 0:
        if isinstance(twtt,list) == 0:
            twtt = np.array([twtt])
        else:
            twtt = np.array(twtt)   

    if isinstance(bed_power_dB,type(np.array([]))) == 0:
        if isinstance(bed_power_dB,list) == 0:
            bed_power_dB = np.array([bed_power_dB])
        else:
            bed_power_dB = np.array(bed_power_dB) 

    if len(bed_power_dB) == 0:
        bed_power_dB = np.ones(flight_elev.shape)*np.NaN
    
    ############## Load in the pre-calculated spreading corrections
    ##### Built from Matlab 'Generate_SpreadingMatrix.m'
    ##### Converted to NC from 'Develop_spreadingcorrection.ipynb'
    
    spreading_correction_vals = xr.open_dataset('SpreadingCorrection.nc')
    
    x_search = xr.DataArray(flight_elev,dims=['vector_index'])
    y_search = xr.DataArray(twtt,dims=['vector_index'])
    interpolated_values = spreading_correction_vals.interp(flight_elev=x_search,twtt=y_search)
    corrected_bed_power = bed_power_dB+interpolated_values['spreadingloss_raytracing'].values

    return {'raytracing':interpolated_values['spreadingloss_raytracing'].values, 'bogorodsky':interpolated_values['spreadingloss_bogorodsky'].values, 'corrected_bed_power_dB':corrected_bed_power}