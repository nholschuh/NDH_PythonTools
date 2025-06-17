################ This is the import statement required to reference scripts within the package
import os,sys,glob
ndh_tools_path_opts = [
    '/mnt/data01/Code/',
    '/home/common/HolschuhLab/Code/'
]
for i in ndh_tools_path_opts:
    if os.path.isfile(i): sys.path.append(i)
################################################################################################



def process_Standard_Season_pickedpdf(picked_files,orig_radar_dir,layer_save, cresis_flag=1, layer_save_type=1, layer_load=''):
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
    %     find_rows_from_fullimageset - Setting this to 1 will search all images to figure out which rows
    %                                   of pixels are within the plot. For use when some of the bottom of radargrams
    %                                   is all white.
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
    import matplotlib.pyplot as plt
    
    from PIL import Image
    import cv2
    
    from tqdm import tqdm, tqdm_notebook

    import NDH_Tools as ndh
    
    deconstruct_dir = 'Picked_Temp'
    deconstruct_flag = 1
    delete_flag = 1
    
    
    ########## Here we actually do the image processing:
    for ind0,fn in enumerate(picked_files):
    
        if layer_save_type == 0:
            save_dir = '/'.join(orig_radar_dir[ind0].split('/')[:-1])+'/'+layer_save[ind0]
        else:
            save_dir = layer_save[ind0]
            
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)
            
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
            day_segs = sorted(glob.glob(orig_radar_dir[ind0]+'/*/'))
            frame_lists = []
            for day_seg in day_segs:
                file_list = sorted(glob.glob(day_seg+'/Data_*.mat'))
                if len(file_list) > 0:
                      ki = [];
                      for ind,i in enumerate(file_list):
                          if i.split('/')[-1][5] != 'i':
                              ki.append(ind)
                      file_list = ndh.index_list(file_list,ki)
                else:
                      file_list = sorted(glob.glob(day_seg+'/*.mat'))
                    
                frame_lists.append(sorted(file_list))
                    
    
            
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
    
            im_handle = Image.open(frame_fn)
            np_frame = np.array(im_handle).astype(float)
    
            ########## Handling the solid white image
            if len(np_frame.shape) == 2:
                ##########
                print('Empty Frame -- Reshaping')
                np_frame = np.stack([np_frame,np_frame,np_frame,np_frame])
        
            else:
                ########## Identify the rows and columns to extract from and the frame breaks
                color_totals_cols = np.sum(np_frame,axis=0)
                color_totals_rows = np.sum(np_frame,axis=1)
                
                keep_rows = np.where(color_totals_rows[:,1] != color_totals_rows[:,3])[0]
                keep_cols = np.where(color_totals_cols[:,1] != color_totals_cols[:,3])[0]
    
                ######### Find the pixels associated with frame breaks, which are green
                frame_breaks = np.where((color_totals_cols[:,1] - color_totals_cols[:,0]) > color_totals_cols[:,3]*0.5)[0]
                frame_breaks = np.concatenate([[keep_cols[0]],frame_breaks,[keep_cols[-1]]])
                if len(frame_breaks) > 1:
                    ki = np.where(np.diff(frame_breaks) > 1)[0]
                    if np.diff(frame_breaks)[-1] != 1:
                        ki = np.concatenate([ki,np.array([len(frame_breaks)-1])])
                    frame_breaks = frame_breaks[ki]
        
                ######### Debug plots for the frame break calculation
                if 0:
                    plt.subplot(2,1,1)
                    plt.plot(color_totals_cols)
                    plt.plot(keep_cols,np.ones(keep_cols.shape)*200000)
                    for fb in frame_breaks:
                        plt.axvline(fb,c='blue',ls=':',lw=1)
                    
                    plt.subplot(2,1,2)
                    plt.plot(color_totals_rows)
                    plt.plot(keep_rows,np.ones(keep_rows.shape)*200000)
    
            ######### These are used for pixel identification, the number here really just defines the resolution of selection
            original_width = 10000
            original_height = 10000
    
            ######### Frame_break output x values:
            frame_breaks_x = (frame_breaks - keep_cols[0])/(keep_cols[-1]-keep_cols[0])*original_width
            
            picks = ndh.find_pixelcoords(frame_fn,original_width,original_height,im_pick_params=[[2,20,1,10,1]], predefined_row_inds=ndh.minmax(keep_rows)) 
            
        ##########################################################################################################
        # Part 6 #################################################################################################
        ########## Here we put pixel information in its final objects
    
        
            if len(picks) > 0:
                if len(picks[0]) > 0:
                    good_frames.append(ind1)
                    surfaces = picks[0]
    
                    ########## We loop through surfaces to figure out which frames are in play:
                    associated_frames = []
                    for ind2,i in enumerate(surfaces): 
                        xinds = ndh.minmax(i[:,0])
                        min_frame = np.where(frame_breaks_x < xinds[0])[0]
                        if len(min_frame) == 0:
                            min_frame = 0
                        else:
                            min_frame = min_frame[-1]
                            
                        max_frame = np.where(frame_breaks_x < xinds[1])[0]
                        if len(max_frame) == 0:
                            max_frame = 0
                        else:
                            max_frame = max_frame[-1]
                        associated_frames.append(np.arange(min_frame,max_frame+1))
    
                    ########## Now we construct an object to loop through the associated FRAMES that are relevant:
                    all_picked_frames = np.unique(ndh.flatten_list(associated_frames))
                    associated_surfaces = []
                    for frame_opt in all_picked_frames:
                        surf_temp_list = []
                        for ind2,surf_associated_frames in enumerate(associated_frames):
                            if frame_opt in surf_associated_frames:
                                surf_temp_list.append(ind2)
                        associated_surfaces.append(surf_temp_list)
    
                    ########## Here, we loop through those frames
                    for ind2,surf_inds in enumerate(associated_surfaces):
                        source_frame_ind = all_picked_frames[ind2]
                        source_frame_fn = frame_lists[ind1][source_frame_ind]
    
                        deep_savedir = save_dir+'/'+source_frame_fn.split('/')[-2]
                        save_fn = save_dir+'/'+'/'.join(source_frame_fn.split('/')[-2:])
                        if not os.path.isdir(deep_savedir):
                            os.makedirs(deep_savedir)
    
                        
                        frame_data = ndh.loadmat(source_frame_fn)
                        layer_data = {'picks':[],'Latitude':frame_data['Latitude'],'Longitude':frame_data['Longitude'],
                                  'Elevation':frame_data['Elevation'],'Surface':frame_data['Surface'],'Bottom':frame_data['Bottom']}
                        
                        for ind3,surf_ind in enumerate(surf_inds):
                            
                            target_surf = surfaces[surf_ind]
                            frame_width = len(layer_data['Latitude'])
                            frame_height = len(frame_data['Time'])
    
                            if len(target_surf[:,0]) > 1:
                                ############ Convert the arbitrary coordinates to in-frame coordinates
                                frame_xs_1 = (frame_breaks_x[source_frame_ind]-frame_breaks_x[0])/(frame_breaks_x[-1]-frame_breaks_x[0])*original_width
                                frame_xs_2 = (frame_breaks_x[source_frame_ind+1]-frame_breaks_x[0])/(frame_breaks_x[-1]-frame_breaks_x[0])*original_width
                                true_frame_inds = (target_surf[:,0]-frame_xs_1)/(frame_xs_2-frame_xs_1)*frame_width
        
                                interp_frame_inds = np.arange(np.min(true_frame_inds),np.max(true_frame_inds))
                                if np.max(interp_frame_inds) > len(layer_data['Latitude']):
                                    interp_frame_inds = interp_frame_inds[interp_frame_inds < len(layer_data['Latitude'])]
        
                                true_frame_time_inds = target_surf[:,1]/original_height*frame_height
                                interp_time_inds = np.interp(interp_frame_inds,true_frame_inds,true_frame_time_inds)
                                
                                layer_times = frame_data['Time'][interp_time_inds.astype(int)]
                                ki = interp_frame_inds.astype(int)          
        
                                twtt_temp = np.ones(layer_data['Latitude'].shape)*np.nan
                                twtt_temp[ki] = layer_times
                                layer_data['picks'].append(twtt_temp)
       
                        ndh.savemat(layer_data,save_fn)
                else:
                    empty_frames.append(ind1)
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
        