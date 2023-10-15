def remove_axis_ticks(input_axisObject=[]):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This function removes contours (but I don't remember why I needed this)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %      input_axisObject - axis object to remove to remove the most recent line or lines
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
    import matplotlib.pyplot as plt
    
    if isinstance(input_axisObject,list):
        input_axisObject = plt.gca()
    
    plt.tick_params(left = False, right = False , labelleft = False ,
                    labelbottom = False, bottom = False)