import os
import numpy as np
import tqdm
import glob

################## NDH Tools self imports
###########################################################
from .find_cresisfiles import find_cresisfiles
from .index_list import index_list
from .str_compare import str_compare
###########################################################

def cresis_processing_string(filelist,collate=0,excludes=[],param_dir='/mnt/NDH_data/Google_Drive2/Research_Projects/00_CresisData/opr_params/'):
    """
    % (C) Nick Holschuh - Amherst College - 2025 (Nick.Holschuh@gmail.com)
    % This function creates a typical processing loop string for use with OPR
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %      filelist -- list of files to reprocess
    %      collate=0 -- set to 1 if used for tomo.collate run
    """
    param_spreadsheets = glob.glob(param_dir+'*rds*')

    ki = []
    for ind0,fn in enumerate(filelist):
        skipflag=0
        for exclude in excludes:
            if exclude in fn:
                skipflag=1
        if skipflag == 0:
            ki.append(ind0)
    filelist = index_list(filelist,ki)

    if collate == 0:
        seasons = []
        seg_ids = []
        frames = []
        for fn in tqdm.tqdm(filelist):
            true_fn = find_cresisfiles(fn)
            seasons.append(true_fn['standard'][0].split('/')[-4])
            seg_ids.append(true_fn['standard'][0].split('/')[-2])
            frames.append(int(true_fn['standard'][0].split('/')[-1].split('_')[-1].split('.')[0]))
        
        for ind0,season in enumerate(np.unique(seasons)):
            season_name,wi = str_compare(seasons,season)
            unique_seg_ids = sorted(np.unique(index_list(seg_ids,wi)))
        
            ####### Get the season name
            ssname,ssind = str_compare(param_spreadsheets,season)
            try:
                ssname = ssname[0].split('/')[-1]
                param_ss_string = 'param_ssheet_name = \''+ssname+'\';'
                
                seg_id_string = 'seg_id_list = {\''
                frame_id_string = 'frame_id_list = {'
                
                for ind1,seg_id in enumerate(unique_seg_ids):
                    frame_names,frame_inds = str_compare(seg_ids,seg_id)
                    seg_id_string = seg_id_string+seg_id+'\', \''
                    frame_id_string = frame_id_string+'\'['
            
                    unique_frames = sorted(np.unique(index_list(frames,frame_inds)))
            
                    for ind2,frame_ind in enumerate(unique_frames):
                        frame_id_string = frame_id_string+str(frame_ind)+','
                    frame_id_string = frame_id_string[:-1]+']\','
            
                seg_id_string = seg_id_string[:-3]+'};'
                frame_id_string = frame_id_string[:-1]+'};'
            
                print(' ')
                print(param_ss_string)
                print(seg_id_string)
                print(frame_id_string)
            except:
                print('Coulding find parameter spreadsheet for '+season)
    else:
        #######################################
        ### Create objects to copy for tomo_collate
        
        ########### Get the unique seasons, and store seg_ids and frames
        seasons = []
        seg_ids = []
        frames = []
        for fn in tqdm.tqdm(filelist):
            true_fn = find_cresisfiles(fn)
            seasons.append(true_fn['standard'][0].split('/')[-4])
            seg_ids.append(true_fn['standard'][0].split('/')[-2])
            frames.append(int(true_fn['standard'][0].split('/')[-1].split('_')[-1].split('.')[0]))
        

        seg_id_string = 'seg_id_lists = {\''
        frame_id_string = 'frame_id_lists = {'
        param_ss_string = 'param_ssheet_names = {\''
        
        for ind0,season in enumerate(np.unique(seasons)):
            season_name,wi = str_compare(seasons,season)
            unique_seg_ids = sorted(np.unique(index_list(seg_ids,wi)))
        
            ####### Get the season name
            ssname,ssind = str_compare(param_spreadsheets,season)
            try:
                ssname = ssname[0].split('/')[-1]
                
                
                for ind1,seg_id in enumerate(unique_seg_ids):
                    frame_names,frame_inds = str_compare(seg_ids,seg_id)
            
                    param_ss_string = param_ss_string+ssname+'\',\''
                    seg_id_string = seg_id_string+seg_id+'\', \''
                    frame_id_string = frame_id_string+'['
            
                    unique_frames = sorted(np.unique(index_list(frames,frame_inds)))
            
                    for ind2,frame_ind in enumerate(unique_frames):
                        frame_id_string = frame_id_string+str(frame_ind)+','
                    frame_id_string = frame_id_string[:-1]+'],'
            except:
                print('Coulding find parameter spreadsheet for '+season)
        
        seg_id_string = seg_id_string[:-3]+'};'
        frame_id_string = frame_id_string[:-1]+'};'
        param_ss_string = param_ss_string[:-1]+'};'
        
        print(' ')
        print(param_ss_string)
        print(seg_id_string)
        print(frame_id_string)
