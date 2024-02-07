def subset_dict(input_dict,key_contains):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % this outputs a dictionary only with keys that contain the input string
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    % input_dict -- the dictionary you want to subset
    % key_contains -- string to compare to keys
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    % new_dict -- dictionary with reduced set of keys
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%
    """

    key_opts = list(input_dict)
    new_dict = {}
    for i in key_opts:
        if key_contains in i:
            new_dict[i] = input_dict[i]

    return new_dict
