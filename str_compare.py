def str_compare(strlist,searchterm):
    """
    % (C) Nick Holschuh - Penn State University - 2015 (Nick.Holschuh@gmail.com)
    % Function that searches a list for a string or substring
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %    strlist -- a list of strings
    %    searchterm -- either a complete or partial string to find in the list
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    %    kstrings -- the strings to keep
    %    ki -- the indecies of the associated strings
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%
    """

    kstrings = [s for s in strlist if searchterm in s]
    ki = [ind for ind,s in enumerate(strlist) if searchterm in s]
    return kstrings,ki
