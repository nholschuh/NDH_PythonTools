import hdf5storage
from scipy.io import loadmat

def loadmat(fn):
    """


    """

    try:
        data = hdf5storage.loadmat(fn)
    except:
        data = loadmat(fn)
        
    return data
    
