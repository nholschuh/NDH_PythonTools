import numpy as np
import imageio

def crop_image(inimage,outimage,margin=0):
    """
    % (C) Nick Holschuh - Penn State University - 2015 (Nick.Holschuh@gmail.com)
    % This function takes an image file and removes the solid white margins.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    % inimage -- the filename for the video to crop
    % outimage -- the filename to write the cropped video to
    % margin=0 -- the number of additional rows/columns to add as buffer
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    % [Nothing is returned by this function]
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%
    """

    frame_aggregate = imageio.imread(inimage)

    row_margin = np.where(np.mean(frame_aggregate,0) == 255)[0]
    middle = np.where(np.diff(row_margin) > 1)[0]
    x = row_margin[middle[0]]-margin
    w = row_margin[middle[-1]+1]-row_margin[middle[0]]+2*margin

    row_margin = np.where(np.mean(frame_aggregate,1) == 255)[0]
    middle = np.where(np.diff(row_margin) > 1)[0]
    y = row_margin[middle[0]]-margin
    h = row_margin[middle[-1]+1]-row_margin[middle[0]]+2*margin


    crop_frame = frame_aggregate[y:y+h, x:x+w]
    imageio.imwrite(outimage,crop_frame)
