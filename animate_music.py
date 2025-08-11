import os
import numpy as np
import matplotlib.pyplot as plt
import tqdm

################## NDH Tools self imports
###########################################################
from .generate_animation import generate_animation
from .remove_image import remove_image
from .remove_line import remove_line
###########################################################

def animate_music(videoname,music_data,frame_skip=10,ymax=30,center_ind=0,min_amp=0,max_amp=0):
    """
    % (C) Nick Holschuh - Amherst College - 2025 (Nick.Holschuh@gmail.com)
    % This function animates a delay doppler image
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %      videoname - String (ending in .mp4) containing the file to write to
    %      music_data - MUSIC data loaded with radar_load_music
    %      frame_skip - An integer value, describing the spacing between presented MUSIC slices. 
    %      ymax - The maximum two way travel time to include in the plot (in microseconds)
    %      center_ind - The index associated with nadir for the cross-track dimension of the array. Set
    %                   to 0 if you want the value to be automatically determined
    %      min_amp - The vmin set across the images. If unknown, set to 0.
    %      max_amp - The vmax set across the images. If unknown, set to 0
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
    
    if center_ind == 0:
        center_ind = int(len(music_data['Tomo']['theta'][:,0])/2)
    
    if min_amp == 0:
        min_amp = np.nanpercentile(10*np.log10(music_data['Tomo']['img'][::5,::5,::100].ravel()),5)
    if max_amp == 0:
        max_amp = np.nanpercentile(10*np.log10(music_data['Tomo']['img'][::5,::5,::100].ravel()),99)
            
    ############# Music_image
    theta_rad = music_data['Tomo']['theta'][:,0]
    theta_deg = np.rad2deg(theta_rad)
        
    ############## Initiate the figure
    fig_size = 20
    fig = plt.figure(figsize=(fig_size,8))
    gs = fig.add_gridspec(1,5,wspace=0.1,hspace=1)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1:5])
    
    writer = generate_animation(20)
    
    ############# The nadir image
    slide_inds = np.arange(0,len(music_data['Latitude']),frame_skip)
    ax2.imshow(10*np.log10(music_data['Tomo']['img'][:,center_ind,:]),
                                extent=[music_data['distance'][0]/1000,music_data['distance'][-1]/1000,
                                        music_data['Time'][0]*1e6,music_data['Time'][-1]*1e6],
                                origin='lower',aspect='auto',cmap='gray_r',vmax=max_amp,vmin=min_amp)
    
    ax2.set_ylim([0,ymax])
    ax2.set_xlabel('Distance (km)')
    ax2.invert_yaxis()
    ax2.set_yticks([])
    ax2.set_title('Nadir Image')
    ax1.set_title('Direction of Arrival (X-Track) Image')
    
    with writer.saving(fig, videoname, 100):
        for loop_ind,slide_ind in enumerate(tqdm.tqdm(slide_inds)):
    
            if loop_ind == 0:
                ax1.set_ylim([0,ymax])
                ax1.invert_yaxis()
                ax1.set_xlabel('Off-Axis Direction of Arrival (degrees)')
                ax1.set_ylabel('Two Way Travel Time')
    
            ############## The direction of arrival image
            imdata = ax1.imshow(10*np.log10(music_data['Tomo']['img'][:,:,slide_ind]),
                                extent=[theta_deg[0][0],theta_deg[-1][0],
                                        music_data['Time'][0]*1e6,music_data['Time'][-1]*1e6],
                                origin='lower',aspect='auto',cmap='gray_r',vmax=max_amp,vmin=min_amp)    
    
            ############## The along-track position
            ax2.plot([music_data['distance'][slide_ind]/1000,music_data['distance'][slide_ind]/1000],
                     [music_data['Time'][0]*1e6,music_data['Time'][-1]*1e6],ls=':',c='red')
    
            writer.grab_frame()
            
            remove_image(ax1,1)
            remove_line(ax2,1)   