import xarray as xr
import numpy as np

def add_datavariable_xr(xarray_dataset,new_datavariable,varname,coordinate_names=['y','x']):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % This function takes an existing xarray dataset and adds a new datavariable
    % to the existing coordinate axes (assumed to be y and x)
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %      xarray_dataset -- the existing xarray dataset to be added to
    %      new_datavariable -- the array containing the new data to be added
    %      varname -- the name for the new datavariable
    %      coordinate_names -- default: ['y','x'], the names and order of 
    %                          coordinate variables to assign to the dimensions
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %      The updated xarray dataset
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """    
    
    coordinate_names = tuple(coordinate_names)
    xarray_dataset = xarray_dataset.assign({varname:(coordinate_names,new_datavariable)})
    
    return xarray_dataset
