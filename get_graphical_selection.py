import numpy as np
import matplotlib.pyplot as plt

def get_graphical_selection(points_object):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This will read the structure of a dwg / dxf file and exctract the layer names
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    % points_object -- This is the output of graphical selection
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    % outdata -- a dictionary containing the x and y values of the selected points
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %% --- applied to the output of graphical_selection(points_object)
        
    """

    
    if 'meta_ndh' in points_object[0].__dict__.keys():
        outdata = {'x':points_object[0].get_xdata(), 'y':points_object[0].get_ydata(), 'meta':points_object[0].__dict__['meta_ndh']}
    else:
        outdata = {'x':points_object[0].get_xdata(), 'y':points_object[0].get_ydata()}

    return outdata
