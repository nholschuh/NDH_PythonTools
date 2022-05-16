import numpy as np
from scipy.interpolate import RegularGridInterpolator

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

    ############## Here is the actual function
    my_interpolater = RegularGridInterpolator((iny,inx),indata)

    finalx,finaly = np.meshgrid(newx,newy)

    outdata = my_interpolater((finaly,finalx))

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