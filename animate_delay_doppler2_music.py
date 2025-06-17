################ This is the import statement required to reference scripts within the package
import os,sys,glob
ndh_tools_path_opts = [
    '/mnt/data01/Code/',
    '/home/common/HolschuhLab/Code/'
]
for i in ndh_tools_path_opts:
    if os.path.isfile(i): sys.path.append(i)
################################################################################################


import NDH_Tools as ndh
import numpy as np
import matplotlib.pyplot as plt
import tqdm


def animate_delay_doppler2_music(videoname,radar_data,depth_data,music_data1,doppler_data2,doppler_data3,frame_skip,ymax=30,max_amp=0,min_amp=0):
    """
    % (C) Nick Holschuh - Amherst College - 2025 (Nick.Holschuh@gmail.com)
    % This function animates a delay doppler image
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %      radar_data - original radar data loaded with ndh.radar_load
    %      depth_data - radar image with removed air travel time
    %      music_data1 - The music file
    %      doppler_data2 - The SAR focused doppler images
    %      doppler_data3 - The QLook doppler images
    %      target ind - A specific index in the radar image. If 0, calculate over a rolling window
    %      window_size - The number of samples to include in the fft
    %      deg 
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %% animate_delay_doppler(videoname,radar_data,depth_data,doppler_data,frame_skip,ymax=30,center_ind=0,max_amp=0,min_amp=0)
    """

    music_plot_on = 1
    doppler1_plot_on = 1
    doppler2_plot_on = 1

    music_edge_trim = 2
    
    if min_amp == 0:
        min_amp1 = np.nanpercentile(10*np.log10(music_data['Tomo']['img'][::5,::5,::100].ravel()),10)
        min_amp2 = np.nanpercentile(doppler_data2['doppler_data'][::5,::5,::100].ravel(),10)
        if doppler2_plot_on == 1:
            min_amp3 = np.nanpercentile(doppler_data3['doppler_data'][::5,::5,::100].ravel(),10)
    else:
        min_amp1 = min_amp
        min_amp2 = min_amp
        min_amp3 = min_amp
    if max_amp == 0:
        max_amp1 = np.nanpercentile(10*np.log10(music_data['Tomo']['img'][::5,::5,::100].ravel()),99)
        max_amp2 = np.nanpercentile(doppler_data2['doppler_data'][::5,::5,::100].ravel(),99)
        if doppler2_plot_on == 1:
            max_amp3 = np.nanpercentile(doppler_data3['doppler_data'][::5,::5,::100].ravel(),99)
    else:
        max_amp1 = max_amp
        max_amp2 = max_amp
        max_amp3 = max_amp
    
    ############# DelayDoppler Image
    theta_deg1 = np.rad2deg(music_data['Tomo']['theta'][:,0])[:,0]
    theta_deg2 = doppler_data2['slope_axis']
    theta_deg3 = doppler_data3['slope_axis']
    theta_min = np.min([theta_deg2[0],theta_deg3[0]])
    theta_max = np.max([theta_deg2[-1],theta_deg3[-1]])
    

    ############## Initiate the figure
    if music_plot_on + doppler1_plot_on + doppler2_plot_on == 3:
        fig_size = 32
    else:
        fig_size = 24
        
    fig = plt.figure(figsize=(fig_size,8))
    if music_plot_on + doppler1_plot_on + doppler2_plot_on == 3:
        gs = fig.add_gridspec(1,7,wspace=0.2,hspace=1)
    else:
        gs = fig.add_gridspec(1,6,wspace=0.2,hspace=1)
        
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1:5])
    ax3 = fig.add_subplot(gs[5])

    if doppler2_plot_on == 1:
        ax4 = fig.add_subplot(gs[6])
    
    writer = ndh.generate_animation(20)
    
    ############# Identifying the indecies for each dataset for the animation
    ### This is determined from the first doppler dataset
    slide_inds2 = np.arange(0,len(doppler_data2['distance']),frame_skip)
    slide_inds1 = ndh.find_nearest(music_data['distance'],doppler_data2['distance'][slide_inds2])
    slide_inds1 = slide_inds1['index']

    if doppler2_plot_on == 1:
        #slide_inds3 = ndh.find_nearest_xy(doppler_data3['distance'],doppler_data2['distance'][slide_inds2])
        slide_inds3 = ndh.find_nearest_xy(np.stack([doppler_data3['x'],doppler_data3['y']]).T,np.stack([doppler_data2['x'][slide_inds2],doppler_data2['y'][slide_inds2]]).T)
        slide_inds3 = slide_inds3['index']
    
    ############# The nadir image
    ax2.imshow(10*np.log10(np.abs(radar_data['Data'])**2),
                                extent=[radar_data['distance'][0]/1000,radar_data['distance'][-1]/1000,
                                        radar_data['Time'][0]*1e6,radar_data['Time'][-1]*1e6],
                                origin='lower',aspect='auto',cmap='gray_r')
    
    ax2.set_ylim([0,ymax])
    ax2.set_xlabel('Distance (km)')
    ax2.invert_yaxis()
    ax2.set_yticks([])
    ax2.set_title(' '.join(radar_data['filename'])+'  -   Nadir Image')
    ax1.set_title('Direction of Arrival (Along-Track) Image')
    
    with writer.saving(fig, videoname, 100):
        for loop_ind in tqdm.tqdm(np.arange(len(slide_inds1))):
            slide_ind1 = slide_inds1[loop_ind]
            slide_ind2 = slide_inds2[loop_ind]
            if doppler2_plot_on == 1:
                slide_ind3 = slide_inds3[loop_ind]
    
            if music_plot_on == 1:
                ############## The across-track direction of arrival image 1 
                imdata = ax1.imshow(10*np.log10(music_data1['Tomo']['img'][:,music_edge_trim+1:-music_edge_trim,slide_ind1]),
                                    extent=[theta_deg1[music_edge_trim+1],theta_deg1[-music_edge_trim],
                                            music_data1['Time'][0]*1e6,music_data1['Time'][-1]*1e6],
                                    origin='lower',aspect='auto',cmap='gray_r',vmax=max_amp1,vmin=min_amp1)  
    
            if doppler1_plot_on == 1:
                ############## The along-track direction of arrival image 1 
                imdata = ax3.imshow(doppler_data2['doppler_data'][slide_ind2,:,:],
                                    extent=[theta_deg2[0],theta_deg2[-1],
                                            doppler_data2['Time'][0]*1e6,doppler_data2['Time'][-1]*1e6],
                                    origin='lower',aspect='auto',cmap='gray_r',vmax=max_amp2,vmin=min_amp2)   
    
            if doppler2_plot_on == 1:
                ############## The along-track direction of arrival image 2 
                imdata = ax4.imshow(doppler_data3['doppler_data'][slide_ind3,:,:],
                                    extent=[theta_deg3[0],theta_deg3[-1],
                                            doppler_data3['Time'][0]*1e6,doppler_data3['Time'][-1]*1e6],
                                    origin='lower',aspect='auto',cmap='gray_r',vmax=max_amp3,vmin=min_amp3)   
    
            if loop_ind == 0:
                ax1.set_ylim([0,ymax])
                ax1.invert_yaxis()
                ax1.set_xlabel('Direction of Arrival (degrees)')
                ax1.set_ylabel('Two Way Travel Time')
                ax1.set_title('Across-Track Image')
            
                ax3.set_ylim([0,ymax])
                ax3.set_xlim([theta_min,theta_max])
                ax3.invert_yaxis()
                ax3.set_xlabel('Direction of Arrival (degrees)')
                ax3.set_title('Along-Track Image')

                if doppler2_plot_on == 1:
                    ax4.set_ylim([0,ymax])
                    ax4.set_xlim([theta_min,theta_max])
                    ax4.invert_yaxis()
                    ax4.set_xlabel('Direction of Arrival (degrees)')
                    ax4.set_title('(Unfocused)')
                
            ############## The along-track position
            ax2.plot([doppler_data2['distance'][slide_ind2]/1000,doppler_data2['distance'][slide_ind2]/1000],
                     [doppler_data2['Time'][0]*1e6,doppler_data2['Time'][-1]*1e6],ls=':',c='red')
    
            writer.grab_frame()
            
            ndh.remove_line(ax2,1)   
            if music_plot_on == 1:
                ndh.remove_image(ax1,1)
    
            if doppler1_plot_on == 1:
                ndh.remove_image(ax3,1)
    
            if doppler2_plot_on == 1:
                ndh.remove_image(ax4,1)