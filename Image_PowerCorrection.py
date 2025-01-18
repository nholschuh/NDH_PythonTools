
import xarray as xr
import numpy as np

def Image_PowerCorrection(radar_image,flight_elev,depth_axis,attenuation_val,attenuation_type):
    """
    % (C) Nick Holschuh - Amherst College - 2024 (Nick.Holschuh@gmail.com)
    % This function, applied to a depth_shifted image, applies a depth_power
    % correction that allows you to interpret relative reflectivity within the ice column
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %     radar_image -- The depth_shifted (not elevation shifted) image
    %     flight_elev -- The elevation of the plane relative to the ice surface (in m)
    %     depth_axis -- The z axis associated with the depth_shifted image
    %     attenuation_val -- Attenuation in db/km
    %     attenuation_type -- 0: 1 wawy attenuation rate, (multiplied by range)
    %                         1: two way attenuation rate, (multiplied by depth)
    %                         2: nx2 array with depths and attenuation rate values
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %     power_corrected_radarim -- radar image (in dB) corrected for spreading and attenuation
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %% e.g.:
    radar_image = depth_data['new_data']
    flight_elev = radar_data['Elevation']
    depth_axis = depth_data['depth_axis']
    attenuation_val = 8.0
    attenuation_type = 0
    """
    
    ################ This is the import statement required to reference scripts within the package
    import os,sys,glob
    ndh_tools_path_opts = [
        '/mnt/data01/Code/',
        '/home/common/HolschuhLab/Code/'
    ]
    for i in ndh_tools_path_opts:
        if os.path.isdir(i): sys.path.append(i); correction_root_dir=i;
    ################################################################################################
    
    ############## Load in the pre-calculated spreading corrections
    ##### Built from Matlab 'Generate_SpreadingMatrix.m'
    ##### Converted to NC from 'Develop_spreadingcorrection.ipynb'
    
    spreading_correction_vals = xr.open_dataset(correction_root_dir+'NDH_Tools/SpreadingCorrection.nc')

    ############## Construct a synthetic twtt for the depth_image
    cair = 299792458 
    cice = 1.68e8
    dz = np.mean(np.diff(depth_axis))
    imdims = radar_image.shape
    depth_image = np.cumsum(np.ones(imdims),axis=0)*dz
    twtt_image = depth_image*2/cice+flight_elev*2/cair
    elev_image = np.zeros(imdims)+flight_elev
    x_search = xr.DataArray(elev_image.ravel(),dims=['vector_index'])
    y_search = xr.DataArray(twtt_image.ravel(),dims=['vector_index'])
    spreading_losses = spreading_correction_vals.interp(flight_elev=x_search,twtt=y_search)
    spreading_losses = spreading_losses['spreadingloss_raytracing'].values.reshape(imdims)

    ######### One way attenuation Rate
    if attenuation_type == 0:
        attenuation_losses = depth_image*2*np.abs(attenuation_val)/1000

    ######### Two way attenuation Rate
    elif attenuation_type == 1:
        attenuation_losses = depth_image*np.abs(attenuation_val)/1000

    ######### Attenuation profile (assumes two way)
    elif attenuation_type == 2:
        attenuation_val = np.interp1(attenuation_val[:,0],np.abs(attenuation_val[:,1]),depth_axis)
        attenuation_val = np.zeros(imdims)+attenuation_val
        attenuation_losses = np.cumsum(attenuation_val,axis=0)*1000*2       

    power_corrected_radarim = 10*np.log10(radar_image)-spreading_losses+attenuation_losses

    return {'corrected_im':power_corrected_radarim, 'spreading_correction':spreading_losses, 'attenuation_correction':attenuation_losses}