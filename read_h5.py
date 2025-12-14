import h5py
import numpy as np

################## NDH Tools self imports
###########################################################
from .remove_key import remove_key
###########################################################

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
                    ds_dict[group_info[1]] = _read_dataset_resolving_refs(node, h5f)
                
                if len(group_info)-2 == 1:
                        ds_dict[group_info[1]][group_info[2]] = _read_dataset_resolving_refs(node, h5f)

                elif len(group_info)-2 == 2:
                        ds_dict[group_info[1]][group_info[2]][group_info[3]] = _read_dataset_resolving_refs(node, h5f)

                elif len(group_info)-2 == 3:
                        ds_dict[group_info[1]][group_info[2]][group_info[3]][group_info[4]] = _read_dataset_resolving_refs(node, h5f)

                elif len(group_info)-2 == 4:
                        ds_dict[group_info[1]][group_info[2]][group_info[3]][group_info[4]][group_info[5]] = _read_dataset_resolving_refs(node, h5f)
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

    ######################## two additional helper functions
    def _read_dataset_resolving_refs(ds: h5py.Dataset, root_file: h5py.File):
        """Return ds contents, resolving object/region references recursively, no check_dtype()."""
        data = ds[()]  # may be plain data, an object ref, a region ref, or arrays thereof
    
        # Fast path: plain numeric/strings/compound, not references
        if not isinstance(data, (h5py.Reference, h5py.RegionReference, np.ndarray)):
            return data
        if isinstance(data, np.ndarray) and data.dtype.kind != 'O':
            # Non-object arrays (numeric, fixed-length strings, etc.) -> plain data
            return data
    
        def _deref(x):
            # Object reference
            if isinstance(x, h5py.Reference):
                if not x:  # null ref
                    return None
                tgt = root_file[x]
                if isinstance(tgt, h5py.Dataset):
                    return _read_dataset_resolving_refs(tgt, root_file)
                elif isinstance(tgt, h5py.Group):
                    out = {}
                    def _collect(name, obj):
                        parts = name.split('/')
                        cur = out
                        for p in parts[:-1]:
                            cur = cur.setdefault(p, {})
                        if isinstance(obj, h5py.Dataset):
                            cur[parts[-1]] = _read_dataset_resolving_refs(obj, root_file)
                        else:
                            cur = cur.setdefault(parts[-1], {})
                    tgt.visititems(_collect)
                    return out
                return None
    
            # Region reference
            if isinstance(x, h5py.RegionReference):
                if not x:
                    return None
                dset = root_file[x]   # the target dataset
                return dset[x]        # selection within that dataset
    
            # Anything else: return as-is
            return x
    
        # Scalar reference?
        if isinstance(data, (h5py.Reference, h5py.RegionReference)):
            return _deref(data)
    
        # Array of references or mixed objects
        # Build an object array to store dereferenced results
        result = np.empty(getattr(data, 'shape', ()), dtype=object)
        it = np.nditer(np.asarray(data, dtype=object),
                       flags=['refs_ok', 'multi_index', 'zerosize_ok'],
                       op_flags=['readonly'])
        for item in it:
            result[it.multi_index] = _deref(item.item())
        return result

    def normalize_h5(obj):
        """Recursively simplify data read from HDF5:
           - squeeze 1-length axes
           - unwrap singletons
           - convert [('real','imag')] records -> complex
           - collapse stackable object arrays
        """
        # dict: recurse
        if isinstance(obj, dict):
            return {k: normalize_h5(v) for k, v in obj.items()}
    
        # lists/tuples: recurse
        if isinstance(obj, (list, tuple)):
            return type(obj)(normalize_h5(v) for v in obj)
    
        # references that slipped through
        if isinstance(obj, (h5py.Reference, h5py.RegionReference)):
            return None
    
        # numpy arrays
        if isinstance(obj, np.ndarray):
            a = obj
    
            # Convert structured dtype with real/imag -> complex
            if a.dtype.names and {'real', 'imag'} <= set(a.dtype.names):
                a = a['real'] + 1j * a['imag']
    
            # Object arrays: unwrap/stack if possible
            if a.dtype == object:
                # Single-element object array -> unwrap and normalize
                if a.size == 1:
                    return normalize_h5(a.item())
    
                # Normalize each element
                flat = [normalize_h5(x) for x in a.flat]
    
                # Try to stack if all elements are numeric arrays of same shape
                if all(isinstance(x, np.ndarray) and x.dtype != object for x in flat):
                    same_shape = all(x.shape == flat[0].shape for x in flat)
                    if same_shape:
                        try:
                            stacked = np.stack(flat).reshape(a.shape + flat[0].shape)
                            stacked = np.squeeze(stacked)
                            if stacked.size == 1:
                                return stacked.reshape(()).item()
                            return stacked
                        except Exception:
                            pass
    
                # Fallback: rebuild as object array with normalized contents
                return np.array(flat, dtype=object).reshape(a.shape)
    
            # Non-object arrays: squeeze and unwrap scalars
            a = np.squeeze(a)
            if a.size == 1:
                return a.reshape(()).item()
            return a
    
        # scalars etc.
        return obj
    
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

    ds_dict_filt = normalize_h5(ds_dict_filt)
    return ds_dict_filt,orig_struct



    