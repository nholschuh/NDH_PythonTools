import xarray as xr
import numpy as np

def make_nc(input_x,input_y,input_vars,input_varnames,num_dims=0,filename='temp.nc',description='No description provided',coord_vars=['x','y'],writefile0_or_dataset1_or_both2 = 1):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % This function uses xarray to construct a netcdf
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %    input_x - This should be the x coordinate variable array, corresponding to columns
    %    input_y - This should be the y coordinate variable array, corresponding to roes
    %    input_vars - This should be a list of datavariable arrays, of shape (leny,lenx)
    %    input_varnames - This should be a list of variable names to attribute to input_vars
    %    filename='temp.nc' - This is the name of the netcdf to write
    %    description='No description provided' - A description to go in netcdf metadata
    %    coord_vars=List of names for x coord and y coord, defaults to ['x','y']
    %    writefile0_or_dataset1_or_both2 = 1 - This determines whether or not it will write
    %                                          out a netcdf or just make the xarray dataset
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %    output -- the xarray dataset, if writefile0_or_dataset1_or_both2 > 0
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """    
    data_dict = {}    
    
    if isinstance(input_varnames,str) == 1:
        input_varnames = [input_varnames]
    
    if isinstance(input_vars,list) == 1:
        input_vars = np.array(input_vars)
        if input_vars.ndim == 3:
            input_vars = np.moveaxis(input_vars,[0,1,2],[2,0,1])
    
    
    ######## This is the default case, where the code tries to determine the
    ######## number of dimensions of the variable fields
    if num_dims == 0:
        
        if input_vars.ndim == 1:
            data_dict[input_varnames[0]] = ([coord_vars[0]],input_vars)
            coord_dict = {coord_vars[0]:([coord_vars[0]],input_x)}
        elif input_vars.ndim == 2:
            data_dict[input_varnames[0]] = ([coord_vars[1],coord_vars[0]],input_vars)
            coord_dict = {coord_vars[0]:([coord_vars[0]],input_x),coord_vars[1]:([coord_vars[1]],input_y)}
        
        ####### If there is more than one variable provided, then it assumes that
        ####### the variable data has been provided as a 3D array, with the 
        ####### third dimension defining each variable
        else:
            for ind1,i in enumerate(input_varnames):
                data_dict[i] = ([coord_vars[1],coord_vars[0]],input_vars[:,:,ind1])
            coord_dict = {coord_vars[0]:([coord_vars[0]],input_x),coord_vars[1]:([coord_vars[1]],input_y)}
            
    ######## Here we handle the case where you specify 1D data but provide
    ######## multiple data variables
    if num_dims == 1:
        for ind1,i in enumerate(input_varnames):
            data_dict[i] = ([coord_vars[0]],input_vars[ind1])
        coord_dict = {coord_vars[0]:([coord_vars[0]],input_x)}
        
    if num_dims == 2:
        if input_vars.ndim == 2:
            data_dict[input_varnames[0]] = ([coord_vars[1],coord_vars[0]],input_vars)
            coord_dict = {coord_vars[0]:([coord_vars[0]],input_x),coord_vars[1]:([coord_vars[1]],input_y)}
        else:
            for ind1,i in enumerate(input_varnames):
                data_dict[i] = ([coord_vars[1],coord_vars[0]],input_vars[:,:,ind1])
            coord_dict = {coord_vars[0]:([coord_vars[0]],input_x),coord_vars[1]:([coord_vars[1]],input_y)}
    
    ######## Here is where the netcdf actually gets written
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