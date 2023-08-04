import numpy as np
import matplotlib.pyplot as plt

def get_contour_data(contour_object):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    % points_object -- 
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    % outdata -- 
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
    
    return clines