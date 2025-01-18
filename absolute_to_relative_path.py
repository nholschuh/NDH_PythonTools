from pathlib import Path
import os

def absolute_to_relative_path(inpath):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % This function finds the relative path to the current directory given some absolute path
    """    

    # Define an absolute path
    absolute_path = Path(inpath)
    
    # Define the base directory to make the path relative to
    base_directory = Path.cwd()
    
    # Convert to a relative path
    relative_path = os.path.relpath(absolute_path,base_directory)

    return relative_path
