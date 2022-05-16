import os
import glob 

# Get all *.py filenames in __init__'s folder
full_paths = glob.glob(os.path.join(os.path.dirname(__file__), '*.py'))

# Remove path prefix and remove __init__.py from the list
file_names = [os.path.split(f)[1] for f in full_paths if f != __file__]

# Remove extension
files = [os.path.splitext(f)[0] for f in file_names]

for f in files:
    # from archive import f (__name__ is 'archive')
    __import__(__name__+'.'+f, globals=globals())

    # assign the function f.main to variable f
    globals()[f]=getattr(globals()[f], f)
    
