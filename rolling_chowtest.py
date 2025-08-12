import numpy as np
import matplotlib.pyplot as plt
import scipy

def rolling_chowtest(series_x,series_y,spacing,window_length,power_check=0,plot_flag=0):
    """
    % (C) Nick Holschuh - Amherst College - 2025 (Nick.Holschuh@gmail.com)
    % This function applies a rolling chow test to find structural breaks in slopw
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %      series_x -- a 1d array with x values
    %      series_y -- a 1d array with y values
    %      spacing -- the index spacing between possible breakpoints
    %      window_length -- the window size used for regression (0 if using the full dataset)
    %      plot_flag    
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
    ############### Construct known matrix
    steps = np.arange(spacing,len(series_x),spacing)
    independent_matrix = np.zeros([len(series_x)*2*len(steps),len(steps)*6])
    dependent_matrix = np.zeros([len(series_x)*2*len(steps),len(steps)*3])
    sl = len(series_x)
    start_counter = 0
    
    out_step = []
    
    for ind0,step in enumerate(steps):
        if window_length == 0:
            s1_start = 0
            s2_start = step
            s1_end = step
            s2_end = sl
            full_window = s2_end=s1+start
            
        else:
            s1_start = np.max([0,step-window_length])
            s2_start = step
            s1_end = step
            s2_end = np.min([sl,step+window_length])
            full_window = s2_end-s1_start
    
        if np.min([s1_end-s1_start,s2_end-s2_start]) < 5:
            pass
        else:
            ######### The full regression
            independent_matrix[start_counter+s1_start:start_counter+s2_end,6*ind0+0] = series_x[s1_start:s2_end]
            independent_matrix[start_counter+s1_start:start_counter+s2_end,6*ind0+1] = 1
            dependent_matrix[start_counter+s1_start:start_counter+s2_end,3*ind0] = series_y[s1_start:s2_end]
            
            ######### The first regression
            independent_matrix[start_counter+s1_start+full_window:start_counter+s1_end+full_window,6*ind0+2] = series_x[s1_start:s1_end]
            independent_matrix[start_counter+s1_start+full_window:start_counter+s1_end+full_window,6*ind0+3] = 1
            dependent_matrix[start_counter+s1_start+full_window:start_counter+s1_end+full_window,3*ind0+1] = series_y[s1_start:s1_end]
        
            ######### The second regression
            independent_matrix[start_counter+s2_start+full_window:start_counter+s2_end+full_window,6*ind0+4] = series_x[s2_start:s2_end]
            independent_matrix[start_counter+s2_start+full_window:start_counter+s2_end+full_window,6*ind0+5] = 1
            dependent_matrix[start_counter+s2_start+full_window:start_counter+s2_end+full_window,3*ind0+2] = series_y[s2_start:s2_end]
        
            ######### The counter for where to start
            start_counter = start_counter+2*full_window
            out_step.append(step)

    out_step = np.array(out_step)
    
    ############# Here we remove columns that have fewer than 1 sample:
    n = np.sum(independent_matrix != 0,axis=0)
    ki = np.where(n > 0)[0]
    independent_matrix = independent_matrix[:,ki]
    
    n = np.sum(dependent_matrix != 0,axis=0)
    ki = np.where(n > 0)[0]
    dependent_matrix = dependent_matrix[:,ki]
    
    ############# This filters out empty rows or rows with NaNs
    remove_determination_series = np.sum(np.concatenate([independent_matrix,dependent_matrix],axis=1),axis=1)
    ki = np.where(np.all([np.isnan(remove_determination_series) == 0, remove_determination_series != 0],axis=0))[0]
    independent_matrix = independent_matrix[ki,:]
    dependent_matrix = dependent_matrix[ki,:]
    
    ############# Now we fit the parameters, optimized for sparse matrices
    if 0:
        beta = np.linalg.inv(independent_matrix.T @ independent_matrix) @ independent_matrix.T @ dependent_matrix
    else:
        A = scipy.sparse.csr_matrix(independent_matrix.T @ independent_matrix)
        b = (independent_matrix.T @ dependent_matrix)
        beta = scipy.sparse.linalg.spsolve(A, b)
        
    solution_matrix = independent_matrix @ beta
    
    ############# Now we calculate the chow test results
    rss = np.sum((dependent_matrix-solution_matrix)**2,axis=0)
    rss[np.isnan(rss)] = 0
    k = 2
    n = np.sum(dependent_matrix != 0,axis=0)
    n_true = n[np.arange(0,len(n),3)]
    rss_full = rss[np.arange(0,len(rss),3)]
    rss1 = rss[np.arange(1,len(rss),3)]
    rss2 = rss[np.arange(2,len(rss),3)]
    chow_score = ((rss_full-(rss1+rss2))/k)/((rss1+rss2)/(n_true-2*k))
    
    ############## Get the slopes and intercepts
    slope_col_inds = np.arange(0,len(out_step)*3,1)
    slope_row_inds = np.arange(0,len(out_step)*3,1)*2
    intercept_col_inds = np.arange(0,len(out_step)*3,1)
    intercept_row_inds= np.arange(0,len(out_step)*3,1)*2+1
    
    slopes = beta[(slope_row_inds,slope_col_inds)]
    slope_all = slopes[np.arange(0,len(slopes),3)] 
    slope_pres = slopes[np.arange(1,len(slopes),3)] 
    slope_posts = slopes[np.arange(2,len(slopes),3)]
    
    intercepts = beta[(intercept_row_inds,intercept_col_inds)]
    int_all = intercepts[np.arange(0,len(slopes),3)] 
    int_pres = intercepts[np.arange(1,len(slopes),3)] 
    int_posts = intercepts[np.arange(2,len(slopes),3)] 
    
    peaks,trash = scipy.signal.find_peaks(chow_score)
    if power_check > 0:
        ki = np.where(chow_score[peaks] > np.percentile(chow_score,power_check))[0]
        peaks = peaks[ki]

    min_x_inds = np.concatenate([np.array([0]),peaks])
    max_x_inds = np.concatenate([peaks,np.array([len(out_step)])])
    min_x = series_x[np.concatenate([np.array([0]),out_step[peaks.astype(int)]])]
    max_x = series_x[np.concatenate([out_step[peaks.astype(int)],np.array([len(series_x)-1])])]

    slopes = []
    ints = []
    for ind in np.arange(len(min_x_inds)-1):
        #slopes.append(np.mean(slope_all[min_x_inds[ind]:max_x_inds[ind]]))
        #ints.append(np.mean(int_all[min_x_inds[ind]:max_x_inds[ind]]))
        if ind == 0:
            slopes.append(slope_pres[max_x_inds[ind]])
            ints.append(int_pres[max_x_inds[ind]])
        
        slopes.append(slope_posts[max_x_inds[ind]])
        ints.append(int_posts[max_x_inds[ind]])

    if plot_flag == 1:
        plt.subplot(2,1,1)
        plt.plot(series_x,series_y)
        for peak in peaks:
            plt.axvline(series_x[out_step[peak]],c='red',label='structural break')

        for ind in np.arange(len(slopes)):
            plt.plot([min_x[ind],max_x[ind]],np.array([min_x[ind],max_x[ind]])*slopes[ind]+ints[ind],'--',c='red')

        plt.xlabel('X Series')
        plt.ylabel('Y Series')
        plt.legend()
        
        plt.subplot(2,1,2)
        plt.plot(series_x[out_step],chow_score,'.')
        plt.xlim([np.min(series_x),np.max(series_x)])
        plt.xlabel('X Series')
        plt.ylabel('Chow Score')
    
    out_dict={'peaks':series_x[out_step[peaks]],'series_inds':out_step,'chow_scores':chow_score,'min_xs':min_x,'max_xs':max_x,'slopes':slopes,'ints':ints}
    
    return out_dict