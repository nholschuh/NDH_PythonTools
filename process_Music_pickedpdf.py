################ This is the import statement required to reference scripts within the package
import os,sys,glob
ndh_tools_path_opts = [
    '/mnt/data01/Code/',
    '/home/common/HolschuhLab/Code/'
]
for i in ndh_tools_path_opts:
    if os.path.isfile(i): sys.path.append(i)
################################################################################################


from tqdm import tqdm, tqdm_notebook
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
import NDH_Tools as ndh


def process_Music_pickedpdf(fn,data_dir,surf_load,music_load,surf_save,only_edgetrims=0,remove_framedir=1):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    %     This function takes a picked PDF for a MUSIC image and digitizes 
    %     the picked layers and associated edgetrims
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %       fn -- The name of the picked pdf file to process
    %       data_dir -- The directory that contains the season information for the file
    %       surf_load -- The name (eg. CSARP_surf_ndh) that loads in the original surface files
    %       music_load -- The name (eg. CSARP_music3D_ndh) that loads in the original music files
    %       surf_save --  The name of the directory you want to save the new surf files into (CSARP_surf_iPad)
    %       only_edgetrims -- [0] In case you only want to extract the edge-trim values    
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %       This will save a new surf file into the "surf_save" directory. Because of some funny ways
    %       Python saves .mat files, you need to run a complementary matlab function on your picked files afterward
    %       "XXXXXXXXXXX"
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 
    ########## Here we actually do the image processing:
    if not os.path.isdir(data_dir+surf_save):
        os.makedirs(data_dir+surf_save)
    
    
    ##########################################################################################################
    # Part 1 ##################################################################################################
    ######## Here we parse the name for the file information and the image specifications
    local_fn_whole = fn.split('/')[-1]
    fileparts = local_fn_whole.split('.')[0].split('_')

    fs = int(fileparts[5])
    crop = int(fileparts[7])
    day_seg = '_'.join(fileparts[1:3])
    local_fn = '_'.join(fileparts[0:4])

    ##########################################################################################################
    # Part 2 #################################################################################################
    ######## Here we load in the original surf files for modification
    surf_fn = data_dir+surf_load+'/'+day_seg+'/'+local_fn+'.mat'
    music_fn = data_dir+music_load+'/'+day_seg+'/'+local_fn+'.mat'
    surf_data = ndh.loadmat(surf_fn)
    times = ndh.loadmat(music_fn,['Time'])['Time'][0]
    surf_pick = np.ones(surf_data['surf']['y'][3].shape)*np.NaN

    ######## These are the properties of the original file that need to be provided to the image processing
    original_width = len(surf_pick[:,0])
    original_height = crop

    ##########################################################################################################
    # Part 3 #################################################################################################
    ######## Here we define the objects that need to be populated with picks
    bottom_picks = surf_data['surf']['y'][3]
    edge_trim = np.ones(surf_data['surf']['y'][3].shape)*np.NaN
    debris_edge = []
    debris_picks = []
    for i in range(4):
        debris_picks.append(np.ones(surf_data['surf']['y'][3].shape)*np.NaN)
        debris_edge.append(np.ones(surf_data['surf']['y'][3].shape)*np.NaN)

    ##########################################################################################################
    # Part 4 ###################################################################################################
    ########## The following converts a pdf to multiple images
    print('Starting the pdf deconstruction for: '+local_fn)
    
    comb_deconstruct_dir = '/'.join(fn.split('/')[0:-1])+'/temp_frame_deconstruction/'
    if os.path.isdir(comb_deconstruct_dir) == 0:
        os.makedirs(comb_deconstruct_dir)
    
    os_cmd = 'convert -quality 20 -density 144 %s %s/%s' % (fn,comb_deconstruct_dir,'Frame_%03d.png')
    os.system(os_cmd)
    frame_list = sorted(glob.glob(comb_deconstruct_dir+'/*.png'))

    ##########################################################################################################
    # Part 5 ##################################################################################################
    print('Starting the information extraction.')
    ########## Here we actually load the images and extract pixel coordinate information
    error_frames = []
    error_lengths = []
    error_data = []
    error_ims = []
    error_fns = []
    
    for ind1,frame_fn in enumerate(tqdm(frame_list)):
        ################## Here is where the actual pixel information gets extracted
    
        #################################################
        ## IF YOU GET A FEW ERROR FRAMES                #
        ## The best thing to do is probably adjust the  #
        ## distance threshold for pixel combination or  #
        ## the minimum number of pixels in an edge trim.#
        ## These are the 4th and 2nd pick params        #
        #################################################

        picks = ndh.find_pixelcoords(frame_fn,original_width,original_height,im_pick_params=[[0,20,0,70,2],[2,25,1,10,1]])  
        pixel_run_str =         'picks = ndh.find_pixelcoords(frame_fn,%d,%d,im_pick_params=[[0,20,0,70,2],[2,25,1,10,1]])' % (original_width,original_height)

    ##########################################################################################################
    # Part 6 #################################################################################################
        edges = picks[0]
        center_val = np.median(np.array(edges)[:,0])
        left_edge = []
        left_time = []
        right_edge = []
        right_time = []
        for ind2,i in enumerate(edges):
            if i[0] > center_val:
                right_time.append(times[int(i[1])])
                right_edge.append(i[0])
            else:
                left_time.append(times[int(i[1])])
                left_edge.append(i[0])
                
        left_order = np.squeeze(np.argsort(left_time)[::-1])
        right_order = np.squeeze(np.argsort(right_time)[::-1])
        
        if left_order.ndim == 0:
            left_order = np.expand_dims(left_order,0)
        if right_order.ndim == 0:
            right_order = np.expand_dims(right_order,0)
            
        surfaces = picks[1]
        max_surf_depth = []
        surfaces_time = []
        for ind2,i in enumerate(surfaces):
            surfaces_time.append(times[i[:,1].astype(int)])
            max_surf_depth.append(np.max(surfaces_time[-1]))
        surf_order = np.argsort(max_surf_depth)[::-1]
        ############## For the case where more than one layer is picked
        if np.all([len(edges)/2 != len(surfaces), only_edgetrims == 0]):
            error_frames.append(ind1)
            error_lengths.append([len(edges),len(surfaces)])
            error_data.append([picks])
            error_ims.append(np.array(Image.open(frame_fn)))
            error_fns.append(frame_fn)
    
        elif np.all([np.mod(len(edges),2) == 1, only_edgetrims == 1]):
            error_frames.append(ind1)
            error_lengths.append([len(edges),len(surfaces)])
            error_data.append([picks])
            error_ims.append(np.array(Image.open(frame_fn)))
            error_fns.append(frame_fn)    
            
        else:
            ############ Add the entries to the proper objects        
            for ind2,i in enumerate(left_order):
                if ind2 == 0:
                    edge_trim[int(left_edge[i]),ind1*fs] = left_time[i] 
                    edge_trim[int(right_edge[i]),ind1*fs] = right_time[i] 
                else:
                    if only_edgetrims == 0:
                        debris_edge[ind2-1][int(left_edge[i]),ind1*fs] = left_time[i] 
                        debris_edge[ind2-1][int(right_edge[i]),ind1*fs] = right_time[i] 
    
            ############ Here the surfs get populated (or ignored, if desired)
            if only_edgetrims == 0:
                for ind2,i in enumerate(surf_order):
                    for ind3 in range(len(surfaces[i])):
                        if ind2 == 0:
                            bottom_picks[int(surfaces[i][ind3][0]),ind1*fs] = surfaces_time[i][ind3]  
                        else:
                            debris_picks[ind2-1][int(surfaces[i][ind3][0]),ind1*fs] = surfaces_time[i][ind3]  
                        
            os_cmd = 'rm %s' % (frame_fn)
            os.system(os_cmd)
    ##########################################################################################################
    # Part 7 #################################################################################################
    ########## Here we clean up the temporary directory and save the output
    if remove_framedir != 1:
        os_cmd = 'rm -r %s' % (comb_deconstruct_dir[:-1])
        print('When ready, run:     '+os_cmd)
        print(' ')
    
    if len(error_frames) > 0:
        print('To test the pixelcoords function, run:')
        print(pixel_run_str)
        print(' ')
        print('Some frames had errors: ',error_frames)
        for ind1, i in enumerate(error_frames):
            print(str(i)+':', error_lengths[ind1])


    ######### The application of ground truth can't handle a pick in every column. Here
    ######### we downselect the GT objects to include only every other value:
    center_ind = np.where(np.max(np.sum(~np.isnan(surf_data['surf']['y'][3]),1)) == np.sum(~np.isnan(surf_data['surf']['y'][3]),1))[0]
    rep_spacing = 2;
    start_rep = np.mod(center_ind,rep_spacing)+1
    rep_rows = np.arange(start_rep,len(bottom_picks[:,0]),rep_spacing)
    bottom_picks[rep_rows,:] = np.NaN
    for ind1 in range(len(debris_picks)):
        debris_picks[ind1][rep_rows,:] = np.NaN


    ######### Here we actually save the files
    if not os.path.isdir(data_dir+surf_save+'/'+day_seg):
        os.makedirs(data_dir+surf_save+'/'+day_seg)
    
    if only_edgetrims == 0:
        surf_data['surf']['y'][3] = bottom_picks
        
    surf_data['surf']['y'][7] = edge_trim
    surf_data['surf']['name'][7] = 'EdgeTrim'
    ndh.savemat(dict(surf_data),data_dir+surf_save+'/'+day_seg+'/'+local_fn+'.mat')    
    
    ############ In the event that there are more than one picked horizon
    if len(debris_edge) > 0:
        surf_debris = ['CSARP_surf_debris_01','CSARP_surf_debris_02','CSARP_surf_debris_03','CSARP_surf_debris_04']
        for i in surf_debris:
            if not os.path.isdir(data_dir+i):
                os.makedirs(data_dir+i)        
    
    for ind1 in range(len(debris_edge)):
        if len(np.where(~np.isnan(debris_picks[ind1]))[0]) > 0:
            if not os.path.isdir(data_dir+surf_debris[ind1]+'/'+day_seg):
                os.makedirs(data_dir+surf_debris[ind1]+'/'+day_seg)
            else:
                pass
            surf_data['surf']['y'][3] = debris_picks[ind1]
            surf_data['surf']['y'][7] = debris_edge[ind1]
            ndh.savemat(surf_data,data_dir+surf_debris[ind1]+'/'+day_seg+'/'+local_fn+'.mat')
    
    error_dict = {'frame_num':error_frames,'edge_and_surf_lengths':error_lengths,'picks':error_data,'images':error_ims,'frame_fns':error_fns}

    
    return surf_data,error_dict