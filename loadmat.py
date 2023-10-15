import hdf5storage
import mat73
import scipy

import sys
sys.path.append('/mnt/data01/Code/')

def loadmat(fn,varnames=None):
    """


    """
    import scipy.io
    from NDH_Tools import read_h5
    
    debug_flag = 0

    try:
        if varnames == None:
            if debug_flag == 1:
                print('Trying Method 1 with no described variables')
            data = mat73.loadmat(fn)
        else:
            if debug_flag == 1:
                print('Trying Method 1 with no defined variables')
            data = read_h5(fn,varnames)
            
    except:
        try:
            if debug_flag == 1:
                print('Trying Method 2')
            data = scipy.io.loadmat(fn,variable_names=varnames,squeeze_me=True)
        except:
            try:
                if debug_flag == 1:
                    print('Abandoning the goal of loading specific variables')
                data = mat73.loadmat(fn)
                print('You couldn''t load just the variables you asked for, but loaded the whole file instead')
            except:
                if debug_flag == 1:
                    print('Something is wrong with this .mat file')
                data = {}
            
    if isinstance(data,tuple) == 1:
        data = data[0]
        
    return data
    
    
