import matplotlib.animation as manimation

def generate_animation(fps,title='Matplotlib Animation',comment='Matplotlib Animation'):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This will generates the object that will produce an animation. There are
    % two accessory lines of code required, one outside your loop and one after
    % generating the image (supplied below)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    % spacing -- the gap between sequential values
    % fps -- the offset from 0 to round to
    %
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
    FFMpegWriter = manimation.writers['ffmpeg']
    metadata = dict(title=title, artist='Matplotlib',
                    comment=comment)
    writer = FFMpegWriter(fps=fps, metadata=metadata)
    return writer