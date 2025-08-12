import os
from datetime import datetime

def list_notebooks(root='.',extension='.ipynb'):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % This function takes a directory and finds all python notebooks in subdirectories
    % sorted by modified date.
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
    notebooks = []

    for dirpath, _, filenames in os.walk(root):
        for file in filenames:
            if file.endswith(extension):
                full_path = os.path.join(dirpath, file)
                mtime = os.path.getmtime(full_path)
                notebooks.append({
                    'filename': file,
                    'directory': dirpath,
                    'modified': datetime.fromtimestamp(mtime)
                })

    # Sort by last modified date, descending
    notebooks.sort(key=lambda x: x['modified'], reverse=True)

    # Print header
    print(f"{'Notebook Name':40} {'Directory':40} {'Last Modified':25}")
    print("-"*105)

    # Print each notebook
    for nb in notebooks:
        print(f"{nb['filename'][:39]:40} {nb['directory'][:39]:40} {nb['modified'].strftime('%Y-%m-%d %H:%M:%S'):25}")

    return notebooks

