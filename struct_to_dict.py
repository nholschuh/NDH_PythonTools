import numpy as np

def struct_to_dict(x):
    """
    % (C) Nick Holschuh - Amherst College -- 2024 (Nick.Holschuh@gmail.com)
    %
    % This function will convert a structured array to a dictionary (for use in loading parameter information)
    """ 
    def _unwrap0d(x):
        """Unwrap 0-D numpy arrays repeatedly (handles arr[()] cases)."""
        while isinstance(x, np.ndarray) and x.ndim == 0:
            x = x[()]
        return x
    
    def to_dict_from_dtype(x):
        x = _unwrap0d(x)
    
        # Structured scalar (np.void) -> dict using field names
        if isinstance(x, np.void) and x.dtype.names:
            return {name: to_dict_from_dtype(_unwrap0d(x[name])) for name in x.dtype.names}
    
        # Structured ndarray -> single dict if size==1, else list of dicts
        if isinstance(x, np.ndarray) and x.dtype.names:
            return (to_dict_from_dtype(_unwrap0d(x.reshape(())).item())
                    if x.size == 1 else
                    [to_dict_from_dtype(rec) for rec in x.ravel()])
    
        # Object arrays: unwrap scalar, else iterate via Python containers
        if isinstance(x, np.ndarray) and x.dtype == object:
            return to_dict_from_dtype(_unwrap0d(x)) if x.ndim == 0 else \
                   [to_dict_from_dtype(v) for v in x.tolist()]
    
        # Plain ndarrays: keep as arrays (use x.tolist() if you need JSON)
        if isinstance(x, np.ndarray):
            return x
    
        # Python containers
        if isinstance(x, (list, tuple)):
            return type(x)(to_dict_from_dtype(v) for v in x)
    
        # NumPy scalar -> Python scalar
        if isinstance(x, np.generic):
            return x.item()
    
        # Everything else (str, int, custom objects, etc.)
        return x

    return to_dict_from_dtype(x)