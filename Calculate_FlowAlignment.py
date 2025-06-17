################ This is the import statement required to reference scripts within the package
import os,sys,glob
ndh_tools_path_opts = [
    '/mnt/data01/Code/',
    '/home/common/HolschuhLab/Code/'
]
for i in ndh_tools_path_opts:
    if os.path.isfile(i): sys.path.append(i)
################################################################################################

import xarray as xr
import NDH_Tools as ndh
import numpy as np


def Calculate_FlowAlignment(profile_xy,velocity_xr, threshold = np.pi/18):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % This function takes a profile and a vector field and determines their alignment    
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %    profile_xy - an nx2 vector with x and y coordinates for the line to analayze
    %    velocity_xr - xarray dataset with 'u' and 'v' variables for vector comparison
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %    angle_out - angle (between 0 and pi/2) descriibing the angle between the vector field and profile
    %    below_thresh - boolean describing those points on profile whose angle falls under the threshold
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """     
    x_search = xr.DataArray(profile_xy[:,0],dims=['vector_index'])
    y_search = xr.DataArray(profile_xy[:,1],dims=['vector_index'])
    interpolated_values = velocity_xr.interp(x=x_search,y=y_search)
    path_dx = np.concatenate([np.array([0]),np.diff(profile_xy[:,0])])
    path_dy =np.concatenate([np.array([0]),np.diff(profile_xy[:,1])])
    vel_dx = interpolated_values['u'].values
    vel_dy = interpolated_values['v'].values

    path_scalar = np.sqrt(path_dx**2+path_dy**2)
    vel_scalar = np.sqrt(vel_dx**2+vel_dy**2)

    proj_x,projy,mag=ndh.vector_projection(path_dx/path_scalar,path_dy/path_scalar,vel_dx/vel_scalar,vel_dy/vel_scalar)
    angle_out = np.arccos(mag)
    below_thresh = angle_out < threshold

    return {'angle':angle_out, 'threshold_met':below_thresh}


