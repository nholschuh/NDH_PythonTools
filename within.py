import matplotlib.path as mpltPath
import numpy as np

def within(points,polygon):
    """
    % (C) Nick Holschuh - Amherst College - 2023 (Nick.Holschuh@gmail.com)
    % This function takes a datetime object and converts it to a decimal year
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %    date -- datetime object or list of datetime objects
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    %    date_output -- date as decimal year
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %% https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python
    """    
    path = mpltPath.Path(polygon)
    inside = path.contains_points(points)
    
    return inside