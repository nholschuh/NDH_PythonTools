import numpy as np
import matplotlib.pyplot as plt
import tqdm
import xarray as xr

################ This is the import statement required to reference scripts within the package
import os,sys,glob
ndh_tools_path_opts = [
    '/mnt/data01/Code/',
    '/mnt/l/mnt/data01/Code/',
    '/home/common/HolschuhLab/Code/'
]
for i in ndh_tools_path_opts:
    if os.path.isfile(i): sys.path.append(i)
################################################################################################

import NDH_Tools as ndh

def calculate_flowlines(input_xr,seed_points,uv_varnames=['u','v'],xy_varnames=['x','y'],steps=20000,ds=2,forward0_both1_backward2=1):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % This function prints out the minimum and maximum values of an array
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     input_xr -- xarray dataarray that has the gradient objects in it
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %      output -- the min and max in a 1x2 array
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 

    ##################### Here, we standardize the naming convention within the xarray object
    input_xr = input_xr.rename({xy_varnames[0]:'x',xy_varnames[1]:'y'})
    uv_scalar = np.sqrt(input_xr[uv_varnames[0]].values**2 + input_xr[uv_varnames[1]].values**2)
    input_xr[uv_varnames[0]] = (('y','x'),input_xr[uv_varnames[0]].values/uv_scalar)
    input_xr[uv_varnames[1]] = (('y','x'),input_xr[uv_varnames[1]].values/uv_scalar)


    #################### We initialize the objects for the flowline calculation
    flowlines = []

    #################### Here is the forward calculation
    if forward0_both1_backward2 <= 1:
        temp_xs = np.expand_dims(seed_points[:,0],0)
        temp_ys = np.expand_dims(seed_points[:,1],0)

        for ind0 in tqdm.tqdm(np.arange(steps)):
            x_search = xr.DataArray(temp_xs[-1,:],dims=['vector_index'])
            y_search = xr.DataArray(temp_ys[-1,:],dims=['vector_index'])
            new_u = input_xr[uv_varnames[0]].sel(x=x_search,y=y_search,method='nearest')
            new_v = input_xr[uv_varnames[1]].sel(x=x_search,y=y_search,method='nearest')

            ######### This is an order of magnitude slower
            #new_u = input_xr[uv_varnames[0]].interp(x=x_search,y=y_search)
            #new_v = input_xr[uv_varnames[1]].interp(x=x_search,y=y_search)

            temp_xs = np.concatenate([temp_xs,temp_xs[-1:,:]+new_u.values.T*ds])
            temp_ys = np.concatenate([temp_ys,temp_ys[-1:,:]+new_v.values.T*ds])

        xs = temp_xs
        ys = temp_ys
    else:
        xs = np.empty([0,len(seed_points)])
        ys = np.empty([0,len(seed_points)])


    #################### Here is the backward calculation
    if forward0_both1_backward2 >= 1:
        temp_xs = np.expand_dims(seed_points[:,0],0)
        temp_ys = np.expand_dims(seed_points[:,1],0)

        for ind0 in tqdm.tqdm(np.arange(steps)):
            x_search = xr.DataArray(temp_xs[-1,:],dims=['vector_index'])
            y_search = xr.DataArray(temp_ys[-1,:],dims=['vector_index'])
            new_u = input_xr[uv_varnames[0]].sel(x=x_search,y=y_search,method='nearest')
            new_v = input_xr[uv_varnames[1]].sel(x=x_search,y=y_search,method='nearest')

            ######### This is an order of magnitude slower
            #new_u = input_xr[uv_varnames[0]].interp(x=x_search,y=y_search)
            #new_v = input_xr[uv_varnames[1]].interp(x=x_search,y=y_search)

            temp_xs = np.concatenate([temp_xs,temp_xs[-1:,:]-new_u.values.T*ds])
            temp_ys = np.concatenate([temp_ys,temp_ys[-1:,:]-new_v.values.T*ds])

        xs = np.concatenate([np.flipud(temp_xs),xs])
        ys = np.concatenate([np.flipud(temp_ys),ys])  



    flowlines = []
    for ind0 in np.arange(len(xs[0,:])):
        xy = np.stack([xs[:,ind0],ys[:,ind0]]).T
        flowlines.append(xy)
        
    return flowlines

