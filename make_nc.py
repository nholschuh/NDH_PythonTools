import xarray as xr
import numpy as np

def make_nc(input_x,input_y,input_vars,input_varnames,filename='temp.nc',description='No description provided',writefile0_or_dataset1_or_both2 = 1):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % This function uses xarray to construct a netcdf
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     input_x,
    %    input_y,
    %    input_vars,
    %    input_varnames,
    %    filename='temp.nc',
    %    description='No description provided',
    %    writefile0_or_dataset1 = 1
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %      output -- the min and max in a 1x2 array
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """    
    data_dict = {}
    if input_vars.ndim == 2:
        data_dict[input_varnames[0]] = (['y','x'],input_vars)
    else:
        for ind1,i in enumerate(input_varnames):
            data_dict[i] = (['y','x'],input_vars[:,:,ind1])
            
    coord_dict = {'x':(['x'],input_x),'y':(['y'],input_y)}
    
    ds = xr.Dataset(
        data_vars=data_dict,
        coords=coord_dict,
        attrs=dict(description=description),
    )
    
    if writefile0_or_dataset1_or_both2 == 0:
        ds.to_netcdf(path=filename)
    elif writefile0_or_dataset1_or_both2 == 2:
        ds.to_netcdf(path=filename)
        return ds
    else:
        return ds