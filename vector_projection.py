import numpy as np

def vector_projection(input_xvec,input_yvec,projectiontarget_xvec,projectiontarget_yvec):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %    input_xvec -- x components of the vectors you want to reproject
    %    input_yvec -- y components of the vectors you want to reproject
    %    projectiontarget_xvec -- x components of the vectors you want to project the input onto
    %    projectiontarget_yvec -- y components of the vectors you want to project the input onto
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    %    reproj_x -- the x component of input_vec projected onto projectiontarget
    %    reproj_y -- the y component of input_vec projected onto projectiontarget
    %    reproj_mag -- the magnitude of the reprojected vector
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    # a dot b / mag(b) -- projection of a onto b

    proj_mag = np.sqrt(projectiontarget_xvec**2+projectiontarget_yvec**2)
    proj_dir_x = projectiontarget_xvec/proj_mag
    proj_dir_y = projectiontarget_yvec/proj_mag

    reproj_mag = input_xvec*proj_dir_x+input_yvec*proj_dir_y
    reproj_x = proj_dir_x*reproj_mag
    reproj_y = proj_dir_y*reproj_mag

    return reproj_x,reproj_y,reproj_mag