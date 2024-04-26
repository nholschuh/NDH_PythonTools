import matplotlib

def cmap_data(colormapname):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % This function gets the colormap object from matplotlib for value extraction
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     colormapname -- the string for the colormap of choice
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %      cmap -- The colormap object, which takes values from 0-1 to generate a color.
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 
    cmap = matplotlib.cm.get_cmap(colormapname)
    
    return cmap
    
