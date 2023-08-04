import numpy as np
import matplotlib.pyplot as plt

def graphical_selection(points_object,style_arguments={},lock_to=0):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This will allow you to interact with a figure plotted with matplotlib in ipympl
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    % points_object -- This is the plot object that will update with the selected points
    %                  Must initialize with "points_object = plt.plot([],[])"
    % style_arguments -- A dictionary containing all of the line attributes you want for the points object.
    %                  key options -- 'ms','color','style'
    % lock_to -- if set to 1, than graphical selection can only choose points
    %            for data that has already been plotted
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    % points_object -- a dictionary containing the x and y values of the selected points
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %% 

    Input Commands ---------------------------------
        Left Click -- add a new point with a meta value of "0"
        Right Click -- add a NaN with a meta value of "1"
        "f" key -- selects a point and appends a meta value of "2"
        "u" key -- undo the last point selection
    """
    
    if isinstance(points_object,type([])):
        points_object = plt.plot([],[],'.',color='black')
    
    if 'meta_ndh' not in points_object[0].__dict__.keys():
        points_object[0].__dict__['meta_ndh'] = np.zeros(len(points_object[0].get_xdata()))
    
    for i in style_arguments.keys():
        if i == 'ms':
            points_object[0].set_ms(style_arguments[i])
        if i == 'color':
            points_object[0].set_color(style_arguments[i])
        if i == 'linestyle':
            points_object[0].set_linestyle(style_arguments[i])
        if i == 'markerstyle':
            points_object[0].set_marker(style_arguments[i])  
            
    ####### This collects the existing points if lock_to == 1
    if lock_to == 1:
        import scipy.spatial
        ds_fac = 1
        ax = plt.gca()
        
        x_total = np.array([])
        y_total = np.array([])
        for line_ind in range(len(ax.lines)):
            x = np.array(ax.lines[line_ind].get_xdata())
            y = np.array(ax.lines[line_ind].get_ydata())
            x_total = np.concatenate([x_total,x])
            y_total = np.concatenate([y_total,y])
        x_total = x_total[::ds_fac]
        y_total = y_total[::ds_fac]
        points = np.stack([x_total,y_total]).T
        if len(points) == 0:
            print('There doesn''t seem to be any data. Make sure graphical_selection comes after the data are plotted')
        ckdtree = scipy.spatial.cKDTree(points)
            
    
    def onclick(event):
        
        if lock_to == 0:
            x_add = event.xdata
            y_add = event.ydata
        elif lock_to == 1:
            cp_id = closest_point_id(ckdtree, event.xdata, event.ydata)
            x_add = x_total[cp_id]
            y_add = y_total[cp_id]
        
        ######################## Left Click
        if event.button == 1:
            updated_xs = np.concatenate([points_object[0].get_xdata(),[x_add]])
            updated_ys = np.concatenate([points_object[0].get_ydata(),[y_add]])
            points_object[0].set_xdata(updated_xs)
            points_object[0].set_ydata(updated_ys)
            points_object[0].__dict__['meta_ndh'] = np.concatenate([points_object[0].__dict__['meta_ndh'],np.ones(1)*0])
            
        ######################### Right Click
        elif event.button == 3:
            updated_xs = np.concatenate([points_object[0].get_xdata(),[np.NaN]])
            updated_ys = np.concatenate([points_object[0].get_ydata(),[np.NaN]])
            points_object[0].set_xdata(updated_xs)
            points_object[0].set_ydata(updated_ys)
            points_object[0].__dict__['meta_ndh'] = np.concatenate([points_object[0].__dict__['meta_ndh'],np.ones(1)*1])

    def on_key(event):
        if event.key == 'u':
            updated_xs = points_object[0].get_xdata()[0:-1]
            updated_ys = points_object[0].get_ydata()[0:-1]
            points_object[0].set_xdata(updated_xs)
            points_object[0].set_ydata(updated_ys)
            points_object[0].__dict__['meta_ndh'] = points_object[0].__dict__['meta_ndh'][0:-1]
        if event.key == 'f':
            updated_xs = np.concatenate([points_object[0].get_xdata(),[x_add]])
            updated_ys = np.concatenate([points_object[0].get_ydata(),[y_add]])
            points_object[0].set_xdata(updated_xs)
            points_object[0].set_ydata(updated_ys)
            points_object[0].__dict__['meta_ndh'] = np.concatenate([points_object[0].__dict__['meta_ndh'],np.ones(1)*2])
            
    cid = plt.gcf().canvas.mpl_connect('button_press_event', onclick)
    cid = plt.gcf().canvas.mpl_connect('key_press_event', on_key)
    
    return points_object


def closest_point_distance(ckdtree, x, y):
    #returns distance to closest point
    return ckdtree.query([x, y])[0]

def closest_point_id(ckdtree, x, y):
    #returns index of closest point
    return ckdtree.query([x, y])[1]

def closest_point_coords(ckdtree, x, y):
    # returns coordinates of closest point
    return ckdtree.data[closest_point_id(ckdtree, x, y)]
    # ckdtree.data is the same as points