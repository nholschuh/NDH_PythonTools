import hdf5storage
import scipy.io
import mat73
import os

################ This is the import statement required to reference scripts within the package
import os,sys
ndh_tools_path_opts = [
    '/mnt/data01/Code/',
    '/home/common/HolschuhLab/Code/'
]
for i in ndh_tools_path_opts:
    if os.path.isfile(i): sys.path.append(i)
#################################################################

def savemat(matfiledata,fn):
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
    
    rm_keys = []
    for i in list(matfiledata):
        if isinstance(matfiledata[i],mat73.AttrDict):
            rm_keys.append(i)
            
    if len(rm_keys) > 0:
        print('Warning: .mat save functions can''t handle certain object types [mat73.AttrDict].\n')
        for i in rm_keys:
            #matfiledata, rmnum = remove_key(matfiledata,i,0)
            matfiledata[i] = dict(matfiledata[i])
    
    
    try:
        try:
            try:
                os.remove(fn)
            except:
                pass
            hdf5storage.write(matfiledata, '.', fn, matlab_compatible=True)
        except:
            scipy.io.savemat(fn,matfiledata)
    except:
        print('Something is wrong, and the savemat functions failed.')
    
