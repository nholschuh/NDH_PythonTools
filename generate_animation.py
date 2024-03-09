import matplotlib.animation as manimation
import os

if os.path.isdir('/home/common/HolschuhLab/Code/'):
    import matplotlib.pyplot as plt
    plt.rcParams['animation.ffmpeg_path']='/home/common/HolschuhLab/Code/HolschuhLab_CondaEnv/bin/ffmpeg'
    

def generate_animation(fps,title='Matplotlib Animation',comment='Matplotlib Animation'):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This will generates the object that will produce an animation. There are
    % two accessory lines of code required, one outside your loop and one after
    % generating the image (supplied below)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    % fps -- The framerate (in frames per second)
    % title -- This is the title of the video as stored in the file
    % comment -- This stores some meta-text about your videoo
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    % writer -- the object that will be used to collect frames and write the animation
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    REMEMBER TO INCLUDE IN YOUR CODE --------
    with writer.saving(fig, videoname, 100):
    writer.grab_frame()
    
    """   

    print('After Generating the Writer, include the following:')
    print('Outside the loop:      with writer.saving(fig, videoname, 100):')
    print('To capture a frame:    writer.grab_frame()')
    
    
    # Define the meta data for the movie
    try:
        FFMpegWriter = manimation.writers['ffmpeg']
        metadata = dict(title=title, artist='Matplotlib',
                    comment=comment)
        writer = FFMpegWriter(fps=fps, metadata=metadata)
        print('Using the FFMpeg writer')
    except:
        PillowWriter = manimation.writers['pillow']
        metadata = dict(title=title, artist='Matplotlib',
                    comment=comment)
        writer = PillowWriter(fps=fps, metadata=metadata)
        print('Using the Pillow writer')

    return writer
