import numpy as np

def distance_vector(x,y,total0_or_increment1=0):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This function takes in x and y coordinates and calculates either the
    % cumulative distance along the line or the incremental distance between
    % points.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    % x - x_coordinates for your input array
    % y - y_coordinates for your input array
    % total0_or_increment1 - the cumulative distance [0] or the incremental
    %                       distance (1). If you select (1), the last distance
    %                       value is assumed to be == the second to last value.
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The function returns the following objects:
    %
    % distvec - your array of distances, the same length as the input vector
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%
    """

    if 'total0_or_increment1' not in locals():
        total0_or_increment1 = 0

    if 'y' not in locals():
        y = np.zeros(len(x));


    distvec = np.zeros(len(x))
    dists = np.sqrt(np.diff(x)**2+np.diff(y)**2)
    
    if total0_or_increment1 == 0:
        distvec[1:] = np.cumsum(dists)
    else:
        distvec[:-1] = dists
        distvec[-1] = distvec[-2]
        
    return distvec
