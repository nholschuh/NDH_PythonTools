import sys
sys.path.append('/mnt/data01/Code/')

def flatten_list(list_of_lists,recursive_flag=1,nan_divide=0):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This will take a list of lists (or an array of arrays) and flattens
    % them to just an array of the items). There may also be a method on lists
    % called "flatten" which does this too, but this version handles subordinate
    % arrays that might also be within the list.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    % flatten_list -- The list of lists to be flattened
    % recursive_flag -- This will keep flattening until the list stops changing
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
    
    if nan_divide == 1:
        new_list_of_lists = []
        for i in list_of_lists:
            new_list_of_lists.append(i)
            new_list_of_lists.append([np.nan])
        list_of_lists = new_list_of_lists[:-1]
    
    
    flat_list = []
    array_flag = 0
    steps = 0
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

        flat_list = list(np.array(flat_list))
        
        ######### Here we test if the lists are truly identical
        comb_result,r1,r2 = compare_list(flat_list,flat_list_check)

        if comb_result:
            recursive_flag = 0
        if recursive_flag == 0:
            recursive_flag = 0
            
        ############ nan's present in the ojbect break the list comparison.
        ############ so we force it to short circuit after 5 steps
        if steps > 5:
            recursive_flag = 0
        
        if recursive_flag == 1:
            flat_list_check = flat_list.copy()
            list_of_lists = flat_list.copy()
            flat_list = []
        
        steps = steps+1
        #print(steps)
    
    return flat_list
