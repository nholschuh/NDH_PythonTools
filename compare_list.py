import numpy as np

def compare_list(list1,list2):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % This function compares entire lists, and spits out two comparative statistics:
    %    1 -- Are all items across both lists both the same shape and same value
    %    2 -- Are all items across both lists the same value
    %    3 -- Are all items across both lists the same shape
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     list1 -- first list to compare
    %     list2 -- second list to compare
    %
    %%%%%%%%%%%%%%%
    % The outputs, following the structure in the headline description:
    %
    %      1: true/false
    %      2: true/false
    %      3: true/false
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 
    result1 = all(map(lambda x, y: np.all(x == y), list1,list2))
    result2 = all(map(lambda x, y: np.all(np.array(x).shape == np.array(y).shape), list1,list2))
    
    comb_result = np.all([result1,result2])
    
    return comb_result,result1,result2
    
