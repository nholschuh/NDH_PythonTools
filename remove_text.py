def remove_text(input_axisObject,num=1,verbose=1):
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
    for text in input_axisObject.texts[0:num]:
        try:
            text.remove()
        except:
            if verbose == 1:
                print('Couldn''t remove line')
            else:
                pass 