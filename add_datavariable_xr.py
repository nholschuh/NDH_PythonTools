import xarray as xr
import numpy as np

def add_datavariable_xr(xarray_dataset,new_datavariable,varname,coordinate_names=['y','x']):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % This function uses xarray to construct a netcdf
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """    
    
    coordinate_names = tuple(coordinate_names)
    xarray_dataset = xarray_dataset.assign({varname:(coordinate_names,new_datavariable)})
    
    return xarray_dataset
