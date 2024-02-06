################ This is the import statement required to reference scripts within the package
import os,sys,glob
ndh_tools_path_opts = [
    '/mnt/data01/Code/',
    '/home/common/HolschuhLab/Code/'
]
for i in ndh_tools_path_opts:
    if os.path.isfile(i): sys.path.append(i)
################################################################################################

def find_pixelcoords(im_filename,original_width,original_height,im_pick_params=0):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    %     This function does the standard load, transformation, and plotting
    %     that is common in the CReSIS radar analysis workflow
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     im_filename - The filename of the image that you want to extract info from
    %     originial_width - The original matrix width (used to generate the image)
    %     original__height - The original matrix height (used to generate the image
    %     im_pick_params - This defines how the contours are treated. There should be four parameters per image:
    %                             ### ---- which bands to look for minima in (color of lines)
    %                             ### ---- minimum contour size (number of points)
    %                             ### ---- the aggregation type (0: average of marker, 1: horizontal bar)
    %                             ### ---- distance threshold for pixel combination or separation
    %                             ### ---- the distance calculation method (0:true or 1:vertical or 2:overweight horizontal)
    %                       0 defaults to [[0,5,0,5],[2,25,1,10]] which looks for blue points and red lines
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %     pick_output - A list containing pixel coordinate information for the points and lines of interest
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 
    
    from PIL import Image
    import NDH_Tools as ndh
    import numpy as np
    import cv2
    import tqdm


    im_handle = Image.open(im_filename)
    np_frame = np.array(im_handle)

    ########### Here we identify which pixels are in the plot, and the two axes
    
    ######################### This method only works if the image is perfectly white outside of the axes
    if 0:
        im_frame = np.where(np_frame[:,:,3] == 255)
    
        cinds = ndh.minmax(im_frame[1])
        rinds = ndh.minmax(im_frame[0])
    else:
    ########################## This is meant to handle some spillover of lines and points outside the image
        row_sum = np.sum(np_frame[:,:,2] == 255,axis=1)
        col_sum = np.sum(np_frame[:,:,2] == 255,axis=0)
        
        rinds = ndh.minmax(np.where(row_sum <= np.percentile(row_sum,80)-1))
        cinds = ndh.minmax(np.where(col_sum <= np.percentile(col_sum,80)-1))
        
    xrange = np.linspace(0,original_width,cinds[1]-cinds[0])
    yrange = np.linspace(0,original_height,rinds[1]-rinds[0])

    sub_im = np_frame[rinds[0]:rinds[1],cinds[0]:cinds[1],:]

    ########### Here, we pull out the markings on the image. Where there is no blue, it is likely red, and vice versa
    if im_pick_params == 0:
        im_colors = ['blue','red']
        im_pick_params = [[0,5,0,50,2],[2,25,1,10,1]] 
        ### This defines how the contours are treated. There should be three parameters here:
                                 ### ---- which bands to look for minima in (0: red, 1: green, 2:blue)
                                 ### ---- minimum contour size (number of points)
                                 ### ---- the aggregation type (0: average of marker, 1: horizontal bar)
                                 ### ---- distance threshold for pixel combination or separation
                                 ### ---- the distance calculation method (0:true or 1:vertical, 2: overweight horizontal)

    pick_output = []
    
    for ind1 in range(len(im_pick_params)):

        _, process_im = cv2.threshold(sub_im[:,:,im_pick_params[ind1][0]], 5, 255, cv2.THRESH_BINARY_INV)
        process_contours, _ = cv2.findContours(process_im, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        pick_temp = []
        #######################################################################################            
        ############ Here, we post-process the picks to deal with gaps / multiple layers, etc.        
        #######################################################################################
        ########### Finally, we loop through the edge_trims and the picks, and pull out just the relevant info

        #print('--- Total number of countoured objects to process: %d' %len(process_contours))
        mod_step = 10**np.floor(np.log10(len(process_contours)/10));

        
        #for ind2 in tqdm.tqdm(range(len(process_contours))):
        for ind2 in range(len(process_contours)):

            pick_img = np.zeros_like(process_im)
            cv2.drawContours(pick_img, process_contours, ind2, color=255, thickness=-1)
            rind,cind = np.where(pick_img)
            true_x_inds = np.round(xrange[cind])

            ########## Attempt to exclude bad contours
            if len(rind) > im_pick_params[ind1][1]:

                ##################################### Here is the case where you just want a contour's centroid
                if im_pick_params[ind1][2] == 0:
                    x_ind = int(np.mean(cind)) 
                    y_ind = int(np.mean(rind))
                    true_x_ind = np.round(xrange[x_ind]) 
                    true_y_ind = np.round(yrange[y_ind])
                    ######## Here we add the results to the final object
                    pick_temp.append([true_x_ind,true_y_ind])

                #################################### Here you want the full contour, assuming it is horizontal
                if im_pick_params[ind1][2] == 1:
                    pick_temp_temp = []
                    for ind3, cols in enumerate(np.unique(true_x_inds)):
                        true_x_ind = int(cols) 
                        compare_inds = np.where(true_x_inds == cols)[0]
                        ########## We want to lean toward the top side, so we split the difference between mean and min
                        y_ind = int(np.mean([
                            np.mean(rind[compare_inds]),
                            np.min(rind[compare_inds])])
                        )
                        true_y_ind = np.round(yrange[y_ind])                        
                        pick_temp_temp.append([true_x_ind,true_y_ind])
                    pick_temp.append(np.array(pick_temp_temp))


        if len(pick_temp) > 0:
            #######################################################################################            
            ############ Here, we post-process the picks to deal with gaps / multiple layers, etc.        
            #######################################################################################
            ###################### This combines points that are within a given distance threshold
            if im_pick_params[ind1][2] == 0:
                dist_thresh = im_pick_params[ind1][3]
                pick_temp_array = np.array(pick_temp)

                if im_pick_params[ind1][4] == 0:
                    pick_pos = pick_temp_array[:,0] + pick_temp_array[:,1]*np.sqrt(np.array(-1,dtype=complex));
                    pick_dists = np.abs(np.tile(pick_pos,(len(pick_pos),1)).transpose()-np.tile(pick_pos,(len(pick_pos),1)))
                elif im_pick_params[ind1][4] == 1:
                    pick_pos = pick_temp_array[:,1];
                    pick_dists = np.abs(np.tile(pick_pos,(len(pick_pos),1)).transpose()-np.tile(pick_pos,(len(pick_pos),1))) 
                if im_pick_params[ind1][4] == 2:
                    pick_pos = pick_temp_array[:,0]*10 + pick_temp_array[:,1]*np.sqrt(np.array(-1,dtype=complex));
                    pick_dists = np.abs(np.tile(pick_pos,(len(pick_pos),1)).transpose()-np.tile(pick_pos,(len(pick_pos),1)))                

                for ind2 in range(len(pick_temp_array)):
                    pick_dists[0:ind2+1,ind2] = 1000
                min_pick_dist = np.min(pick_dists,1)
                combine_inds = np.where(min_pick_dist < dist_thresh)[0]
                remove_inds = []
                new_picks = []
                for i in combine_inds:
                    j = np.where(pick_dists[i,:] == min_pick_dist[i])[0][0]
                    remove_inds.append(i)
                    remove_inds.append(j)
                    new_x_ind = int(np.mean([pick_temp_array[i,0],pick_temp_array[j,0]]))
                    new_y_ind = int(np.mean([pick_temp_array[i,1],pick_temp_array[j,1]]))
                    new_picks.append([new_x_ind,new_y_ind])

                keep_inds = list(set(np.arange(0,len(pick_temp_array)).tolist())-set(remove_inds))
                old_picks = pick_temp_array[keep_inds]

                ## Here we deal with all replaced or no replaced edge cases
                if len(keep_inds) == 0:
                    pick_temp = new_picks
                elif len(new_picks) == 0:
                    pick_temp = old_picks.tolist()
                else:
                    pick_temp = np.concatenate([old_picks,np.array(new_picks)]).tolist()

            ################### Here is the layer, rather than point, case, where layers smaller than a particular size are joined
            if im_pick_params[ind1][2] == 1:
                dist_thresh = im_pick_params[ind1][3]

                pick_dist = np.ones([len(pick_temp),len(pick_temp)])*1e5
                for ind2 in range(len(pick_temp)):
                    for ind3 in np.arange(ind2+1,len(pick_temp)):
                        pa_1 = np.array(pick_temp[ind2])
                        pa_2 = np.array(pick_temp[ind3])
                        pick_dist_temp = ndh.find_nearest_xy(pa_1,pa_2)
                        pick_dist[ind2,ind3] = np.min(pick_dist_temp['distance'])

                min_pick_dist = np.min(pick_dist,1)
                combine_inds = np.where(min_pick_dist < dist_thresh)[0]

                remove_inds = []
                new_picks = []
                for i in combine_inds:
                    j = np.where(pick_dist[i,:] == min_pick_dist[i])[0][0]
                    remove_inds.append(i)
                    remove_inds.append(j)
                    new_picks.append(pick_temp[i].tolist()+pick_temp[j].tolist())

                keep_inds = list(set(np.arange(0,len(pick_temp)).tolist())-set(remove_inds))
                old_picks = ndh.index_list(pick_temp,keep_inds)


                if len(keep_inds) == 0:
                    pick_temp = new_picks
                elif len(new_picks) == 0:
                    pick_temp = old_picks
                else:
                    pick_temp = old_picks+new_picks

                ###### I'm not sure why, but for some reason, some layers are lists and some are arrays. Here we make them all arrays
                for i in range(len(pick_temp)):
                    pick_temp[i] = np.array(pick_temp[i])
        
            

        
        if im_pick_params[ind1][2] == 0:
            pick_output.append(pick_temp)
        else:
            pick_output.append(pick_temp)

                    

    return pick_output