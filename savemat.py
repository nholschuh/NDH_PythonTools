import hdf5storage

def savemat(matfiledata,fn):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % Saves a data dictionary as an hdf5 compatible matlab file
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     matfiledata -- data dictionary containing the information to write
    %     fn -- the filename to write to
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 
    hdf5storage.write(matfiledata, '.', fn, matlab_compatible=True)
    
