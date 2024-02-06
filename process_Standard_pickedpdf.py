################ This is the import statement required to reference scripts within the package
import os,sys,glob
ndh_tools_path_opts = [
    '/mnt/data01/Code/',
    '/home/common/HolschuhLab/Code/'
]
for i in ndh_tools_path_opts:
    if os.path.isfile(i): sys.path.append(i)
################################################################################################



def process_Standard_pickedpdf(picked_files,orig_radar_dir,layer_save, cresis_flag=1, layer_save_type=1, layer_load=''):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    %     This function extracts annotations from nadir radargrams made on an iPad
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     picked_files - List of filenames of pdfs containing annotations
    %     orig_radar_dir - List of directories that contained the origina radar data files contained in each pdf
    %     layer_save - The name of the directory you want to save layer output to
    %     cresis_flag=1 - If this is a CReSIS file, this should be set to 1, otherwise, 0.
    %     layer_save_type=1 - For most applications, this should be set to 1, which is, save files in your current dir. 
    %                     0 - This allows you to save layer files within the cresis file_tree
    %     layer_load='' - This is not fully implemented, but it would allow you to populate existing layer files
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %     saved files for annotations in each image
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 

    import glob
    import os
    import numpy as np
    
    from PIL import Image
    import cv2
    
    from tqdm import tqdm, tqdm_notebook

    import NDH_Tools as ndh
    
    deconstruct_dir = 'Picked_Temp'
    deconstruct_flag = 1
    delete_flag = 1
    if layer_save_type == 1:
        layer_load=''
    
    ########## Here we actually do the image processing:
    for ind0,fn in enumerate(picked_files):
        
        ##########################################################################################################
        # Part 1 ##################################################################################################
        ######## Here we parse the name for the file information and the image specifications
        local_fn_whole = fn.split('/')[-1]
        fileparts = local_fn_whole.split('.')[0].split('_')
        
        crop = fileparts[-1]
    
        
        ##########################################################################################################
        # Part 2 #################################################################################################
        ######## Here we identify the files we may need to load later
        if cresis_flag == 1:
            day_seg = '_'.join(fileparts[1:3])
            year = day_seg[0:4]
            season = ndh.cresis_season(day_seg)['season']
            standard_fns = sorted(glob.glob(orig_radar_dir[ind0]+'/Data_'+day_seg+'*.mat'))
        else:
            standard_fns = sorted(glob.glob(orig_radar_dir[ind0]+'/*.mat'))
    
        if layer_save_type == 0:
            layer_fns = []
            layer_load_fns = []
            save_dir = '/'.join(standard_fns[0].split('/')[0:-3])+'/'+layer_save
            for ind1,temp_fn in enumerate(standard_fns):
                deconstructed_fn = temp_fn.split('/')
                deconstructed_fn[-3] = layer_save
                layer_fns.append('/'.join(deconstructed_fn))
    
                if len(layer_load) > 0:
                    layer_load_fn_temp = deconstructed_fn
                    layer_load_fn_temp[-3] = layer_load
                    layer_load_fns.append(layer_load_fn_temp)
                    
        elif layer_save_type == 1:
            save_dir = './'+layer_save
            layer_fns = []
            for ind1,temp_fn in enumerate(standard_fns):
                layer_fns.append(save_dir+'/'+temp_fn.split('/')[-1])
            
        ########### Preconstruct directories for use:
        comb_deconstruct_dir = './'+deconstruct_dir
        if not os.path.isdir(comb_deconstruct_dir):
            os.makedirs(comb_deconstruct_dir)
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)
        ##########################################################################################################
        # Part 3 #################################################################################################
        ######## Here we define the objects that need to be populated with picks
    
        ##########################################################################################################
        # Part 4 ###################################################################################################
        ########## The following converts a pdf to multiple images
        if deconstruct_flag == 1:
            print('Starting the pdf deconstruction for: '+local_fn_whole)
            os_cmd = 'convert -quality 20 -density 144 %s %s/%s' % (fn,comb_deconstruct_dir,'Frame_%03d.png')
            os.system(os_cmd)
        frame_list = sorted(glob.glob(comb_deconstruct_dir+'/*.png'))
            
        ##########################################################################################################
        # Part 5 ##################################################################################################
        print('Starting the information extraction.')
        ########## Here we actually load the images and extract pixel coordinate information
        error_frames = []
        good_frames = []
        empty_frames = []
        for ind1,frame_fn in enumerate(tqdm(frame_list)):
            ##### Confirm that file is associated with the right frame
            if '_%0.3d' % (ind1+1) in standard_fns[ind1]:
                frame_data = ndh.loadmat(standard_fns[ind1])
                times = frame_data['Time']
                    
                original_width = len(frame_data['Bottom'])-1
                height_index = ndh.find_nearest(frame_data['Time'],np.nanmax(frame_data['Bottom']))
                
                if crop == 'maxbotplus25':
                    original_height = height_index['index'][0]+25
                elif crop == 'maxbotplus100':
                    original_height = height_index['index'][0]+100
                elif crop == 'nocrop':
                    original_height = len(frame_data['Time'])
                    
                picks = ndh.find_pixelcoords(frame_fn,original_width,original_height,im_pick_params=[[2,25,1,10,1]])  
            else:
                error_frames.append(ind1)
        
        ##########################################################################################################
        # Part 6 #################################################################################################
        ########## Here we put pixel information in its final objects
    
        
            if len(picks[0]) > 0:
    
                good_frames.append(ind1)
                surfaces = picks[0]
                max_surf_depth = []
                surfaces_time = []
                for ind2,i in enumerate(surfaces):
                    surfaces_time.append(times[i[:,1].astype(int)])
                    max_surf_depth.append(np.max(surfaces_time[-1]))
                surf_order = np.argsort(max_surf_depth)[::-1]
                layer_local_fn = standard_fns[ind1].split('/')[-1]
                
                ########## Load or construct the object
                if len(layer_load) == 0:
                    layer_data = {'picks':[],'Latitude':frame_data['Latitude'],'Longitude':frame_data['Longitude'],
                                  'Elevation':frame_data['Elevation'],'Surface':frame_data['Surface'],'Bottom':frame_data['Bottom']}
                elif len(layer_load) > 0:
                    layer_data = ndh.loadmat(layer_load_fns[ind1])
                    layer_ids = layer_data['id']
                    layer_quality = layer_data['quality']
                    layer_twtt = layer_data['twtt']
                    layer_type = layer_data['type']
                    
                    basic_infill_object = np.ones(layer_twtt[0].shape)
                else:
                    error_frames.append(ind1)
                        
                ########## Loop through the layers
                for ind2,i in enumerate(surf_order):
                    layer_times = frame_data['Time'][np.array(surfaces[i]).astype(int)[:,1]]
                    ki = np.array(surfaces[i]).astype(int)[:,0]
                        
                    if layer_save_type == 0:
                        ######## For some reason layer files and the image have different sizes.
                        ######## so we have to interpolate the pick indecies onto the gpstime...
                        ki_times = np.squeeze(frame_data['GPS_time'][ki])
                        ki_layer, new_ki = np.unique(ndh.find_nearest(layer_data['gps_time'],np.squeeze(ki_times))['index'],return_index=True)
    
                        twtt_temp = basic_infill_object*np.nan
                        twtt_temp[ki_layer] = ki_times[new_ki]
    
                        layer_twtt = np.vstack([layer_twtt,twtt_temp])
                        layer_ids = np.append(layer_ids,layer_ids[-1]+1)
                        layer_type = np.vstack([layer_type,basic_infill_object*2])
                        layer_quality = np.vstack([layer_quality,basic_infill_object])
    
                    elif layer_save_type == 1:
                        twtt_temp = np.ones(layer_data['Latitude'].shape)*np.nan
                        twtt_temp[ki] = layer_times
                        layer_data['picks'].append(twtt_temp)
                            
                if layer_save_type == 0:            
                    layer_data['id'] = layer_ids
                    layer_data['quality'] = layer_quality
                    layer_data['twtt'] = layer_twtt
                    layer_data['type'] = layer_type
    
    
                ndh.savemat(layer_data,layer_fns[ind1])
    
            else:
                empty_frames.append(ind1)
       
    
        if len(error_frames) > 0:
            print('Some frames had errors: ',error_frames)
            
        print('These frames had picks: ',good_frames)
        print('These frames were empty: ',empty_frames)
                
            
        ##########################################################################################################
        # Part 7 #################################################################################################
        ########## Here we clean up the temporary directory and save the output
        if delete_flag == 1:
            os_cmd = 'rm -r %s' % (comb_deconstruct_dir)
            os.system(os_cmd)
        