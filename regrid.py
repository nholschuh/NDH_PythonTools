import numpy as np
from scipy.interpolate import RegularGridInterpolator
import matplotlib.pyplot as plt

class CustomError(Exception):
     pass

def regrid(inx,iny,indata,newx,newy):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This function takes a gridded dataset and redefines it on a new mesh
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %      inx -- array with the original x axis values
    %      iny -- array with the original y axis values
    %      indata -- the original 2-d data array
    %      inx -- array with the new x axis
    %      iny -- array with the new y axis
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    %      outdata -- the regridded array
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

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
    my_interpolater = RegularGridInterpolator((iny,inx),indata,fill_value=np.NaN,bounds_error=False)

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

    if flipy_flag == 1:
        outdata = np.flipud(outdata)
        print('flipping y axis')
    if flipx_flag == 1:
        outdata = np.fliplr(outdata)
        print('flipping x axis')
    
    return outdata
    
    ############### This solution would interpolate using bivariate splines (too slow)
    #kx = 3; ky = 3; # spline degree
    #
    #
    #spline = RectBivariateSpline(
    #    inx, iny, indata, kx=kx, ky=ky, s=0
    #)
    #
    #xgrid,ygrid = np.meshgrid(newx,newy)
    #
    ## resample and fill extrapolated points with 0:
    #resampled_data = spline.ev(xgrid, ygrid)
    #extrapol = (((xgrid < inx.min()) | (xgrid >= inx.max())) |
    #            (ygrid < iny.min()) | (ygrid >= iny.max()))
    #resampled_data[extrapol] = 0