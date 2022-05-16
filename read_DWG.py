import sys
sys.path.append('/mnt/data01/Code/')

import numpy as np
import ezdxf

def read_DWG(dxf_file_name):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This function reads a DWG file
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %      dxf_file_name -- The filename to read
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    %      outdict -- the data read from the file
    %      layers -- the set of all possible layers
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """    
    from NDH_Tools import get_DWG_layers
    from NDH_Tools import read_DWG_layer
    
    data = ezdxf.readfile(dxf_file_name)
    
    layers = get_DWG_layers(data)
    
    outdict = {}
    for i in layers:
        outdict[i] = read_DWG_layer(i,data)
        
    return outdict, layers