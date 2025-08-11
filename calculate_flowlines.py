import numpy as np
import matplotlib.pyplot as plt
import tqdm
import xarray as xr
import os

def calculate_flowlines(input_xr,seed_points,uv_varnames=['u','v'],xy_varnames=['x','y'],steps=20000,ds=2,forward0_both1_backward2=1):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % This function takes a vector field described in an xarray dataset, an
    % array of points, and calculates flowlines that pass through the array
    % points following the vector field.
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     input_xr -- this must be an xarray dataset with two dataarrays, represting
    %                 the x components and the y components of a vector field. The data
    %                 variables and the coordinate variables that describe them can have
    %                 any name, but the defaults are 'u','v','x','y'.
    %     seed_points -- this should be an nx2 array containing x/y pairs for seed points
    %                    used to constrain the calculated flowlines
    %     uv_varnames -- default=['u','v'], these are the datavariable names for the
    %                    vector field components.
    %     xy_varnames -- default=['x','y'], these are the coordinate variable names 
    %                    describing the columns and rows of the vector field arrays
    %     steps -- default=20000, this is the number of steps to take away from the seed
    %               in either the forward or backward direction
    %     ds -- default=2, this is the step-size to take when propagating the flowline away
    %           from the seedpoint (in the same units as the coordinate variables
    %     forward0_both1_backward2 -- default=1, this sets whether or not you want 
    %                                 the flowlines to extend down-vector, up-vector, or
    %                                 both from the seed point.
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %      output -- a list of nx2 arrays containing the flowlines associated with
    %                each seed point
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 

    ##################### Here, we standardize the naming convention within the xarray object
    input_xr = input_xr.rename({xy_varnames[0]:'x',xy_varnames[1]:'y'})
    uv_scalar = np.sqrt(input_xr[uv_varnames[0]].values**2 + input_xr[uv_varnames[1]].values**2)
    input_xr[uv_varnames[0]] = (('y','x'),input_xr[uv_varnames[0]].values/uv_scalar)
    input_xr[uv_varnames[1]] = (('y','x'),input_xr[uv_varnames[1]].values/uv_scalar)


    #################### We initialize the objects for the flowline calculation
    flowlines = []

    #################### Here is the forward calculation
    if forward0_both1_backward2 <= 1:
        temp_xs = np.expand_dims(seed_points[:,0],0)
        temp_ys = np.expand_dims(seed_points[:,1],0)

        for ind0 in tqdm.tqdm(np.arange(steps)):
            x_search = xr.DataArray(temp_xs[-1,:],dims=['vector_index'])
            y_search = xr.DataArray(temp_ys[-1,:],dims=['vector_index'])
            new_u = input_xr[uv_varnames[0]].sel(x=x_search,y=y_search,method='nearest')
            new_v = input_xr[uv_varnames[1]].sel(x=x_search,y=y_search,method='nearest')

            ######### This is an order of magnitude slower
            #new_u = input_xr[uv_varnames[0]].interp(x=x_search,y=y_search)
            #new_v = input_xr[uv_varnames[1]].interp(x=x_search,y=y_search)

            temp_xs = np.concatenate([temp_xs,temp_xs[-1:,:]+new_u.values.T*ds])
            temp_ys = np.concatenate([temp_ys,temp_ys[-1:,:]+new_v.values.T*ds])

        xs = temp_xs
        ys = temp_ys
    else:
        xs = np.empty([0,len(seed_points)])
        ys = np.empty([0,len(seed_points)])


    #################### Here is the backward calculation
    if forward0_both1_backward2 >= 1:
        temp_xs = np.expand_dims(seed_points[:,0],0)
        temp_ys = np.expand_dims(seed_points[:,1],0)

        for ind0 in tqdm.tqdm(np.arange(steps)):
            x_search = xr.DataArray(temp_xs[-1,:],dims=['vector_index'])
            y_search = xr.DataArray(temp_ys[-1,:],dims=['vector_index'])
            new_u = input_xr[uv_varnames[0]].sel(x=x_search,y=y_search,method='nearest')
            new_v = input_xr[uv_varnames[1]].sel(x=x_search,y=y_search,method='nearest')

            ######### This is an order of magnitude slower
            #new_u = input_xr[uv_varnames[0]].interp(x=x_search,y=y_search)
            #new_v = input_xr[uv_varnames[1]].interp(x=x_search,y=y_search)

            temp_xs = np.concatenate([temp_xs,temp_xs[-1:,:]-new_u.values.T*ds])
            temp_ys = np.concatenate([temp_ys,temp_ys[-1:,:]-new_v.values.T*ds])

        xs = np.concatenate([np.flipud(temp_xs),xs])
        ys = np.concatenate([np.flipud(temp_ys),ys])  



    flowlines = []
    for ind0 in np.arange(len(xs[0,:])):
        xy = np.stack([xs[:,ind0],ys[:,ind0]]).T
        flowlines.append(xy)
        
    return flowlines
