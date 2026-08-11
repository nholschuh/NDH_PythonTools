import numpy as np
import matplotlib.pyplot as plt

def line_simplify(lines, bearing_thresh=5.0, distance_sd_thresh=4.0, plotter=False):
    """
    Subdivides data into separate lines and reduces the number of points 
    to capture the essence of profile data.
    
    Parameters:
    - lines: A single 2D numpy array of (x,y) points, or a list of such arrays.
    - bearing_thresh: The angular change threshold (in degrees) to keep a point.
    - distance_sd_thresh: Standard deviation multiplier to split lines with large gaps.
    - plotter: Boolean flag to plot the original vs. reduced lines.
    
    Returns:
    - final_lines: The reduced line(s).
    - line_inds: The indices of the original points retained in the final line(s).
    """
    
    # Determine if we were provided a single line or a list of lines
    if isinstance(lines, np.ndarray) and lines.ndim == 2:
        lines_list = [lines]
        return_single = True
    else:
        lines_list = list(lines)
        return_single = False

    final_lines = []
    line_inds_list = []

    for i, current_line in enumerate(lines_list):
        # Ensure we are working with a float numpy array to handle NaNs
        line_arr = np.array(current_line, dtype=float)
        
        # ====================================================================
        # 1. Distance Thresholding (Line Separating Component)
        # ====================================================================
        if distance_sd_thresh > 0 and len(line_arr) > 1:
            # Calculate distances between consecutive points natively
            diffs = np.diff(line_arr, axis=0)
            dists = np.linalg.norm(diffs, axis=1)
            
            mv = np.nanmean(dists)
            std_v = np.nanstd(dists)
            
            # Find indices where the distance exceeds the threshold
            nan_inds = np.where(dists > mv + std_v * distance_sd_thresh)[0]
            
            if len(nan_inds) > 0:
                nan_vec = np.array([[np.nan, np.nan]])
                # Insert NaNs backwards to prevent shifting indices during insertion
                for idx in nan_inds[::-1]:
                    line_arr = np.insert(line_arr, idx + 1, nan_vec, axis=0)

        # ====================================================================
        # 2. Complexity Reduction Component
        # ====================================================================
        if len(line_arr) < 2:
            final_lines.append(line_arr)
            line_inds_list.append(np.array([0]))
            continue

        # Calculate line direction (bearings). 
        # Using arctan2(dx, dy) naturally maps 0 to North/Up, progressing clockwise.
        diffs = np.diff(line_arr, axis=0)
        dx, dy = diffs[:, 0], diffs[:, 1]
        b = np.degrees(np.arctan2(dx, dy)) % 360
        b = np.append(b, b[-1]) # Append last bearing to match coordinate length
        
        # Initiate the reduced complexity algorithm at the first non-NaN bearing
        valid_inds = np.where(~np.isnan(b))[0]
        ind = valid_inds[0] if len(valid_inds) > 0 else 0
        
        fl = [line_arr[ind]]
        fl_ind = [ind]
        
        while ind < len(b) - 1:
            if np.isnan(b[ind]):
                # Introduce a NaN, step forward, and capture the next valid point
                fl.append(np.array([np.nan, np.nan]))
                ind += 1
                fl_ind.append(ind)
                
                valid_sub_inds = np.where(~np.isnan(b[ind:]))[0]
                if len(valid_sub_inds) > 0:
                    ind = ind + valid_sub_inds[0]
                    fl.append(line_arr[ind])
                    fl_ind.append(ind)
                else:
                    break # Reached the end of the line with NaNs
                    
            else:
                # Calculate angular difference, handling 360-degree wrap-around safely
                tb = b[ind:] - b[ind]
                tb = (tb + 180) % 360 - 180 
                
                # Find when bearing changes by more than the threshold, or becomes NaN
                change_inds = np.where((np.abs(tb) > bearing_thresh) | np.isnan(tb))[0]
                
                if len(change_inds) == 0:
                    ind_next = len(b) - 1 # Jump to the end of the line
                else:
                    ind_next = ind + change_inds[0]
                
                # Prevent infinite loops if threshold is 0
                if ind_next == ind:
                    ind_next += 1
                    
                if ind_next < len(line_arr):
                    fl.append(line_arr[ind_next])
                    fl_ind.append(ind_next)
                    
                ind = ind_next

        final_lines.append(np.array(fl))
        line_inds_list.append(np.array(fl_ind))

        # ====================================================================
        # 3. Plotting Component
        # ====================================================================
        if plotter:
            plt.plot(line_arr[:, 0], line_arr[:, 1], 'o', color='blue', mfc='blue', alpha=0.5, label='Original' if i==0 else "")
            plt.plot(np.array(fl)[:, 0], np.array(fl)[:, 1], 'o-', color='red', label='Reduced' if i==0 else "")

    if plotter:
        plt.legend()
        plt.title('Line Complexity Reduction')
        plt.axis('equal')
        plt.show()

    if return_single:
        return final_lines[0], line_inds_list[0]
    else:
        return final_lines, line_inds_list