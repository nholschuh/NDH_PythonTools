################ This is the import statement required to reference scripts within the package
import os,sys
ndh_tools_path_opts = [
    '/mnt/data01/Code/',
    '/home/common/HolschuhLab/Code/'
]
for i in ndh_tools_path_opts:
    if os.path.isfile(i): sys.path.append(i)

import matplotlib.pyplot as plt
import numpy as np
################################################################################################


def radar_load_music(fn):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    %     This function enables the loading and concatenation of multiple music files
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     fn -- the input filename or list of filenames to be read
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %     radar_data -- the simple product of loading the mat file (+ x and y coordinates and distance added)
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 

    
    import NDH_Tools as ndh
    
    if isinstance(fn,list) == 0:
        fn = [fn]
        
    concat_list = ['Elevation','GPS_time','Latitude','Longitude','Surface','Bottom']
    
    ############## Here we loop through the radar data and concatenate the files
    for fn_ind,fn_temp in enumerate(fn):
        
        if fn_ind == 0:
            radar_data = ndh.loadmat(fn_temp);
            xy = ndh.polarstereo_fwd(radar_data['Latitude'],radar_data['Longitude'])
            distance = ndh.distance_vector(xy['x'],xy['y'])
            radar_data['x'] = xy['x']
            radar_data['y'] = xy['y']
            radar_data['distance'] = distance
            radar_data['im_end'] = [0,len(distance)]
            radar_data['orig_ind'] = np.arange(0,len(distance))
            radar_data['filename'] = [fn_temp.split('/')[-1]]
            
        if fn_ind > 0:
            
            radar_data_temp = ndh.loadmat(fn_temp)
            xy_temp = ndh.polarstereo_fwd(radar_data_temp['Latitude'],radar_data_temp['Longitude'])
            
            ########## Here we deal with potentially overlapping frames
            comp_dists = ndh.find_nearest_xy([xy_temp['x'],xy_temp['y']],[radar_data['x'][-1],radar_data['y'][-1]])
            
            if comp_dists['index'] != 0:                
                for cut_key in concat_list:
                    radar_data_temp[cut_key] = radar_data_temp[cut_key][comp_dists['index'][0]:]
                radar_data_temp['Data'] = radar_data_temp['Data'][:,comp_dists['index'][0]:]
                radar_data_temp['Tomo']['img'] = radar_data_temp['Tomo']['img'][:,:,comp_dists['index'][0]:]
                xy_temp['x'] = xy_temp['x'][comp_dists['index'][0]:]
                xy_temp['y'] = xy_temp['y'][comp_dists['index'][0]:]
            
            inc_dist = comp_dists['distance'][0]
            distance = ndh.distance_vector(xy_temp['x'],xy_temp['y'])
        
            if inc_dist < 0.01:
                inc_dist = 0.01
                
            ########## Here we do the data concatenation
            radar_data['x'] = np.concatenate([radar_data['x'],xy_temp['x']])
            radar_data['y'] = np.concatenate([radar_data['y'],xy_temp['y']])
            radar_data['distance'] = np.concatenate([radar_data['distance'],distance+np.max(radar_data['distance'])+inc_dist])
            radar_data['im_end'].append(len(radar_data['distance']))
            radar_data['orig_ind'] = np.concatenate([radar_data['orig_ind'],np.arange(comp_dists['index'][0],len(distance))])
            radar_data['filename'].append(fn_temp.split('/')[-1])
            
            radar_data['Data'] = np.concatenate([radar_data['Data'],radar_data_temp['Data']],axis=1)
            radar_data['Tomo']['img'] = np.concatenate([radar_data['Tomo']['img'],radar_data_temp['Tomo']['img']],axis=2)
            
            for concat_keys in concat_list:
                radar_data[concat_keys] = np.concatenate([radar_data[concat_keys],radar_data_temp[concat_keys]])
            
    
    return radar_data