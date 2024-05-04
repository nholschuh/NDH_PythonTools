################ This is the import statement required to reference scripts within the package
import os,sys,glob
ndh_tools_path_opts = [
    '/mnt/data01/Code/',
    '/home/common/HolschuhLab/Code/'
]
for i in ndh_tools_path_opts:
    if os.path.isfile(i): sys.path.append(i)
################################################################################################

from collections.abc import Iterable
import numpy as np
import NDH_Tools as ndh


def cresis_dataaggregator(filelist,remove_totaldata=0,savename='',depthcap=0,at_samples=[],at_samples_type=0):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % This function can take a list of CReSIS Radar files and extract the relevent bits     
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %    filelist - list of filenames to read
    %    remove_totaldata - flag [0 or 1] which dictates whether or not to preserve the radargrams
    %    savename - a string for the name of the .mat file to write
    %    depthcap - an index for the maximum depth sample to include
    %    at_samples - list of lists, including the start and end along-track sample to use, or a an
    %                 outline to act as bouunds for the aggregated data
    %    at_samples_type - 0 is defined indecies, 1 is an outline
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %    save_dict - dictionary containing:
    %       Data_Vals: The array with coordinate and profile information
    %       DV_Info: Metadata describing the columns in Data_Vals
    %       start_indecies: The index within the larger data array when each new file starts
    %       filenames: The original filenames included in the aggregation
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """     
    print_flag = 0
    start_flag = 1
    filenames = []
    Aggregated_Data = []
    start_indecies = [0]
    Data_Vals = []
    
    ###################### We loop through the list of input files
    for f_ind,fn in enumerate(filelist):
    
        radar_data = ndh.loadmat(fn)
        final_varlist = []
    
        ################## We create a Bottom object if needed
        if 'Surface' not in radar_data.keys():
            radar_data['Surface'] = radar_data['Latitude'].copy()*np.NaN
        if 'Bottom' not in radar_data.keys():
            radar_data['Bottom'] = radar_data['Surface'].copy()*np.NaN
    
        ################## Calculate Polarstereo coordinates
        xy = ndh.polarstereo_fwd(radar_data['Latitude'], radar_data['Longitude'])
        radar_data['x'] = xy['x']
        radar_data['y'] = xy['y']
        radar_data['distance'] = ndh.polarstereo_fwd(radar_data['x'],radar_data['y'])
        final_varlist.append('x')
        final_varlist.append('y')
    
        ################## We apply the depthcap, if prescribed
        if depthcap > 0:
            radar_data['Data'] = radar_data['Data'][:depthcap,:]
            radar_data['Time'] = radar_data['Time'][:depthcap]
            
        ################## This object is used to subset along tack, if requested
        if len(at_samples) == 0:
            trace_index = np.arange(0,len(radar_data['Latitude']))
        else:
            if at_samples_type == 0:
                trace_index = np.arange(at_samples[f_ind][0],at_samples[f_ind][1]+1)
            else:
                trace_index = np.where(ndh.within(np.stack([radar_data['x'],radar_data['y']]).T,at_samples))[0]
            radar_data['Data'] = radar_data['Data'][:,trace_index]
    
        ################## All objects that are the same shape as latitude get subset
        orig_len = len(radar_data['Latitude'])
        for key_opt in radar_data.keys():
            if isinstance(radar_data[key_opt],type(radar_data['Latitude'])):
                shape_array = np.array(radar_data[key_opt].shape)
                if len(shape_array) > 0:
                    if np.max(shape_array == orig_len) == 1:
                        final_varlist.append(key_opt)
        
        for kk in final_varlist:
            if len(radar_data[kk]) == orig_len:
                radar_data[kk] = radar_data[kk][trace_index]
    
        ################## Here we extract date info from the filename
        fn_parts = fn.split('/')[-1].split('.')[0].split('_')
        
        year = int(fn_parts[1][0:4])
        month = int(fn_parts[1][4:6])
        day = int(fn_parts[1][6:8])
        seg = int(fn_parts[2])
        frm = int(fn_parts[3])
        file_ind = f_ind
    
    
        ################## Then, we try and construct the object and concatenate everything. Some files had trouble with this
        temp_Data_Vals = np.vstack((radar_data['x'],radar_data['y'],radar_data['Latitude'],radar_data['Longitude'],radar_data['Elevation'],
                                    radar_data['Surface'],radar_data['Bottom'],radar_data['GPS_time'],trace_index,
                                    np.ones(radar_data['Latitude'].shape)*year, np.ones(radar_data['Latitude'].shape)*month, np.ones(radar_data['Latitude'].shape)*day, 
                                    np.ones(radar_data['Latitude'].shape)*seg, np.ones(radar_data['Latitude'].shape)*frm, np.ones(radar_data['Latitude'].shape)*file_ind)).T
    
        ################## The initial file starts the objects, subsequent files add to them
        if start_flag > 1:
            Data_Vals = np.concatenate((Data_Vals, temp_Data_Vals), axis=0)
            if print_flag == 1:
                print('Completed File '+str(f_ind)+' - '+fn)
        else:
            start_indecies = [0]
            Data_Vals = temp_Data_Vals
            start_flag = start_flag+1
            if print_flag == 1:
                print('Started with file '+str(f_ind)+' - '+fn)
    
        ################## The start index for each new file is logged, along with the file name
        start_indecies.append(start_indecies[-1] + len(trace_index))
        filenames.append(fn)
    
        ################## Finally, the radargrams are appended if desired
        if remove_totaldata == 0:
            Aggregated_Data.append([radar_data['Data'],radar_data['distance'],radar_data['Time']])
        
        
    start_indecies = start_indecies[:-1]
    DV_Info = ['X Coordinate (ps)','Y Coordinate (ps)','Latitude','Longitude','Flight Elevation','Surface Pick','Bottom Pick','GPS Time','Trace Index','Year','Month','Day','Segment','Frame','File Index']
    
    save_dict = {'Data_Vals':Data_Vals,'DV_Info':DV_Info,'start_indecies':start_indecies,'filenames':filenames,'Aggregated_Data':Aggregated_Data}
    if len(savename) > 0:
        ndh.savemat(save_dict,savename)
        

    return save_dict