##########################################################################################
#### This version of the code doesn't work quite right...
##########################################################################################
##def calculate_flowlines(x,y,u,v,seed_points,max_error=0.00001,retry_count_threshold=10):
##    """
##    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
##    %
##    % This function prints out the minimum and maximum values of an array
##    %
##    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
##    % The inputs are:
##    %
##    %     input_array -- array of data to analyze
##    %
##    %%%%%%%%%%%%%%%
##    % The outputs are:
##    %
##    %      output -- the min and max in a 1x2 array
##    %
##    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
##    """ 
##
##    ################# This uses a modified plt.streamline to pass through a user-editable keyword
##    ################# argument "max_error", which goes into the interpolater to guarantee
##    ################# accurate streamline calculation. Copy the updated version of streamplot
##    ################# into your matplotlib directory to enable the use of streamline
##    ################# calculation from NDH_Tools (in streamline.py, which calls _integrate_rk12)
##
##    if isinstance(seed_points,list):
##        seed_points = np.array(seed_points)
##
##    if len(seed_points.shape) == 1:
##        seed_points = np.expand_dims(seed_points,axis=0)
##
##    ###################### Initialize the returned object
##    final_sls = []
##    for ind0 in np.arange(len(seed_points[:,0])):
##        final_sls.append([])
##
##    retry_count = 0
##    retry_inds = np.arange(0,len(seed_points[:,0]))
##    seed_subset = seed_points
##
##    while len(retry_inds) > 0:
##
##        sls = []
##
##        ################# Calculate the streamlines for all unfound seed points
##        fig = plt.figure()
##        if retry_count == 0:
##            print('The initial streamline calculation -- this can be slow. Finding '+str(len(seed_subset[:,0]))+' streamlines')
##        try:
##            streamlines = plt.streamplot(x,y,u,v,start_points=seed_points, max_error=max_error, density=100)
##        except:
##            streamlines = plt.streamplot(x,y,u,v,start_points=seed_points, density=100)
##            if retry_count == 0:
##                print('Note: You need to update your matplotlib streamline.py and reduce the max error for this to work properly')
##        plt.close(fig)
##
##        ################# Here we extract the coordinate info from the streamlines
##        sl_deconstruct = []
##        for i in streamlines.lines.get_paths():
##            sl_deconstruct.append(i.vertices[1])
##        sl_deconstruct = np.array(sl_deconstruct)
##
##        ################ Here we separate the streamlines based on large breaks in distance
##        sl_dist = ndh.distance_vector(sl_deconstruct[:,0],sl_deconstruct[:,1],1)
##        dist_mean = np.mean(sl_dist)
##        breaks = np.where(sl_dist > (dist_mean+1)*50)[0]
##        if len(breaks) > 0:
##            breaks = np.concatenate([np.array([-1]),breaks,np.array([len(sl_deconstruct[:,0])])])+1
##        else:
##            breaks = np.array([0,len(sl_deconstruct[:,0])+1])
##
##        for ind0 in np.arange(len(breaks)-1):
##            sls.append(sl_deconstruct[breaks[ind0]:breaks[ind0+1],:])
##
##        ################ Here we identify which streamline goes with which seed_point
##        matching = []
##        for ind0 in np.arange(len(seed_subset[:,0])):
##            dists = []
##            for ind1,sl in enumerate(sls):
##                comp_vals = ndh.find_nearest_xy(sl,seed_subset[ind0,:])
##                dists.append(comp_vals['distance'][0])
##            best = np.where(np.array(dists) < 1e-8)[0]
##            try:
##                matching.append(best[0])
##            except:
##                matching.append(-1)
##
##        ################# populate the final object
##        for ind0,i in enumerate(matching):
##            if i != -1:
##                final_sls[retry_inds[ind0]] = sls[i]
##
##        ################# Finally, we identify the new set of streamlines that need to be computed, based on which have no match
##        new_retry_inds = np.where(np.array(matching) == -1)[0]
##        seed_subset = seed_points[retry_inds[new_retry_inds],:]
##        retry_inds = retry_inds[new_retry_inds]
##
##        if len(retry_inds) > 0:
##            retry_count = retry_count+1
##            print('Recalculating for nearly overlapping points -- try '+str(retry_count)+'. Finding '+str(len(seed_subset[:,0]))+' streamlines')
##            
##        if retry_count > retry_count_threshold:
##            break
##
##    if 0:
##        plt.figure()
##        plt.plot(test_dist)
##        plt.axhline(dist_median,c='orange')
##
##    if 0:
##        plt.figure()
##        plt.plot(test[:,0],test[:,1],c='blue')
##        for i in final_sls:
##            plt.plot(i[:,0],i[:,1],c='red')
##        plt.plot(seed_points[:,0],seed_points[:,1],'o')
##
##
##    return final_sls