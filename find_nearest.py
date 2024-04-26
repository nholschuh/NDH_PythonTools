import numpy as np

def find_nearest(vector_2_search,value):
    """
    % (C) Nick Holschuh - Penn State University - 2013 (Nick.Holschuh@gmail.com)
    % In the way that the find commands finds values in a matrix identical to
    % the search vector, this command finds the nearest entry.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    % vector_2_search = The set of data that you want to search. Should be a 
    %                   0 or 1 dimensional array (I don't get zero dimensional arrays)
    % value = The value you want to find within "vector_2_search". Can be
    %         a single value or an array of values.
    %
    %%%%%%%%%%%%%%%
    % The output is a dictionary containing:
    %
    %       index = the index values for the location within "vector_2_search" where
    %               the nearest possible values are stored.
    %
    %       distance = the distance between the values and their nearest point within
    %                  the vector_2_search
    %
    %       results = the values themselves within the vector.
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    if isinstance(vector_2_search,list):
        vector_2_search = np.array(vector_2_search)
    if isinstance(value,list):
        value = np.array(value)

    ############### Here, we substitute out NaNs so they are never chosen
    if np.max(np.isnan(vector_2_search) == 1):
        vector_2_search[np.isnan(vector_2_search)] = np.inf
    
    comp_vec = vector_2_search
    
    if isinstance(vector_2_search,type(np.array([]))) == 0:
        if isinstance(vector_2_search,type([])):
            vector_2_search = np.array(vector_2_search)
        else:
            vector_2_search = np.array([vector_2_search])
        
    if isinstance(value,type(np.array([]))) == 0:
        if isinstance(value,type([])):
            vector_2_search = np.array(value)
        else:
            value = np.array([value])

    if len(value):
        value2 = value.transpose()
    else:
        value2 = value


    value_search = value2

    complex_dists = np.tile(comp_vec,(len(value_search),1)).transpose()-np.tile(value_search,(len(comp_vec),1))
    dists = np.abs(complex_dists);

    ## Most efficient method for looking for an individual
    ## value
    minval = np.min(dists,0)
    ind = np.argmin(dists,0)
    index = ind.transpose()
    distance = minval.transpose()
    result = vector_2_search[index]              

    return {'index':index, 'distance':distance, 'result':result}