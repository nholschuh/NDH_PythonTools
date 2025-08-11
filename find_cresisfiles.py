from datetime import date
import os
import sys
import glob

################## NDH Tools self imports
###########################################################
from .cresis_season import cresis_season
from .str_compare import str_compare
###########################################################

def find_cresisfiles(y,m=0,d=0,seg=0,frm=0,plus_or_minus_frames=0):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    %     This function finds the season name associated with a flight day
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     y - either the year, or a string for the filename you want the season for
    %     m - the month
    %     d - the day
    %     seg - the segment number
    %     frm - the frame number
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %     season_out - A dictionary with information about the matching season
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """     

    root_dir_opts = ['/mnt/data01/Data/RadarData/CReSIS_Filestructure/ct_data/rds/',
                     '/home/common/HolschuhLab/Data/RadarData/',
                    '/kucresis/scratch/dataproducts/opr_data/rds/']
    
    for rd in root_dir_opts:
        if os.path.isdir(rd):
            root_dir = rd
            break

    if 'root_dir' not in locals():
        raise Exception("There doesn't appear to be any radar directory")
    
    if isinstance(y,str) == 1:
        if y[0] == 'D':
            seg = int(y[14:16])
            frm = int(y[17:20])
            m = int(y[9:11])
            d = int(y[11:13])
            y = int(y[5:9])
        else:
            seg = int(y[9:11])
            frm = int(y[13:16])
            m = int(y[4:6])
            d = int(y[6:8])    
            y = int(y[0:4])

    frm = frm+plus_or_minus_frames
                
    season = cresis_season(y,m,d)
    dayseg_str = '%0.4d%0.2d%0.2d_%0.2d' % (y,m,d,seg)
    filestr = 'Data_%s_%0.3d' % (dayseg_str,frm)
    
    processing_types = sorted(glob.glob(root_dir+season['season']+'/*/'))
    search_types = ['qlook','standard','music','surf','DEM']

    dir_names = [[],[],[],[],[]]
    found_files = [[],[],[],[],[]]
    
    for ind0,ptype in enumerate(search_types):
        type_fdrs,type_fdrs_ind = str_compare(processing_types,ptype)
    
        for ind1,type_fdr in enumerate(type_fdrs):
            if ind0 < 4:
                file_opts = sorted(glob.glob(type_fdr+dayseg_str+'/'+filestr+'.mat'))
            else:
                file_opts = sorted(glob.glob(type_fdr+dayseg_str+'/'+'_'.join(filestr.split('_')[1:])+'_bottom.mat'))
                                   
            for ind2, file_select in enumerate(file_opts):
                found_files[ind0].append(file_select)
                temp_dir_name = file_select.split('/')
                dir_names[ind0].append(temp_dir_name[-3])
    
    
    found_files = {'qlook':found_files[0],'qlook_dirs':dir_names[0],
                   'standard':found_files[1],'standard_dirs':dir_names[1],
                   'music':found_files[2],'music_dirs':dir_names[2],
                   'surf':found_files[3],'surf_dirs':dir_names[3],
                   'DEM':found_files[4],'DEM_dirs':dir_names[4]}
    
    return found_files
