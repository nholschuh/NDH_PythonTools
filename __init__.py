################### Packages needed for init
import importlib
import os
import pkgutil


#####################################################
# Import all self-named functions
#####################################################

__all__ = []

package_name = __name__
package_path = os.path.dirname(__file__)

for modinfo in pkgutil.iter_modules([package_path]):
    module_name = modinfo.name
    if module_name.startswith("_") or module_name == "__init__" or module_name == "attenuation_tools":
        continue

    module = importlib.import_module(f".{module_name}", package=package_name)
    attr = getattr(module, module_name, None)

    if callable(attr):
        globals()[module_name] = attr
        __all__.append(module_name)

########## Still thinking about proper implementation for this
######################################################
# Import all functions from attenuation_tools.py
######################################################
#
#nickmodule = importlib.import_module(".attenuation_tools", package=__name__)
#for name, obj in inspect.getmembers(nickmodule):
#    if inspect.isfunction(obj):
#        globals()[name] = obj
