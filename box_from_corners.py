import numpy as np

def box_from_corners(xs,ys):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % This function takes x and y edge values for a rectangle, and produces a
    % 5x2 array of corner points that trace out the rectangle (for use in plotting)
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     xs - 2 value array contaiining the x edges of the rectangle
    %     ys - 2 value array contaiining the y edges of the rectangle
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %      box -- the 5x2 array containing the corner points for the rectangle
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 
    x_array = np.array([xs[0],xs[1],xs[1],xs[0],xs[0]])
    y_array = np.array([ys[1],ys[1],ys[0],ys[0],ys[1]])
    
    box = np.stack([x_array,y_array]).T
        
    return box
    
