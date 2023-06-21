import hdf5storage
import mat73
import scipy

import sys
sys.path.append('/mnt/data01/Code/')

def loadmat(fn,varnames=None):
    """


    """
    
    from NDH_Tools import read_h5

    try:
        if varnames == None:
            data = mat73.loadmat(fn)
            #print('Used the Mat73 Method')
        else:
            data = read_h5(fn,varnames)
            
    except:
        try:
            
            data = scipy.io.loadmat(fn,varnames,squeeze_me=True)
            
#            ############ This loop collapses unnecessary dimensions
#            for i in data.keys():
#                if type(data[i]) == type({}):
#                    for j in data[i].keys():
#                        if type(data[i][j]) == type({}):
#                            pass
#                        else:
#                            try:
#                                data[i][j] = np.squeeze(data[i][j])
#                            except:
#                                pass
#                else:
#                    try:
#                        data[i] = np.squeeze(data[i])
#                    except:
#                        pass                       
                        
            
            #print('Used the SciPy Method')
        except:
            print('Something is wrong with this .mat file')
            
    return data
    
    
