import numpy as np
import scipy.interpolate as interp
import sys
sys.path.append('/mnt/data01/Code/')
from NDH_Tools import distance_vector

def line_fill(segmat,value,density0_or_distance1):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % Fills in data points with given 'density' along provided segments, withdata 
    % provided in an nxm matrix, where n is the number of data, with thefirst 2 
    % columns containing the x and y coordinates. The later columns can be other 
    % data that you wish to linearly interpolate between points.
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     segmat -- This is an Nx2 matrix that contains x and y values
    %     value -- either the density or the distance between points
    %     density0_or_distance1 -- this defines either the number of points
    %               between the supplied values in the segmat, or the spacing
    %               between them.
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %      linematrix -- array with the additional values inserted
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 


    if isinstance(segmat,type(np.array)) == 0:
        segmat = np.array(segmat)

    s_dim = segmat.shape
    turnflag = 2

    if np.min(s_dim) == 1:
        remove_flag = 1;
        if s_dim(1) == 1:
            segmat = [segmat.T,np.zeros(segmat.T.shape)];
            turnflag = 1
        else:
            segmat = [segmat,zeros(segmat.shape)];
            turnflag = 2
    else:
        remove_flag = 0
        if s_dim[0] == 2:
            segmat = segmat.T
            turnflag = 1


    ################### the section for interpolating a fixed number of points for each group
    if density0_or_distance1 == 0:
        linematrix = np.zeros((value*(len(segmat[:,1])-1)+1,len(segmat[0,:]))) #Creates an empty vector with the value*# of original values

        for i in np.arange(len(segmat[:,1])-1):
            rangevec = segmat[i+1,:] - segmat[i,:]
            incrementvec = rangevec/value

            startingindex = value*i
            linematrix[startingindex,:] = segmat[i,:]
            for j in np.arange(value-1):
                linematrix[startingindex+j+1,:] = linematrix[startingindex+j,:]+incrementvec

        linematrix[len(linematrix[:,1])-1,:] = segmat[len(segmat[:,1])-1,:]



    ###################     
    else:
        dist_vec2 = distance_vector(segmat[:,0],segmat[:,1],1)
        remove_rows = np.where(dist_vec2 == 0)[0]

        segmat = np.delete(segmat,remove_rows,0)
        dist_vec = distance_vector(segmat[:,0],segmat[:,1])
        new_dist = np.arange(0,np.max(dist_vec),value)

        linematrix = np.zeros((len(new_dist),len(segmat[0,:])))
        for i in np.arange(len(segmat[0,:])):
            f =  interp.interp1d(dist_vec,segmat[:,i])
            linematrix[:,i] = f(new_dist)


    if remove_flag == 1:
        linematrix = linematrix[:,:-2]

    if turnflag == 1:
        segmat = segmat.T
        linematrix = linematrix.T
    elif turnflag == 2:
        linematrix = linematrix   
        
    return linematrix
    
