import numpy as np

def compare_list(list1,list2):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % This function tests the equality of every item in a list
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     list1 -- first list to compare
    %     list2 -- second list to compare
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %      true/false
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 
    result1 = all(map(lambda x, y: np.all(x == y), list1,list2))
    result2 = all(map(lambda x, y: np.all(np.array(x).shape == np.array(y).shape), list1,list2))
    
    comb_result = np.all([result1,result2])
    
    return comb_result,result1,result2
    
