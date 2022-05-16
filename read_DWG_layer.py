import sys
import numpy as np
import ezdxf

def read_DWG_layer(layer_name, dxf_file_data):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    %     This function takes a layer name (determined from 'get_DWG_layers')
    %     and exctracts the associated values
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     layer_name -- string containing the layer name to read
    %     dxf_file_data -- the dxf_file_data gotten from library 'ezdxf' read
    %                      using module ezdxf.readfile
    %
    %%%%%%%%%%%%%%%
    % The output is a data dictionary with the following keys:
    %
    %     'sx': segments_x, 
    %      'sy': segments_y, 
    %      'stype': entry_type, 
    %      'snum': entry_num, 
    %      'text_strings': text_strings, 
    %      'text_x': text_x, 
    %      'text_y': text_y, 
    %      'hatch_x': hatch_x, 
    %      'hatch_y': hatch_y
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %% This is mostly a subroutine for "read_DWG"
    """ 
    
    msp = dxf_file_data.modelspace()
    Building_Outlines = msp.query('*[layer=="'+layer_name+'"]')
    
    
    segments_x = []
    segments_y = []

    entry_type = []
    entry_num = []

    hatch_x = []
    hatch_y = []

    text_strings = []
    text_x = []
    text_y = []

    for ind,e in enumerate(Building_Outlines):

        if e.dxf.dxftype == 'LINE':
            segments_x.append(e.dxf.start[0])
            segments_x.append(e.dxf.end[0])
            segments_y.append(e.dxf.start[1])
            segments_y.append(e.dxf.end[1])  

            entry_type.append(1)
            entry_num.append(ind)
            entry_type.append(1)
            entry_num.append(ind)

        elif e.dxf.dxftype == 'ARC':
            
            if e.dxf.start_angle > e.dxf.end_angle:
                rads = np.concatenate([np.linspace(e.dxf.start_angle,360,50)/360*2*np.pi,
                                     np.linspace(0,e.dxf.end_angle,50)/360*2*np.pi])
            else:
                rads = np.linspace(e.dxf.start_angle,e.dxf.end_angle,50)/360*2*np.pi
            xs = np.cos(rads)*e.dxf.radius+e.dxf.center[0]
            ys = np.sin(rads)*e.dxf.radius+e.dxf.center[1]
            for i in range(0,len(xs)):
                segments_x.append(xs[i])
                segments_y.append(ys[i])
                entry_type.append(2)
                entry_num.append(ind)

        elif e.dxf.dxftype == "POLYLINE":
            itemlength = e.__len__()
            for i in range(0,itemlength):
                pvals = e.__getitem__(i).format(format='xyz')
                segments_x.append(pvals[0])
                segments_y.append(pvals[1]) 
                entry_type.append(3)
                entry_num.append(ind)

        elif e.dxf.dxftype == 'LWPOLYLINE':
            itemlength = e.__len__()
            for i in range(0,itemlength):
                pvals =  e.__getitem__(i)
                segments_x.append(pvals[0])
                segments_y.append(pvals[1])
                entry_type.append(4)
                entry_num.append(ind)

            if e.closed:
                pvals =  e.__getitem__(0)
                segments_x.append(pvals[0])
                segments_y.append(pvals[1])
                entry_type.append(4)
                entry_num.append(ind)            

        elif e.dxf.dxftype == 'CIRCLE':
            if e.dxf.radius < 5000:
                rads = np.linspace(0,2*np.pi,100)
                xs = np.cos(rads)*e.dxf.radius+e.dxf.center[0]
                ys = np.sin(rads)*e.dxf.radius+e.dxf.center[1]

                for i in range(0,len(xs)):
                    segments_x.append(xs[i])
                    segments_y.append(ys[i])
                    entry_type.append(5)
                    entry_num.append(ind)

        elif e.dxf.dxftype == 'ELLIPSE':
            rads = np.linspace(0,2*np.pi,100)
            vert_iterable = e.vertices(rads)

            for i in range(0,len(rads)):
                vert = next(vert_iterable)
                segments_x.append(vert[0])
                segments_y.append(vert[1]) 
                entry_type.append(6)
                entry_num.append(ind)

        elif e.dxf.dxftype == 'SPLINE':
            for i in range(0,e.fit_point_count()):
                segments_x.append(e.fit_points.__getitem__(i)[0])
                segments_y.append(e.fit_points.__getitem__(i)[1])
                entry_type.append(7)
                entry_num.append(ind)

        elif e.dxf.dxftype == 'TEXT':   
            text_strings.append(e.dxf.text)
            text_x.append(e.get_pos()[1][0])
            text_y.append(e.get_pos()[1][1])

        elif e.dxf.dxftype == 'MTEXT':   
            text_strings.append(e.text)
            text_x.append(e.dxf.insert[0])
            text_y.append(e.dxf.insert[1])

        elif e.dxf.dxftype == 'DIMENSION':
            pass

        elif e.dxf.dxftype == 'INSERT':
            pass

        elif e.dxf.dxftype == 'HATCH':
            sub_hatch_x = []
            sub_hatch_y = []

            for i in e.paths.paths:
                try:
                    popts = i.vertices
                    for j in popts:
                        sub_hatch_x.append(j[0])
                        sub_hatch_x.append(j[1])
                except:
                    for j in i.edges:
                        if j.EDGE_TYPE == 'LineEdge':
                            sub_hatch_x.append(j.start[0])
                            sub_hatch_x.append(j.end[0])
                            sub_hatch_y.append(j.start[1])
                            sub_hatch_y.append(j.end[1])  

                        elif j.EDGE_TYPE == 'ArcEdge':
                            if j.start_angle > j.end_angle:
                                  rads = np.concatenate([np.linspace(j.start_angle,360,50)/360*2*np.pi,
                                     np.linspace(0,j.end_angle,50)/360*2*np.pi])                             
                            else:
                                rads = np.linspace(j.start_angle,j.end_angle,50)
                            xs = np.cos(rads)*j.radius+j.center[0]
                            ys = np.sin(rads)*j.radius+j.center[1]
                            for i in range(0,len(xs)):
                                sub_hatch_x.append(xs[i])
                                sub_hatch_y.append(ys[i])

                        elif j.EDGE_TYPE == 'EllipseEdge':
                            pass

                        elif j.EDGE_TYPE == 'SplineEdge':
                            pass
        else:

            pass

        segments_x.append(np.NaN)
        segments_y.append(np.NaN) 
        entry_type.append(10)
        entry_num.append(ind)
        

        
    segments_x = np.array(segments_x)
    segments_y = np.array(segments_y)
    entry_type = np.array(entry_type)
    entry_num = np.array(entry_num)
    text_x = np.array(text_x)
    text_y = np.array(text_y)
    
    output = {'sx': segments_x, 'sy': segments_y, 'stype': entry_type, 'snum': entry_num, 'text_strings': text_strings, 'text_x': text_x, 'text_y': text_y, 'hatch_x': hatch_x, 'hatch_y': hatch_y}
    
    return output
    
