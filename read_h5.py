import sys
sys.path.append('/mnt/data01/Code/')
import h5py

def read_h5(fn,keylist=[],verbose_flag=0):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This function reads a DWG file
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %      fn -- filename of h5 to read
    %      keylist=[] -- This allows you to provide a list of strings, for keys you want to load. All others are excluded
    %      verbose_flag=0 -- If 1, this tells you about the load process
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    %      ds_dict_filt -- a dictionary with all keys with empty values removed
    %      orig_struct -- a dictionary that has all the keys intact, but no data
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %% Note: This only goes 6 groups deep. If you need more than that, this will need to be modified

    """
    from NDH_Tools import remove_key
    
    def get_ds_dictionaries(name, node):
        fullname = node.name
        group_info = fullname.split('/')

        ############# keylist allows you to only load in keys that include a particular string,
        ############# if keylist isn't supplied, everything is loaded. This sets the flag
        ############# that determines if a particular variable should be loaded.
        if len(keylist) == 0:
            load_flag = 1
        else:
            #### Is the string present in the h5 path? If so, load that group/dataset
            if len(set.intersection(set(keylist),set(group_info))) > 0:
                load_flag = 1
            else:
                load_flag = 0
        
        ############## This is the section of code executed if that key is desired
        if load_flag == 1:
            if isinstance(node, h5py.Dataset):
            # node is a dataset
                if verbose_flag == 1:
                    print(f'Dataset: {fullname}; adding to dictionary')
                                
                if len(group_info)-2 == 0:
                    ds_dict[group_info[1]] = node[:]
                
                if len(group_info)-2 == 1:
                        ds_dict[group_info[1]][group_info[2]] = node[:]

                elif len(group_info)-2 == 2:
                        ds_dict[group_info[1]][group_info[2]][group_info[3]] = node[:]

                elif len(group_info)-2 == 3:
                        ds_dict[group_info[1]][group_info[2]][group_info[3]][group_info[4]] = node[:]

                elif len(group_info)-2 == 4:
                        ds_dict[group_info[1]][group_info[2]][group_info[3]][group_info[4]][group_info[5]] = node[:]
            else:
            # node is a group
                if len(group_info)-1 == 1:
                        ds_dict[group_info[1]] = {}

                elif len(group_info)-1 == 2:
                        ds_dict[group_info[1]][group_info[2]] = {}

                elif len(group_info)-1 == 3:
                        ds_dict[group_info[1]][group_info[2]][group_info[3]] = {}

                elif len(group_info)-1 == 4:
                        ds_dict[group_info[1]][group_info[2]][group_info[3]][group_info[4]] = {}
        
        ########################################################################################## 
        ############## By contrast, this secton just reproduces the h5 structure
        if isinstance(node, h5py.Dataset):
        # node is a dataset
            if len(group_info)-2 == 1:
                    orig_struct[group_info[1]][group_info[2]] = None
            elif len(group_info)-2 == 2:
                    orig_struct[group_info[1]][group_info[2]][group_info[3]] = None
            elif len(group_info)-2 == 3:
                    orig_struct[group_info[1]][group_info[2]][group_info[3]][group_info[4]] = None
            elif len(group_info)-2 == 4:
                    orig_struct[group_info[1]][group_info[2]][group_info[3]][group_info[4]][group_info[5]] = None
        else:
         # node is a group
            if len(group_info)-1 == 1:
                    orig_struct[group_info[1]] = {}
            elif len(group_info)-1 == 2:
                    orig_struct[group_info[1]][group_info[2]] = {}
            elif len(group_info)-1 == 3:
                    orig_struct[group_info[1]][group_info[2]][group_info[3]] = {}
            elif len(group_info)-1 == 4:
                    orig_struct[group_info[1]][group_info[2]][group_info[3]][group_info[4]] = {}
        ##########################################################################################               
                        
    
    
    ################################### This is where the recursive loading actually occurs
    with h5py.File(fn,'r') as h5f:
        ds_dict = {}  
        orig_struct = {}
        if verbose_flag == 1:
            print ('**Walking Datasets to get dictionaries**\n')
        h5f.visititems(get_ds_dictionaries)
        if verbose_flag == 1:
            print('\nDONE')
            print('ds_dict size', len(ds_dict))
        
    ################################### Finally, any keys that have no values in them are removed
    removed_num = 1
    removed_total = 0
    ds_dict_filt = ds_dict
    while removed_num > 0:
        ds_dict_filt,removed_num = remove_key(ds_dict_filt,0,3)
        removed_total = removed_total+removed_num
    
    if verbose_flag == 1:
        print('- Removed '+str(removed_total)+' keys')
    
    return ds_dict_filt,orig_struct