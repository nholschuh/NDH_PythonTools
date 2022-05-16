import numpy as np

def list_separator(in_list,separation_inds):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % This function takes a list and breaks it into sublists at specific indecies
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     in_list -- the list to be separated by the indecies below
    %     separation_inds -- array representing the maximum ind to include in each sublist
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %      outlist -- the separated list
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 

    if len(in_list) > separation_inds[-1]:
        separation_inds = np.concatenate([np.atleast_1d(np.array(0)),np.array(separation_inds),np.atleast_1d(np.array(len(in_list)))])
    else:
        separation_inds = np.concatenate([np.atleast_1d(np.array(0)),np.array(separation_inds)])
    
    outlist = []
    for i in range(len(separation_inds)-1):
        tlist = in_list[separation_inds[i]:separation_inds[i+1]]
        outlist.append(tlist)
        
    return outlist
    
