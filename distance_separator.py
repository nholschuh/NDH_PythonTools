import numpy as np

import sys
sys.path.append('/mnt/data01/Code/')
from NDH_Tools import distance_vector
from NDH_Tools import list_separator

def distance_separator(in_x,in_y,distance_sep):
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

    
    dists = distance_vector(in_x,in_y,1)
    naninds = np.where(dists > distance_sep)[0]+1
    
    in_x_sep = list_separator(in_x,naninds)
    in_y_sep = list_separator(in_y,naninds)
    
    out_x = np.array([])
    out_y = np.array([])
    for i in in_x_sep:
        out_x = np.concatenate([out_x,i,np.atleast_1d(np.NaN)])
    for i in in_y_sep:
        out_y = np.concatenate([out_y,i,np.atleast_1d(np.NaN)])
    
    return out_x, out_y
    
    
