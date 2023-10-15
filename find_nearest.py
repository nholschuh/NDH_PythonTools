import numpy as np

def find_nearest(vector_2_search,value,how_many=1):
    """
    % (C) Nick Holschuh - Penn State University - 2013 (Nick.Holschuh@gmail.com)
    % In the way that the find commands finds values in a matrix identical to
    % the search vector, this command finds the nearest entry.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    % vector_2_search = The set of data that you want to search. Each entry
    %                   should be a row. This also works with a n x m x 2
    %                   matrix to search, with x y pairs in the 3rd dimension.
    % value = The value you want to find within "vector_2_search" (row vector)
    % how_many = The function will find the x nearest values to "value", where
    %               x is an integer defined by "how_many"
    %
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    % index = the index values for the location within "vector_2_search" where
    % the nearest possible values are stored.
    %
    % results = the values themselves within the vector.
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    if isinstance(vector_2_search,list):
        vector_2_search = np.array(vector_2_search)
    if isinstance(value,list):
        value = np.array(value)
    
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