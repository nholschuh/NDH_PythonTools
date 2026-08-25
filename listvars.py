import inspect
import types


def listvars(user0_or_all1=0,namespace=0,name_filter='',return_flag=0):
    """
    % (C) Nick Holschuh - Amherst College -- 2026 (Nick.Holschuh@gmail.com)
    %
    % This function prints the name, type, and size of the objects sitting in
    % the calling namespace (the MATLAB "whos" command). By default it hides
    % modules, functions, classes, and the housekeeping variables IPython
    % creates, so what you see is the data you made.
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     user0_or_all1 -- 0 shows only user-created data variables (default),
    %                      1 shows everything, modules and functions included
    %     namespace -- the dictionary to inspect. Defaults to 0, which grabs
    %                  globals() from whatever called this function. Pass
    %                  globals() or locals() explicitly to look elsewhere.
    %     name_filter -- optional substring; only names containing it are shown
    %     return_flag -- 0 prints only (default), 1 also returns the results
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %     output -- (only when return_flag=1) a dictionary containing:
    %
    %         names -- the object names, alphabetically
    %         types -- the type name of each object
    %         sizes -- the shape (arrays) or length (lists/dicts/strings)
    %         objects -- the objects themselves
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    ############### Without an explicit namespace, look at whoever called us
    if isinstance(namespace,dict) == 0:
        namespace = inspect.currentframe().f_back.f_globals

    # The junk IPython leaves in the user namespace (the _-prefixed ones are caught below)
    ipython_names = ['In','Out','get_ipython','exit','quit','open','quit_','json','sys','os']
    skip_types = (types.ModuleType,types.FunctionType,types.MethodType,
                  types.BuiltinFunctionType,types.BuiltinMethodType,type)

    names = []
    types_out = []
    sizes = []
    objects = []

    for name in sorted(namespace.keys(),key=str.lower):
        obj = namespace[name]

        ############### Decide whether this one is user data or infrastructure
        if user0_or_all1 == 0:
            if name.startswith('_'):
                continue
            if name in ipython_names:
                continue
            if isinstance(obj,skip_types):
                continue
            # Catches the callables the types above miss - partials, ufuncs, decorated functions
            if callable(obj) and hasattr(obj,'shape') == 0:
                continue

        if len(name_filter) > 0 and name_filter not in name:
            continue

        ############### Type gets the dtype tacked on for arrays, since that is half the question
        type_str = type(obj).__name__
        if hasattr(obj,'dtype') and isinstance(obj,(types.ModuleType,type)) == 0:
            try:
                type_str = type_str+' ('+str(obj.dtype)+')'
            except:
                pass

        ############### Size is the shape when there is one, the length otherwise
        size_str = ''
        if hasattr(obj,'shape'):
            try:
                size_str = str(tuple(obj.shape))
            except:
                size_str = ''
        elif hasattr(obj,'dims'):
            # xarray Datasets have no single shape, so report the dimensions instead
            try:
                size_str = ', '.join([f'{k}:{v}' for k,v in dict(obj.dims).items()])
            except:
                size_str = ''
        elif isinstance(obj,(list,tuple,set,dict,str)):
            size_str = str(len(obj))

        names.append(name)
        types_out.append(type_str)
        sizes.append(size_str)
        objects.append(obj)

    ############### Print it as a table, with the columns sized to the contents
    if len(names) == 0:
        print('No variables found.')
    else:
        n_w = max([len(x) for x in names]+[4])
        t_w = max([len(x) for x in types_out]+[4])
        s_w = max([len(x) for x in sizes]+[4])

        print(f'{"Name":<{n_w}}  {"Type":<{t_w}}  {"Size":<{s_w}}')
        print('-'*(n_w+t_w+s_w+4))
        for i in range(len(names)):
            print(f'{names[i]:<{n_w}}  {types_out[i]:<{t_w}}  {sizes[i]:<{s_w}}')

    if return_flag == 1:
        return {'names':names,'types':types_out,'sizes':sizes,'objects':objects}
