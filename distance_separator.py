import numpy as np

import sys
sys.path.append('/mnt/data01/Code/')
from NDH_Tools import distance_vector
from NDH_Tools import list_separator

def distance_separator(in_x,in_y,distance_sep,output_type=0):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This function takes x and y coordinates in an array and finds where
    % the line should be separated into separate segments based off a given
    % distance threshold
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    % in_x - x_coordinates for your input array
    % in_y - y_coordinates for your input array
    % distance_sep - the threshold distance used to add NaNs into the array
    %                (defining separate segments)
    % output_type=0 -- this sets whether or not you want a single array with
    %                  nan separators, or a list of segments (1)
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The function returns the following objects:
    %
    % out_x - the new array of x_values that contains NaNs as separators
    % out_y - the new array of y_values that contains NaNs as separators
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%
    """

    if isinstance(in_x,type([])):
        in_x = np.array(in_x)

    try:
        if in_y == 0:
            in_y = np.zeros(in_x.shape)
    except:
        pass
        
    if isinstance(in_y,type([])):
        in_y = np.array(in_y)
    
    dists = distance_vector(in_x,in_y,1)
    naninds = np.where(dists > distance_sep)[0]+1
    if len(naninds) == 0:
        ind_adjust = np.zeros(len(dists))
    else:
        if np.max(naninds) > len(dists)-1:
            naninds = naninds[:-1]
    
        ind_adjust = np.zeros(len(dists))
        ind_adjust[naninds] = 1
        ind_adjust = np.cumsum(ind_adjust)

    if output_type == 0:
        out_xy = np.ones([len(dists)+len(naninds),3])*np.NaN
    
        orig_ind = np.arange(0,len(in_x))
        orig_ind = orig_ind+ind_adjust
        orig_ind = orig_ind.astype(int)
    
        out_xy[orig_ind,0] = in_x
        out_xy[orig_ind,1] = in_y

    elif output_type == 1:
        out_xy = []
        for ind0 in np.unique(ind_adjust):
            ki = np.where(ind_adjust == ind0)[0]
            out_xy.append(np.stack([in_x[ki],in_y[ki],ki]).T)
    
    return out_xy
        
    
        
    
    
