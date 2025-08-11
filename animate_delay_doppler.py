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

def animate_delay_doppler(videoname,radar_data,depth_data,doppler_data,frame_skip,ymax=30,center_ind=0,max_amp=0,min_amp=0):
    """
    % (C) Nick Holschuh - Amherst College - 2025 (Nick.Holschuh@gmail.com)
    % This function animates a delay doppler image
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %      radar_data - original radar data loaded with radar_load
    %      depth_data - radar image with removed air travel time
    %      target ind - A specific index in the radar image. If 0, calculate over a rolling window
    %      window_size - The number of samples to include in the fft
    %      deg 
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %% animate_delay_doppler(videoname,radar_data,depth_data,doppler_data,frame_skip,ymax=30,center_ind=0,max_amp=0,min_amp=0)
    """
    if center_ind == 0:
        center_ind = int(len(doppler_data['slope_axis'])/2)
    
    if min_amp == 0:
        min_amp = np.nanpercentile(doppler_data['doppler_data'][::5,::5,::100].ravel(),5)
    if max_amp == 0:
        max_amp = np.nanpercentile(doppler_data['doppler_data'][::5,::5,::100].ravel(),99)
    
    
    ############# DelayDoppler Image
    theta_deg = doppler_data['slope_axis']

    ############## Initiate the figure
    fig_size = 20
    fig = plt.figure(figsize=(fig_size,8))
    gs = fig.add_gridspec(1,5,wspace=0.1,hspace=1)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1:5])
    
    writer = generate_animation(20)
    
    ############# The nadir image
    slide_inds = np.arange(0,len(doppler_data['distance']),frame_skip)
    ax2.imshow(10*np.log10(np.abs(depth_data['new_data'])**2),
                                extent=[radar_data['distance'][0]/1000,radar_data['distance'][-1]/1000,
                                        doppler_data['Time'][0]*1e6,doppler_data['Time'][-1]*1e6],
                                origin='lower',aspect='auto',cmap='gray_r')
    
    ax2.set_ylim([0,ymax])
    ax2.set_xlabel('Distance (km)')
    ax2.invert_yaxis()
    ax2.set_yticks([])
    ax2.set_title('Nadir Image')
    ax1.set_title('Direction of Arrival (Along-Track) Image')
    
    with writer.saving(fig, videoname, 100):
        for loop_ind,slide_ind in enumerate(tqdm.tqdm(slide_inds)):
    
            
            ############## The direction of arrival image
            imdata = ax1.imshow(doppler_data['doppler_data'][slide_ind,:,:],
                                extent=[theta_deg[0],theta_deg[-1],
                                        doppler_data['Time'][0]*1e6,doppler_data['Time'][-1]*1e6],
                                origin='lower',aspect='auto',cmap='gray_r',vmax=max_amp,vmin=min_amp)   
    
            if loop_ind == 0:
                ax1.set_ylim([0,ymax])
                ax1.invert_yaxis()
                ax1.set_xlabel('Off-Axis Direction of Arrival (degrees)')
                ax1.set_ylabel('Two Way Travel Time')
    
            ############## The along-track position
            ax2.plot([doppler_data['distance'][slide_ind]/1000,doppler_data['distance'][slide_ind]/1000],
                     [doppler_data['Time'][0]*1e6,doppler_data['Time'][-1]*1e6],ls=':',c='red')
    
            writer.grab_frame()
            
            remove_image(ax1,1)
            remove_line(ax2,1)   