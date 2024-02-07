################ This is the import statement required to reference scripts within the package
import os,sys,glob
ndh_tools_path_opts = [
    '/mnt/data01/Code/',
    '/home/common/HolschuhLab/Code/'
]
for i in ndh_tools_path_opts:
    if os.path.isfile(i): sys.path.append(i)
################################################################################################


def find_cresisfiles(y,m=0,d=0,seg=0,frame=0):
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
    %     ant1_gre2 - force a particular continent for days where there are surveys in both places
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %     season_out - A dictionary with information about the matching season
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """     
    from datetime import date
    import os
    import sys
    import glob
    sys.path.append('/mnt/data01/Code/')
    import NDH_Tools as ndh

    root_dir = '/mnt/data01/Data/RadarData/CReSIS_Filestructure/ct_data/rds/'
    
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
                
    season = ndh.cresis_season(y,m,d)
    dayseg_str = '%0.4d%0.2d%0.2d_%0.2d' % (y,m,d,seg)
    filestr = 'Data_%s_%0.3d' % (dayseg_str,frm)
    
    processing_types = sorted(glob.glob(root_dir+season['season']+'/*/'))
    search_types = ['standard','music','surf','DEM']
    dir_names = [[],[],[],[]]
    found_files = [[],[],[],[]]
    
    for ind0,ptype in enumerate(search_types):
        type_fdrs,type_fdrs_ind = ndh.str_compare(processing_types,ptype)
    
        for ind1,type_fdr in enumerate(type_fdrs):
            file_opts = sorted(glob.glob(type_fdr+dayseg_str+'/'+filestr+'.mat'))
            for ind2, file_select in enumerate(file_opts):
                found_files[ind0].append(file_select)
                temp_dir_name = file_select.split('/')
                dir_names[ind0].append(temp_dir_name[-3])
    
            #found_files[ind0] = ndh.flatten_list(found_files[ind0]);
    
    found_files = {'standard':found_files[0],'standard_dirs':dir_names[0],
                   'music':found_files[1],'music_dirs':dir_names[1],
                   'surf':found_files[2],'surf_dirs':dir_names[2],
                   'DEM':found_files[3],'DEM_dirs':dir_names[3]}
    
    return found_files
