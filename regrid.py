import numpy as np
from scipy.interpolate import RegularGridInterpolator
import matplotlib.pyplot as plt
import xarray as xr

class CustomError(Exception):
     pass

def regrid(indata,inx,iny,newx,newy):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This function takes a gridded dataset and redefines it on a new mesh
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %      indata -- the original 2-d data array
    %      inx -- (str) coordinate variable name or array with the original x axis values
    %      iny -- (str) coordinate variable name orarray with the original y axis values
    %      newx -- array with the new x axis
    %      newy -- array with the new y axis
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    %      outdata -- the regridded array
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    ################## Here we do the interpolation via xarray
    if isinstance(indata,type(xr.Dataset({}))):
        try:
            indata = indata.squeeze('band')
        except:
            pass
        
        new_coords = { iny: newy, inx: newx}
        outdata = indata.interp(new_coords, method="linear")

    else:
        ############### Here we decide if we need to flip the input data to make axes increasing --
        ############### (This is important so that we know to re-flip the output before returning)
        dx = inx[1]-inx[0]
        dy = iny[1]-iny[0]
    
        if dx < 0:
            inx = inx[::-1]
            indata = np.fliplr(indata)
            flipx_flag = 1
        else:
            flipx_flag = 0
    
        if dy < 0:
            iny = iny[::-1]
            indata = np.flipud(indata)
            flipy_flag = 1
        else:
            flipy_flag = 0
    
        ############### But we also need to know if we need to flip the comparison grid --
        ############### (This is only important for the regridding step)        
        dx2 = newx[1]-newx[0]
        dy2 = newy[1]-newy[0]
        if dx2 < 0:
            newx = newx[::-1]
        if dy2 < 0:
            newy = newy[::-1]
            
            
        ############## Here is the actual function
        my_interpolater = RegularGridInterpolator((iny,inx),indata,fill_value=-9999,bounds_error=False)
    
        finalx,finaly = np.meshgrid(newx,newy)
    
        try:
            outdata = my_interpolater((finaly,finalx))
        except:
            print('Input Grid (must have values for all output grid: [',np.min(inx),np.max(inx),'],[',np.min(iny),np.max(iny),']')
            print('Output Grid: [',np.min(newx),np.max(newx),'],[',np.min(newy),np.max(newy),']')
            box1x = [np.min(inx),np.max(inx),np.max(inx),np.min(inx),np.min(inx)]
            box1y = [np.max(iny),np.max(iny),np.min(iny),np.min(iny),np.max(iny)]
            box2x = [np.min(newx),np.max(newx),np.max(newx),np.min(newx),np.min(newx)]
            box2y = [np.max(newy),np.max(newy),np.min(newy),np.min(newy),np.max(newy)]
            plt.plot(box1x,box1y,'--',c='black',label='Input Grid')
            plt.plot(box2x,box2y,'-',c='red',label='Output Grid')
            raise CustomError("You have a bounds error for your grids")

        outdata[outdata == -9999] = np.nan
        if flipy_flag == 1:
            outdata = np.flipud(outdata)
            print('flipping y axis')
        if flipx_flag == 1:
            outdata = np.fliplr(outdata)
            print('flipping x axis')
    
    return outdata