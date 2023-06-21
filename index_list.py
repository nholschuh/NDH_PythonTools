

def index_list(input_list,index_array):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % This function allows you to index a list by integer array input
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     input_list -- the list you want to sort
    %     index_array -- array of vlues
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %      output_list -- the sorted_list you want to sort
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 
    output_list = [input_list[i] for i in index_array]
    
    return output_list
    