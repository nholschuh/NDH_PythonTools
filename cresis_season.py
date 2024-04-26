################ This is the import statement required to reference scripts within the package
import os,sys,glob
ndh_tools_path_opts = [
    '/mnt/data01/Code/',
    '/home/common/HolschuhLab/Code/'
]
for i in ndh_tools_path_opts:
    if os.path.isfile(i): sys.path.append(i)
################################################################################################


def cresis_season(y,m=0,d=0,ant1_gre2=1):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    %     This function finds the season name associated with a flight day.
    % There are a small number of flight days in which two campaigns
    % were running apparently. By default, this code will assume you want
    % the Antarctic Season. You can force it to take the greenland season using
    % the given flag.
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
    import numpy as np
    import os
    import sys
    import glob
    sys.path.append('/mnt/data01/Code/')
    import NDH_Tools as ndh

    ########################### Here we find the season metadata. This file was produced
    ########################### from an external matlab script
    season_metadata_dirs = [
        '/mnt/data01/Data/RadarData/CReSIS_Filestructure/'
    ]
    for i in season_metadata_dirs:
        if os.path.isdir(i): season_metadata_path=i


    season_opts = ndh.loadmat(season_metadata_path+'season_metadata.mat')
    
    if isinstance(y,str) == 1:
        if y[0] == 'D':
            m = int(y[9:11])
            d = int(y[11:13])
            y = int(y[5:9])
        else:
            m = int(y[4:6])
            d = int(y[6:8])    
            y = int(y[0:4])
    
    target_date = date.toordinal(date(y,m,d))
    
    full_dates = np.concatenate([season_opts['a_dates'],season_opts['g_dates']])
    ############### Matlab starts at year 0, python at year 1. So there is a 1 year offset applied here
    full_dates[:,0] = full_dates[:,0]-366
    full_dates = np.concatenate([full_dates,np.expand_dims(np.concatenate([np.ones(len(season_opts['a_dates'][:,0])),
                                           np.ones(len(season_opts['g_dates'][:,0]))*2]),0).T],1)
    
    match_ind = np.where(full_dates[:,0] == target_date)[0]
    exact_flag = 1;
    
    if ant1_gre2 == 1:
        if len(match_ind) > 1:
            match_ind = match_ind[0]
    else:
         if len(match_ind) > 1:
            match_ind = match_ind[1]   
        
    if len(match_ind) == 0:
        match_ind = ndh.find_nearest(full_dates[:,0],target_date);
        match_ind = match_ind['index'][0]
        exact_flag = 0;
    
    ############### You have to subtract one from the match ind to deal with matlabs indexing
    if full_dates[match_ind,2] == 1:
        season_out = season_opts['a_names'][int(full_dates[match_ind,1]-1)]
    else:
        season_out = season_opts['g_names'][int(full_dates[match_ind,1]-1)]
        
    if exact_flag == 0:
        print('No exact match was found -- closest suggested season is the following: '+season_out[0])
    
    season_out = {'exact_match':exact_flag,'season':season_out[0],'data_dir':season_out[1],'Date':season_out[2]}
    return season_out
