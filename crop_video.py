import numpy as np
import cv2

def crop_video(invideo,outvideo,margin=0):
    """
    % (C) Nick Holschuh - Penn State University - 2015 (Nick.Holschuh@gmail.com)
    % This function takes a video file and removes the solid white margins
    % from the frames.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    % invideo -- the filename for the video to crop
    % outvideo -- the filename to write the cropped video to
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
    # Open the video
    cap = cv2.VideoCapture(invideo)

    # Initialize frame counter
    cnt = 0

    # Some characteristics from the original video
    w_frame, h_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps, frames = cap.get(cv2.CAP_PROP_FPS), cap.get(cv2.CAP_PROP_FRAME_COUNT)

    ret, frame = cap.read()
    frame_aggregate = np.ones(frame.shape)*255
    frame_aggregate = np.mean(frame_aggregate,2)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            newframe = np.mean(frame,2)
            temp = np.stack([frame_aggregate,newframe])
            frame_aggregate = np.mean(temp,0)
        else:
            break

    row_margin = np.where(np.mean(frame_aggregate,0) == 255)[0]
    middle = np.where(np.diff(row_margin) > 1)[0]
    x = row_margin[middle[0]]-margin
    w = row_margin[middle[-1]+1]-row_margin[middle[0]]+2*margin

    row_margin = np.where(np.mean(frame_aggregate,1) == 255)[0]
    middle = np.where(np.diff(row_margin) > 1)[0]
    y = row_margin[middle[0]]-margin
    h = row_margin[middle[-1]+1]-row_margin[middle[0]]+2*margin

    # output
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(outvideo, fourcc, fps, (w, h))


    # Open the video
    cap = cv2.VideoCapture(invideo)

    while(cap.isOpened()):
        if cnt > 0:
            pass
        else:
            print('started')

        ret, frame = cap.read()

        cnt += 1 # Counting frames

        # Avoid problems when video finish
        if ret==True:
            # Croping the frame
            crop_frame = frame[y:y+h, x:x+w]

            # Percentage
            xx = cnt *100/frames
            print(int(xx),'%')

            # Saving from the desired frames
            #if 15 <= cnt <= 90:
            #    out.write(crop_frame)

            # I see the answer now. Here you save all the video
            out.write(crop_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break


    cap.release()
    out.release()
    cv2.destroyAllWindows()