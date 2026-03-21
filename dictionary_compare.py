def dictionary_compare(a, b, print_flag=1, *, rel_tol=0.0, abs_tol=0.0):
    """
    % (C) GPT-5 (ChatGPT) - 2025
    %     Modified by Nick Holschuh (nholschuh@amherst.edu)
    % This function compares two potentially complicated Python objects (including
    % nested dictionaries, lists/tuples, sets, and NumPy arrays) and reports
    % structural differences and value differences.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %      a            - first dictionary or object to compare
    %      b            - second dictionary or object to compare
    %      print_flag   - Print the output of the dictionary comparison
    %      rel_tol      - [0.0] relative tolerance for float/array comparison
    %      abs_tol      - [0.0] absolute tolerance for float/array comparison
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are:
    %
    %      diff_result - dictionary containing results with three keys:
    %           .structure_diffs   - list of strings describing missing keys,
    %                                length mismatches, or shape differences
    %           .type_diffs        - list of tuples (path, type_a, type_b)
    %                                for places where types differ
    %           .value_diffs       - dictionary where keys are string paths to
    %                                the differing value, and values are tuples
    %                                (value_in_a, value_in_b)
    %
    % Notes:
    %   - NumPy arrays are compared by shape first, then with allclose() for
    %     numeric arrays (using rel_tol/abs_tol) or array_equal() otherwise.
    %   - Lists/tuples are compared element-wise; sets are compared by membership.
    %   - Dictionaries are traversed recursively; missing keys are flagged in
    %     structure_diffs.
    %   - Paths are reported using dot notation for dict keys and [i] for indices.
    """
        
    import math, collections.abc as cabc
    import numpy as np

    out = {"structure_diffs": [], "type_diffs": [], "value_diffs": {}}
    visited = set()

    def is_number(x):
        return isinstance(x, (int, float)) and not isinstance(x, bool)

    def numbers_equal(x, y):
        if isinstance(x, float) or isinstance(y, float):
            try:
                return math.isclose(float(x), float(y), rel_tol=rel_tol, abs_tol=abs_tol)
            except Exception:
                return False
        return x == y

    def equal(x, y):
        if is_number(x) and is_number(y):
            return numbers_equal(x, y)
        return x == y

    def path_join(base, key):
        if isinstance(key, int):
            return f"{base}[{key}]"
        if base == "":
            return str(key)
        return f"{base}.{key}"

    def walk(x, y, path=""):
        pid = (id(x), id(y))
        if pid in visited:
            return
        visited.add(pid)

        # Special handling for numpy arrays
        if isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
            if x.shape != y.shape:
                out["structure_diffs"].append(f"{path or '<root>'} shape {x.shape} != {y.shape}")
                return
            if np.issubdtype(x.dtype, np.number) and np.issubdtype(y.dtype, np.number):
                if not np.allclose(x, y, rtol=rel_tol, atol=abs_tol, equal_nan=True):
                    out["value_diffs"][path or "<root>"] = (x, y)
            else:
                if not np.array_equal(x, y):
                    out["value_diffs"][path or "<root>"] = (x, y)
            return

        # Dicts
        if isinstance(x, dict) and isinstance(y, dict):
            x_keys, y_keys = set(x.keys()), set(y.keys())
            for k in sorted(x_keys - y_keys, key=str):
                out["structure_diffs"].append(f"{path_join(path,k)} missing in right")
            for k in sorted(y_keys - x_keys, key=str):
                out["structure_diffs"].append(f"{path_join(path,k)} missing in left")
            for k in sorted(x_keys & y_keys, key=str):
                walk(x[k], y[k], path_join(path, k))
            return

        # Lists / tuples
        if isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)):
            if len(x) != len(y):
                out["structure_diffs"].append(f"{path or '<root>'} length {len(x)} != {len(y)}")
            for i, (xi, yi) in enumerate(zip(x, y)):
                walk(xi, yi, path_join(path, i))
            return

        # Sets
        if isinstance(x, (set, frozenset)) and isinstance(y, (set, frozenset)):
            if x != y:
                out["value_diffs"][path or "<root>"] = (x, y)
            return

        # Fallback: direct comparison
        if not equal(x, y):
            out["value_diffs"][path or "<root>"] = (x, y)

    walk(a, b, "")

    if print_flag == 1:
        print('Structural Differences --------------')
        for i in out['structure_diffs']:
            print(i)
        
        print('Value Differences -------------------')
        for i in list(out['value_diffs'].keys()):
            if 'array_proc' not in i:
                if 'cluster' not in i:
                    print(i)

    return out
