import sys
import numpy as np
import ezdxf

def get_DWG_layers(dxf_data_or_fn):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This will read the structure of a dwg / dxf file and exctract the layer names
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    % dxf_data_or_fn -- The filename or dataobject to be read.
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    % layers -- the set of all possible layers
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %% This is mostly a subroutine for "read_DWG"
    """
    
    if isinstance(dxf_data_or_fn,type('')) == 1:
        data = ezdxf.readfile(dxf_data_or_fn)
    else:
        data = dxf_data_or_fn
    
    layers = []
    
    msp = data.modelspace()
    for e in msp.query("LINE"):
        layers.append(e.dxf.layer)
        
    for e in msp.query("LWPOLYLINE"):
        layers.append(e.dxf.layer)
        
    return set(layers)