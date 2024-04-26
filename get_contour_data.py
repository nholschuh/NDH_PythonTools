################ This is the import statement required to reference scripts within the package
import os,sys
ndh_tools_path_opts = [
    '/mnt/data01/Code/',
    '/home/common/HolschuhLab/Code/'
]
for i in ndh_tools_path_opts:
    if os.path.isfile(i): sys.path.append(i)
################################################################################################

import numpy as np
import matplotlib.pyplot as plt
import NDH_Tools as ndh

def get_contour_data(contour_object,simplify_flag=0,simplify_threshold=100):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % 
    % This function extracts contour lines from a contour object for further plotting
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    % contour_object -- This is the output from a plt.contour command from Matplotlib
    % simplify_flag -- default=0, if set to 1, contour lines with fewer than 
    %                  "simplify_threshold" nodes will be removed
    % simplify_threshold -- default=100, see use of simplify flag.
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    % new_clines -- an nx3 array, where the first two columns are x and y coordinates
    %               for the contour lines, the third column is the contour value. 
    %               Individual contour lines are spearated by a row of NaNs in the array
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %% 
        
    """
    clines = []
    cvals = contour_object.cvalues
    for ind0,i in enumerate(contour_object.collections):
        if len(i.get_paths()) > 0:
            for j in i.get_paths():
                contour_mat = np.array(j.vertices)
                contour_mat = np.concatenate([contour_mat,np.ones((len(contour_mat[:,0]),1))*cvals[ind0]],axis=1)
                clines.append(contour_mat)

    if simplify_flag == 1:
        new_clines = np.empty(shape=(0,3))
        for ind0,subline in enumerate(clines):
            if len(subline) > simplify_threshold:
                new_clines = np.concatenate([new_clines,np.ones([1,3])*np.NaN,np.array(subline)])
    else:
        new_clines = clines 
        
    
    return new_clines