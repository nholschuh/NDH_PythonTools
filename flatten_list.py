import sys
sys.path.append('/mnt/data01/Code/')

def flatten_list(list_of_lists,recursive=1):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This will take a list of lists (or an array of arrays) and flattens
    % them to just an array of the items)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    % flatten_list -- The list of lists to be flattened
    % recursive -- This will keep flattening until the list stops changing
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
    from NDH_Tools import compare_list
    
    flat_list = []
    array_flag = 0
    recursive_flag = 1
    flat_list_check = list_of_lists.copy()
    
    while recursive_flag == 1:
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

<<<<<<< HEAD
    flat_list = list(np.array(flat_list))
    
    return flat_list
=======
        flat_list = list(np.array(flat_list))
        
        ######### Here we test if the lists are truly identical
        comb_result,r1,r2 = compare_list(flat_list,flat_list_check)

        if comb_result:
            recursive_flag = 0
        if recursive == 0:
            recursive_flag = 0
        
        if recursive_flag == 1:
            flat_list_check = flat_list.copy()
            list_of_lists = flat_list.copy()
            flat_list = []
        
    
    return flat_list
>>>>>>> 7b10ea1e311406c85920d0fdcab9dfc68c118710
