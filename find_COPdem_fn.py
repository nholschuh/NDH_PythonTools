import numpy as np
import sys
import os
import inspect
sys.path.append('/mnt/data01/Code/')


def find_COPdem_fn(lat,lon):
    """
    This is a function that outputs the filename associated wtih the desired latitude & longitude 
    """
    
    from NDH_Tools import find_nearest_xy
    from NDH_Tools import loadmat
    
    curpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    mf_name = curpath+'/COPdem_filelist.mat'
    
    file_info = loadmat(mf_name)
    target = np.array([[float(lat)], [float(lon)]])
    result = find_nearest_xy(file_info['latlon'],target)
    
    if result['distance'] > 1:
        print('This DEM likely doesn\'t contain your point of interest.')
        print('The DEM center is %0.2f degrees away from the target point.' % result['distance'])
    
    return file_info['fn'][result['index'][0]]
    
