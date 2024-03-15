from matplotlib import pyplot as plt
import numpy as np

def add_arrow(lines, position=None, direction='forward', size=15, color='black'):
    """
    add an arrow to a line.

    line:       Line2D object or list of lines
    position:   x-position of the arrow. If None, mean of xdata is taken
    direction:  'left' or 'right'
    size:       size of the arrow in fontsize points
    color:      if None, line color is taken.
    """
    if isinstance(lines,type([])) == 0:
        lines = [lines]

    for line in lines:
        if color is None:
            color = line.get_color()
    
        xdata = line.get_xdata()
        ydata = line.get_ydata()
    
        if position is None:
            position = xdata.mean()
        # find closest index
        if direction == 'right':
            start_ind = np.argmin(np.absolute(xdata - position))
            end_ind = start_ind + 1
        elif direction == 'forward':
            start_ind = 0;
            end_ind = start_ind+1
        else:
            start_ind = np.argmin(np.absolute(xdata - position))
            end_ind = start_ind - 1

        #print(start_ind,end_ind)
        #print(xdata)
        #print(ydata)
        line.axes.annotate('',
            xytext=(xdata[start_ind], ydata[start_ind]),
            xy=(xdata[end_ind], ydata[end_ind]),
            arrowprops=dict(arrowstyle="->", color=color),
            size=size
        )