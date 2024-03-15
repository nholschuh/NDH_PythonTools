import numpy as np

def rotate_to_axis(x,y):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This function rounds a value to a given spacing / order of magnitude
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %    data_to_round -- the array that you want to collapse onto the new spacing
    %    spacing -- the gap between sequential values
    %    shift -- the offset from 0 to round to
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    %    new_data -- the values of the original array, rounded to their target
    %    data_inds -- the number of steps away from the lowest value, using the given spacing
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """


    xmin = np.min(x)
    xmax = np.max(x)
    ymin = np.min(y)
    ymax = np.max(y)

    dx = xmax-xmin
    dy = ymax-ymin
    theta = np.arctan(dy/dx)
    
    unrotate_mat = np.array([[np.cos(-theta),-np.sin(-theta)],[np.sin(-theta),np.cos(-theta)]])
    new_xy = np.matmul(np.stack([x,y]).T,unrotate_mat)
    new_x = new_xy[:,0]
    new_y = new_xy[:,1]

    return new_x,new_y