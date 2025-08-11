################ This is the import statement required to reference scripts within the package
import os,sys,glob
ndh_tools_path_opts = [
    '/mnt/data01/Code/',
    '/home/common/HolschuhLab/Code/',
    '/kucresis/scratch/dataproducts/opr_data/opr_tmp/'
]
for i in ndh_tools_path_opts:
    if os.path.isfile(i): sys.path.append(i)
################################################################################################


import hdf5storage
import scipy.io
import mat73
import numpy as np

def savemat(matfiledata,fn,debug_flag=0):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % Saves a data dictionary as an hdf5 compatible matlab file
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     matfiledata -- data dictionary containing the information to write
    %     fn -- the filename to write to
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 
    
    from NDH_Tools import remove_key

    matfiledata = deep_replace_none(matfiledata)
    
    rm_keys = []
    for i in list(matfiledata):
        try:
            if isinstance(matfiledata[i],mat73.AttrDict):
                rm_keys.append(i)
            #if isinstance(matfiledata[i],type([])):
            #    matfiledata[i] = np.array(matfiledata[i], dtype=numpy.object)
        except:
            pass
            
    if len(rm_keys) > 0:
        print('Warning: .mat save functions can''t handle certain object types [mat73.AttrDict].\n')
        for i in rm_keys:
            #matfiledata, rmnum = remove_key(matfiledata,i,0)
            matfiledata[i] = dict(matfiledata[i])
    
    
    try:
        try:
            #try:
            #    os.remove(fn)
            #except:
            #    pass
            hdf5storage.write(matfiledata, '.', fn, matlab_compatible=True)
            if debug_flag == 1:
                print('Written using the hdf5 writer')
        except:
            scipy.io.savemat(fn,matfiledata)
            if debug_flag == 1:
                print('Written using the scipy.io package')
    except:
        print('Something is wrong, and the savemat functions failed.')

def deep_replace_none(obj):
        if isinstance(obj, dict):
            return {k: deep_replace_none(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [deep_replace_none(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(deep_replace_none(item) for item in obj)
        elif obj is None:
            return 0
        else:
            return obj
