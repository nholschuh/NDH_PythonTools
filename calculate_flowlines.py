import numpy as np
import matplotlib.pyplot as plt

def calculate_flowlines(x,y,u,v,seed_points,max_error=0.00001):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % This function prints out the minimum and maximum values of an array
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     input_array -- array of data to analyze
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %      output -- the min and max in a 1x2 array
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 

    ################# This uses a modified plt.streamline to pass through a user-editable keyword
    ################# argument "max_error", which goes into the interpolater to guarantee
    ################# accurate streammline calculation. Copy this version of streamplot
    ################# into your matplotlib directory to enable the use of streamline
    ################# calculation from NDH_Tools

    
    sls = []
    
    if isinstance(seed_points,list):
        seed_points = np.array(seed_points)
    
    if len(seed_points.shape) == 1:
        seed_points = np.expand_dims(seed_points,axis=0)
    
    fig = plt.figure()
    
    for ind0, sp in enumerate(seed_points[:,0]):
        streamlines = plt.streamplot(x,y,u,v,start_points=[seed_points[ind0,:]], max_error=max_error)


        ########### Here we extract the coordinate information along the streamline
        sl = [streamlines.lines.get_paths()[0].vertices[0]]
        for i in streamlines.lines.get_paths():
            sl.append(i.vertices[1])

        sls.append(np.array(sl))
    
    plt.close(fig)
    
    return sls