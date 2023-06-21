def remove_arrow(input_axisObject,num=1):
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
    
    for i in range(num):
        try:
            input_axisObject.patches.pop(-1)
        except:
            print('Couldn''t remove image')