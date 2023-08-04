def set_axis_size(w,h, ax=None):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This function resizes a figure such that the axes are a specific size (in in)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %     w, h: width, height in inches 
    %     ax: the specific axis (if nothing provided, defaults to current axis)
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Solution from https://stackoverflow.com/questions/64786033/add-axes-to-a-figure-with-a-fixed-size
    """
    import matplotlib.pyplot as plt
    
    if not ax: 
        ax=plt.gca()
        l = ax.figure.subplotpars.left
        r = ax.figure.subplotpars.right
        t = ax.figure.subplotpars.top
        b = ax.figure.subplotpars.bottom
        figw = float(w)/(r-l)
        figh = float(h)/(t-b)
        ax.figure.set_size_inches(figw, figh)