import os
import glob 
import importlib
import inspect


#####################################################
# Import all self-named functions
#####################################################

package_dir = os.path.dirname(__file__)
py_files = glob.glob(os.path.join(package_dir, "*.py"))

for py_file in py_files:
    module_name = os.path.basename(py_file)[:-3]

    ########### This will short-circuit the loop for either of these files
    if module_name == "__init__" or module_name == "attenuation_tools":
        continue

    module = importlib.import_module(f".{module_name}", package=__name__)
    function = getattr(module, module_name, None)
    if function:
        globals()[module_name] = function

######################################################
# Import all functions from attenuation_tools.py
######################################################

nickmodule = importlib.import_module(".attenuation_tools", package=__name__)
for name, obj in inspect.getmembers(nickmodule):
    if inspect.isfunction(obj):
        globals()[name] = obj
