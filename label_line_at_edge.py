import numpy as np
import matplotlib.pyplot as plt

def label_line_at_edge(ax, line_coords, xlims, ylims, label_text, edge_flag=None, color='black'):
    """
    Finds where a line intersects the bounding box and adds a label outside the axis,
    restricted by a specific edge flag.
    
    Parameters:
    - ax: Matplotlib axes object
    - line_coords: nx2 numpy array of [x, y] coordinates
    - xlims: tuple of (xmin, xmax)
    - ylims: tuple of (ymin, ymax)
    - label_text: string to label the line
    - edge_flag: int 1-4 specifying allowed edges to label.
                 1: Left & Bottom
                 2: Right & Bottom
                 3: Right & Top
                 4: Left & Top
                 None: All edges allowed
    - color: color of the text
    """
    # 1. Map the integer flag to the allowed edges
    valid_edges_map = {
        1: ['left', 'bottom'],
        2: ['right', 'bottom'],
        3: ['right', 'top'],
        4: ['left', 'top']
    }
    
    # Default to all edges if no valid flag is provided
    allowed_edges = valid_edges_map.get(edge_flag, ['left', 'right', 'top', 'bottom'])

    xmin, xmax = xlims
    ymin, ymax = ylims
    x, y = line_coords[:, 0], line_coords[:, 1]
    
    # 2. Identify points inside the bounding box
    inside = (x >= xmin) & (x <= xmax) & (y >= ymin) & (y <= ymax)
    
    # If no points are inside, skip
    if not np.any(inside):
        return 
        
    # 3. Find ALL transitions (both entering and exiting the box)
    # inside[:-1] != inside[1:] returns True wherever the line crosses the boundary
    transitions = np.where(inside[:-1] != inside[1:])[0]
    
    # 4. Iterate through each boundary crossing until we find one on an allowed edge
    for idx in transitions:
        x1, y1 = x[idx], y[idx]
        x2, y2 = x[idx+1], y[idx+1]
        
        dx = x2 - x1
        dy = y2 - y1
        
        t_candidates = []
        if dx != 0:
            t_candidates.append(((xmin - x1) / dx, 'left'))
            t_candidates.append(((xmax - x1) / dx, 'right'))
        if dy != 0:
            t_candidates.append(((ymin - y1) / dy, 'bottom'))
            t_candidates.append(((ymax - y1) / dy, 'top'))
            
        for t, edge in t_candidates:
            if -1e-6 <= t <= 1 + 1e-6: # Account for floating point precision
                ix = x1 + t * dx
                iy = y1 + t * dy
                
                # Verify the intersection point lies within the box limits
                if (xmin - 1e-6 <= ix <= xmax + 1e-6) and (ymin - 1e-6 <= iy <= ymax + 1e-6):
                    
                    # NEW: Only label if the intersected edge is in our allowed list
                    if edge in allowed_edges:
                        
                        if edge == 'right':
                            ha, va, xytext = 'left', 'center', (5, 0)
                        elif edge == 'left':
                            ha, va, xytext = 'right', 'center', (-5, 0)
                        elif edge == 'top':
                            ha, va, xytext = 'center', 'bottom', (0, 5)
                        elif edge == 'bottom':
                            ha, va, xytext = 'center', 'top', (0, -5)
                            
                        ax.annotate(label_text, xy=(ix, iy), xytext=xytext, 
                                    textcoords='offset points', ha=ha, va=va, 
                                    color=color, clip_on=False, fontweight='bold')
                        return # Exit the function once we've successfully placed a label
