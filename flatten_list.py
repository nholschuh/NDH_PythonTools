def flatten_list(list_of_lists):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This will take a list of lists (or an array of arrays) and flattens
    % them to just an array of the items)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    % flatten_list -- The list of lists to be flattened
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    % flat_list -- The flattened list (output as an array)
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%
    """

    import numpy as np
    
    flat_list = []
    array_flag = 0
    for sublist in list_of_lists:
        if isinstance(sublist,type([])):
            for item in sublist:
                flat_list.append(item)
        elif isinstance(sublist,type(np.array([]))):
            array_flag = 1
            for item in sublist:
                flat_list.append(item)            
        else:
            flat_list.append(sublist)

    flat_list = list(np.array(flat_list))
    
    return flat_list
