import numpy as np

def find_nearest_xy(vector_2_search,value,how_many=1):
    """
    % (C) Nick Holschuh - Penn State University - 2013 (Nick.Holschuh@gmail.com)
    %
    % In the way that the find commands finds values in a matrix identical to
    % the search vector, this command finds the nearest entry. For use with 
    % arrays of points defined by two coordinates: x and y
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    % vector_2_search = The set of data that you want to search. Primary use has
    %                   this object as an nx2 array, where the columns correspond
    %                   to the x and y coordinates. 
    %                   This also works with a n x m x 2 matrix to search, with 
    %                   x y pairs in the 3rd dimension.
    % value = The values you want to find within "vector_2_search". This must be
    %         an nx2 array, where columns are x and y coordinates
    % how_many = The function will find the x nearest values to "value", where
    %            x is an integer defined by "how_many". 
    %
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

        
    sd = vector_2_search.shape
    if sd[0] == 2:
        vector_2_search = vector_2_search.transpose();
    else:
        vector_2_search = vector_2_search;

    ss = value.shape
    if len(ss) == 1:
        value = np.expand_dims(value,axis=0)
        ss = value.shape    

    ## The two column, vector search case
    if len(sd) == 2:

        comp_vec = vector_2_search[:,0] + vector_2_search[:,1]*np.sqrt(np.array(-1,dtype=complex));
        ss = value.shape
        if np.all([np.min(ss) > 1,ss[0] >= ss[1]]):
            value2 = value.transpose();
        elif ss[0] == 1:
            value2 = value.transpose();
        else:
            value2 = value;


        value_search = value2[0,:] + value2[1,:]*np.sqrt(np.array(-1,dtype=complex));

        complex_dists = np.tile(comp_vec,(len(value_search),1)).transpose()-np.tile(value_search,(len(comp_vec),1))
        dists = np.abs(complex_dists);

        ## Most efficient method for looking for an individual
        ## value

        if how_many == 1:
            minval = np.min(dists,0)
            ind = np.argmin(dists,0)
            index = ind.transpose()
            distance = minval.transpose();
            result = vector_2_search[index,:];    
        else:
            rankings = np.argsort(dists,0)
            ind = rankings[0:how_many,:]
            index = ind.transpose()
            cols = np.arange(len(value[:,0]))
            distance = np.zeros(index.shape)
            result = np.zeros(np.append(index.shape,how_many))
            for ind2 in np.arange(how_many):
                rows = index[:,ind2]            
                distance[:,ind2] = dists[rows,cols]
                result[:,:,ind2] = vector_2_search[rows,:]
            


    #### The m x n x 2, matrix search case
    elif sd[2] == 2:
        vector_2_search_temp[:,:,0] = vector_2_search[:,:,0] - value[:,0];
        vector_2_search_temp[:,:,1] = vector_2_search[:,:,1] - value[:,1];   

        vector_2_search_temp2 = (vector_2_search_temp[:,:,0]**2+vector_2_search_temp[:,:,1]**2)**0.5;

        counter = 1;
        while counter <= how_many:
            temp_index = np.where(np.min(np.min(vector_2_search_temp2)) == vector_2_search_temp2)
            [index_r,index_c] = np.where(np.min(np.min(vector_2_search_temp2)) == vector_2_search_temp2);
            for i in np.arange(0,len(temp_index)):
                index[counter] = temp_index[i]; 
                distance[counter] = np.min(np.min(vector_2_search_temp2));
                result[counter,:] = [vector_2_search[index_r[i],index_c[i],1],vector_2_search[index_r[i],index_c[i],2]];

                ## This sets the distance to the recently selected point to
                ## max, so it is not chosen again.
                vector_2_search_temp2[index[counter]] = np.max(np.max(vector_2_search_temp2));
                counter = counter+1;

                if counter > how_many:
                    break
                    
    return {'index':index, 'distance':distance, 'result':result}