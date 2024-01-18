import numpy as np
import scipy.interpolate as interp

################ This is the import statement required to reference scripts within the package
import os,sys
ndh_tools_path_opts = [
    '/mnt/data01/Code/',
    '/mnt/l/mnt/data01/Code/'
    '/home/common/HolschuhLab/Code/'
]
for i in ndh_tools_path_opts:
    if os.path.isfile(i): sys.path.append(i)
        
import NDH_Tools as ndh
################################################################################################

def line_fill(segmat,value,density0_or_distance1, start=0, stop=0, keep_vertices=0):
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
        
        dist_vec2 = ndh.distance_vector(segmat[:,0],segmat[:,1],1)
        remove_rows = np.where(dist_vec2 == 0)[0]

        segmat = np.delete(segmat,remove_rows,0)
        dist_vec = ndh.distance_vector(segmat[:,0],segmat[:,1])
        
        if stop == 0:
            new_dist = np.arange(start,np.max(dist_vec),value)
        elif stop > np.max(dist_vec):
            new_dist = np.arange(start,np.max(dist_vec),value)
        else:
            new_dist = np.arange(start,stop,value)
            
            
        ############## This section maintains the vertices in the data
        if keep_vertices == 1:
            angle_thresh = 0.1
            headings = ndh.heading(segmat[:,0],segmat[:,1])
            headings_change = np.abs(np.diff(headings))
            keep_inds = np.where(headings_change > angle_thresh)[0]
            add_dists = dist_vec[keep_inds]
            new_dist = np.unique(sorted(np.concatenate([np.array([0]),new_dist,add_dists,np.array([np.max(dist_vec)])])))
            
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
    
