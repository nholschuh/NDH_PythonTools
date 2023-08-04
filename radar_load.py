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


def radar_load(fn,plot_flag=0,elevation1_or_depth2=1):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    %     This function does the standard load, transformation, and plotting
    %     that is common in the CReSIS radar analysis workflow
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     fn -- the input filename to be read
    %     plot_flag -- 0 or 1, for whether or not you want a plot included, or 2 for the plotting code to be printed
    %     elevation1_or_depth2 -- there is a depth conversion that is built in, 1 if you want true elevation, 2 for depth in ice
    %                             0 will give you an empty object
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %     radar_data -- the simple product of loading the mat file (+ x and y coordinates and distance added)
    %     depth_data -- the depth or elevation product
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 

    
    import NDH_Tools as ndh
    
    radar_data = ndh.loadmat(fn);
    xy = ndh.polarstereo_fwd(radar_data['Latitude'],radar_data['Longitude'])
    distance = ndh.distance_vector(xy['x'],xy['y'])
    radar_data['x'] = xy['x']
    radar_data['y'] = xy['y']
    radar_data['distance'] = distance
    
    if elevation1_or_depth2 == 0:
        depth_data = 'No depth data requested'     
    elif elevation1_or_depth2 == 1:
        depth_data = ndh.elevation_shift(radar_data['Data'],radar_data['Time'],radar_data['Surface'],radar_data['Elevation'],radar_data['Bottom'])
    elif elevation1_or_depth2 == 2:
        depth_data = ndh.depth_shift(radar_data['Data'],radar_data['Time'],radar_data['Surface'],radar_data['Elevation'],radar_data['Bottom'])
        
    if plot_flag == 1:
        
        if elevation1_or_depth2 == 0:
            bot_inds = ndh.find_nearest(radar_data['Time'],radar_data['Bottom'])
            bot_ind = np.nanmax(bot_inds['index'])+100
            
            fig = plt.figure(figsize=(15,7))
            imdata = plt.imshow(np.log10(radar_data['Data'][:bot_ind,:]),
                                origin='lower',aspect='auto',cmap='gray_r')
            ax = plt.gca()        
            ax.invert_yaxis()
            
        else:
            fig = plt.figure(figsize=(7,15))
            imdata = plt.imshow(np.log10(depth_data['new_data']),
                                extent=[radar_data['distance'][0]/1000,radar_data['distance'][-1]/1000,
                                        depth_data['depth_axis'][0],depth_data['depth_axis'][-1]],
                                origin='lower',aspect='auto',cmap='gray_r')
            ax = plt.gca()
            ax.invert_yaxis()
        
    elif plot_flag == 2:
        
        if elevation1_or_depth2 == 0:
            print('''
fig = plt.figure(figsize=(15,7))
imdata = plt.imshow(np.log10(depth_data['new_data']),
                    origin='lower',aspect='auto',cmap='gray_r')
ax = plt.gca() 
            ''')            
        else:
            print('''
fig = plt.figure(figsize=(15,7))
imdata = plt.imshow(np.log10(depth_data['new_data']),
                    extent=[radar_data['distance'][0]/1000,radar_data['distance'][-1]/1000,
                            depth_data['depth_axis'][0],depth_data['depth_axis'][-1]],
                    origin='lower',aspect='auto',cmap='gray_r')        

ax = plt.gca()
ax.invert_yaxis()
            ''')
        
    return radar_data,depth_data