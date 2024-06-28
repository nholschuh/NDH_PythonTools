import numpy as np
import cv2

def crop_radardata(radar_data,start_ind=0,end_ind=0,depth_data=[]):
    """
    % (C) Nick Holschuh - Penn State University - 2015 (Nick.Holschuh@gmail.com)
    % This takes standard output from ndh.radar_load and trims the start and end 
    % of keys in the radar dictionarys, based on the provided start and end_ind
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %     radar_data -- the dictionary that is the output from radar_load
    %     start_ind -- the start index to use in the crop. Should be 0 for no crop.
    %     end_ind -- the end index to use in the crop. 0 for no crop. Can be +/1
    %     depth_data -- the dictionary of depth_shifted data to crop, if desired
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %     radar_data -- cropped radar_data object
    %     depth_data -- cropped depth_data object
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%
    """
    
    if end_ind == 0:
        end_ind = len(radar_data['Latitude'])+1
    elif end_ind < 0:
        end_ind = len(radar_data['Latitude'])+1+end_ind

    target_shape = len(radar_data['Latitude'])
    
    modified_keys = []
    for key_opt in radar_data.keys():
        try:
            orig_shape = radar_data[key_opt].shape
            if radar_data[key_opt].shape[0] == target_shape:
                radar_data[key_opt] = radar_data[key_opt][start_ind:end_ind]
            elif radar_data[key_opt].shape[1] == target_shape:
                radar_data[key_opt] = radar_data[key_opt][:,start_ind:end_ind]
            modified_keys.append(key_opt)
            final_shape = radar_data[key_opt].shape
            #print(orig_shape,final_shape)
        except:
            pass

    for key_opt in depth_data.keys():
        try:
            orig_shape = depth_data[key_opt].shape
            if depth_data[key_opt].shape[0] == target_shape:
                depth_data[key_opt] = depth_data[key_opt][start_ind:end_ind]
            elif depth_data[key_opt].shape[1] == target_shape:
                depth_data[key_opt] = depth_data[key_opt][:,start_ind:end_ind]
            modified_keys.append(key_opt)
            final_shape = depth_data[key_opt].shape
            #print(orig_shape,final_shape)
        except:
            pass

    return radar_data,depth_data

