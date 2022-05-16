def remove_key(d,key_to_remove,name0_value1_type2_length3,remove_count=0):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This function removes keys from a dictionary based on a search criterion
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %        d -- dictionary to filter
    %        key_to_remove -- This can be a string, a value, a type, or an integer, depending on the value of the next argument
    %        name0_value1_type2_length3 -- This allows you to filter based on the name of a key, the value associated with that key, 
    %                                       the type of value, or the length of the value. Keys/Values that match "key_to_remove" are removed
    %        remove_count=0 -- This should not be set by the user, but is required for the recursive code. This allows groups that are
    %                           emptied to, themselves, be removed, when using length == 0 as the criterion.
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    %       new_dict -- dictionary with the removed keys
    %       remove_count -- the number of entries removed
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    new_dict = {}
    if isinstance(d, dict):
        for keys in list(d.keys()):
            
            ####### The case where we want to filter by name
            if name0_value1_type2_length3 == 0:
                if keys == key_to_remove:                       # The Logical Test
                    print('----- removed '+keys)
                    remove_count=remove_count+1
                    pass
                else:
                    ############################################# Each of these has to test 
                    if isinstance(d[keys],dict):
                        new_d,remove_count = remove_key(d[keys],key_to_remove,name0_value1_type2_length3,remove_count)
                    else:
                        new_d = d[keys]
                    new_dict[keys] = new_d  
                    
            ####### The case where we want to filter by value
            if name0_value1_type2_length3 == 1:
                if d[keys] == key_to_remove:                       # The Logical Test
                    print('----- removed '+keys)
                    remove_count=remove_count+1
                    pass
                else:
                    if isinstance(d[keys],dict):
                        new_d,remove_count = remove_key(d[keys],key_to_remove,name0_value1_type2_length3,remove_count)
                    else:
                        new_d = d[keys]
                    new_dict[keys] = new_d   
                    
            ####### The case where we want to filter by type
            if name0_value1_type2_length3 == 2:
                if isinstance(d[keys],key_to_remove) == 1:         # The Logical Test
                    print('----- removed '+keys)
                    remove_count=remove_count+1
                    pass
                else:
                    if isinstance(d[keys],dict):
                        new_d,remove_count = remove_key(d[keys],key_to_remove,name0_value1_type2_length3,remove_count)
                    else:
                        new_d = d[keys]
                    new_dict[keys] = new_d   
                    
            ####### The case where we want to filter by length
            if name0_value1_type2_length3 == 3:
                if len(d[keys]) == key_to_remove:                       # The Logical Test
                    print('----- removed '+keys)
                    remove_count=remove_count+1
                    pass
                else:
                    if isinstance(d[keys],dict):
                        new_d,remove_count = remove_key(d[keys],key_to_remove,name0_value1_type2_length3,remove_count)
                    else:
                        new_d = d[keys]
                    new_dict[keys] = new_d   
                    
        return new_dict,remove_count