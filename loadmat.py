import hdf5storage
import mat73
import scipy
import numpy as np

################## NDH Tools self imports
###########################################################
from .read_h5 import read_h5
###########################################################

def loadmat(fn, varnames=None ,debug_flag = 0, force_method=0):
    """
    % (C) Nick Holschuh - Amherst College -- 2024 (Nick.Holschuh@gmail.com)
    %
    % This function uses existing tools to intelligently load .mat files
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     fn -- the .mat file to load (full path)
    %     varnames -- default=None, this allows you to load just a subset of variables.
    %     force_method -- requirue the use of mat73 (1), read_h5 (2), or scipy (3). If 0,
    %                     the code will attempt all methods until one works (or it fails)
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %      data -- Ideally, a dictionary with keys corresponding to variables in the .mat file
    %              I think, sometimes, it produces a tuple that you have to index into, although
    %              I've tried to prevent that.
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 
    import scipy.io

    if force_method == 0:
        ############################ Try statement, that will catch if all else fails
        try:
            if varnames == None:

                #################### Try for options 1, 2, and 3, no defined variables
                try:
                    try:
                        if debug_flag == 1:
                            print('Trying Method 1 with no described variables')
                        data = mat73.loadmat(fn)
                    except:
                        if debug_flag == 1:
                            print('Trying Method 2 with no described variables')                    
                        data = read_h5(fn)
                        data = data[0]
                        for var_opts in data.keys():
                            if type(data[var_opts]) == type(np.array([])):
                                if len(data[var_opts].dtype) > 1:
                                    data[var_opts] = data[var_opts]
                                    temp = data[var_opts]['real'] + 1j * data[var_opts]['imag']
                                    data[var_opts] = temp.astype(np.complex64)
                except:
                    if debug_flag == 1:
                        print('Trying Method 3 with no described variables') 
                    data = scipy.io.loadmat(fn,squeeze_me=True)
                
            else:
                #################### Attempt with defined variables
                try:
                    try:
                        if debug_flag == 1:
                            print('Trying Method 1 with defined variables')
                        data = scipy.io.loadmat(fn,variable_names=varnames,squeeze_me=True)
                    except:
                        data = read_h5(fn,varnames)
                        data = data[0]
                        for var_opts in data.keys():
                            if type(data[var_opts]) == type(np.array([])):
                                if len(data[var_opts].dtype) > 1:
                                    data[var_opts] = data[var_opts]
                                    temp = data[var_opts]['real'] + 1j * data[var_opts]['imag']
                                    data[var_opts] = temp.astype(np.complex64)           
                except:
                    if debug_flag == 1:
                        print('Abandoning the goal of loading specific variables')
                    data = mat73.loadmat(fn)
                    print('You couldn''t load just the variables you asked for, but loaded the whole file instead')
                    
        ############################ The catch all option when everything fails                
        except:
            if debug_flag == 1:
                print('Something is wrong with this .mat file')
            data = {}

    ################################ Forcing a particular method for testing
    elif force_method == 1:
        data = mat73.loadmat(fn)
        
    elif force_method == 2:
        if varnames == None:
            data = read_h5(fn)
        else:
            data = read_h5(fn,varnames)
            
        data = data[0]
        for var_opts in data.keys():
            if type(data[var_opts]) == type(np.array([])):
                if len(data[var_opts].dtype) > 1:
                    data[var_opts] = data[var_opts]
                    temp = data[var_opts]['real'] + 1j * data[var_opts]['imag']
                    data[var_opts] = temp.astype(np.complex64)
                    
    elif force_method == 3:
        if varnames == None:
            data = scipy.io.loadmat(fn,variable_names=varnames,squeeze_me=True)
        else:
            data = scipy.io.loadmat(fn,squeeze_me=True)

    ################################ Forcing a particular method for testing
    if isinstance(data,tuple) == 1:
        data = data[0]
        
    return data
    
    
