

def edgetrim_mask(edge_trim_array, debug_flag=0, start_trim=0, end_trim=0, additional_narrowing=0):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % This function takes in a CSARP_surf y array generated using "pick edge_mask"
    % and converts the output into a mask for subsetting CSARP_dem data
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %      edge_trim_array -- this is typically a 64xn array, with values only
    %                         where edge trim values have been identified.
    %                         These typically are the 8th entry in the 'y' object 
    %                         of a CSARP_surf file
    %      debug_flag=0 -- this will produce a plot at the end showing the edge mask
    %      start_trim=0 -- this removes additional columns at the front of the mask
    %      end_trim=0 -- this removes additional columns from the end of the mask
    %      additional_narrowing=0 -- this takes from both sides relative to the edge trim
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %      mask -- a 64xn array of zeros and ones defined by the trim values
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % the edge trim array is typically surf_data['surf']['y'][7]
    """        
    import numpy as np
    from scipy.interpolate import interp1d
    mask = np.zeros(edge_trim_array.shape)


    ###################################################################
    ### Here we identify the non-NAN values in the edge_trim matrix ###
    ###################################################################
    et_row,et_col = np.where(~np.isnan(edge_trim_array))
    center_split = np.mean(et_row)
    left_ind = np.where(et_row < center_split)
    right_ind = np.where(et_row >= center_split)


    ###################################################################
    ### We interpolate the edge_trim values across all slices      ####
    ###################################################################
    col_opts = np.arange(0,edge_trim_array.shape[1])

    left_row_interpolator = interp1d(et_col[left_ind],et_row[left_ind]+additional_narrowing,fill_value=np.NaN,bounds_error=0)
    right_row_interpolator = interp1d(et_col[right_ind],et_row[right_ind]-additional_narrowing,fill_value=np.NaN,bounds_error=0)

    left_row = left_row_interpolator(col_opts).astype(int)
    right_row = right_row_interpolator(col_opts).astype(int)

    
    ###################################################################
    ### Then we build the mask from the interpolated values        ####
    ###################################################################
    for i in col_opts:
        mask[left_row[i]:right_row[i]+1,i] = 1
    for i in range(start_trim):
        mask[:,i] = 0
    for i in range(end_trim):
        mask[:,-i] = 0

    mask[mask == 0] = np.NaN
    
    
    if debug_flag:
        import matplotlib.pyplot as plt
        plt.imshow(mask)
        plt.plot(et_col,et_row,'o',c='red')
        plt.plot(col_opts,left_row,'-',c='black')
        plt.plot(col_opts,right_row,'-',c='black')
        plt.gca().set_aspect('auto')

    return mask

