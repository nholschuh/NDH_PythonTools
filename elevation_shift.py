import numpy as np
import sys
sys.path.append('/mnt/data01/Code/')

from NDH_Tools import find_nearest
from NDH_Tools import interpNaN 

def elevation_shift(data,time,surface,elevation,bed,disp_flag=0):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This converts radar data in time to true elevation coordinates (WGS84)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    % data - The radar data matrix
    % time - The time axis for the data
    % surface - the surface pick (should theoretically accept both index or
    %           time values)
    % elevation - array containing the flight elevation
    % bed - if exists, the bed pick
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The function returns a dictionary with the following keys:
    %
    % new_data - The data adjusted for flight elevation
    % shift_amount - The number of indecies each column has been shifted 
    %                (Subtract this value from picks to correct them) 
    % depth_axis - The new Z axis for the data
    % surface_elev - The elevation for the new surface
    % bed_elev - The bed elevation if bed pick is supplied
    % multiple - The depth associated with an expected surface multiple
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%
    """

    if np.nanmax(np.mod(surface,1)) == 0:
        ind_flag = 1;
    else:
        ind_flag = 0;

    if np.max(surface) == 0:
        ind_flag = 0

    ########   Fix the orientation of certain objects
    ss = surface.shape
    if len(ss) > 1:
        surface = np.squeeze(surface)
    #    surface = surface.transpose()

    st = time.shape
    if len(st) > 1:
        time = np.squeeze(time)
    #    if st[1] == 1:
    #        time = time.transpose()

    if ind_flag == 1:
        surf_time = time[surface.astype(int)-1]
    else:
        surf_time = surface
    
    ####### How to test for existence??
    if 'disp_flag' not in locals():
        disp_flag = 0

    cair =  299792458;
    cice = cair/np.sqrt(3.15)


    ## Computes ice thickness if the bed pick is supplied
    if 'bed' in locals():
        sb = bed.shape;
        if len(sb) > 1:
            bed = bed.transpose()


        if np.nanmin(np.mod(bed,1)) == 0:
            ind_flag2 = 1
        else:
            ind_flag2 = 0

        if ind_flag2 == 1:
            temp_inds = interpNaN(bed)
            temp_inds[np.where(temp_inds < 1)] = 1
            bed_time = time[np.round(temp_inds).astype(int)-1];
        else:
            bed_time = bed

        thickness_time = bed_time-surf_time
        thickness = thickness_time*cice/2
        
    ######### Here we identify the expected surface multiple in depth:
    multiple_time = surf_time*2
    multiple_thickness = (multiple_time-surf_time)*cice/2

    ## Here we produce the new objects
    new_data1 = np.zeros(data.shape)
    new_data2 = np.zeros(data.shape)

    dt = time[1]-time[0]
    dx = cice*dt/2

    steps = np.floor(len(data[1,:])/10)

    filled_inds = np.where(np.isnan(surface) == 0)[0]
    unfilled_inds = np.where(np.isnan(surface) == 1)[0]


    ### This fills NaN's with the closest picked value
    for i in np.arange(len(unfilled_inds)):
        replace_ind = find_nearest(filled_inds,unfilled_inds[i])
        #[trash replace_ind]
        surface[unfilled_inds[i]] = surface[replace_ind['index'][0]]


    ### This first forces the surface to be the 0th index.
    shift_amount1 = np.zeros(len(data[1,:]))
    surface_elev = np.zeros(len(data[1,:]))
    for i in np.arange(len(data[1,:])):
        if ind_flag == 0:
            temp = find_nearest(time,np.array([surface[i]]))
            shift_amount1[i] = temp['index'][0]
        else:
            shift_amount1[i] = np.round(surface[i])

        surface_elev[i] = elevation[i] - time[int(shift_amount1[i])]*cair/2
        select_inds = np.arange(shift_amount1[i],len(time),1)
        new_data1[np.arange(len(select_inds)),i] = data[select_inds.astype(int),i]
        if np.mod(i-1,steps) == 0:
            if disp_flag == 1:
                print(str(np.round(10*(i-1)/steps)+'% Complete - Surface Shift'))


    top = np.max(surface_elev) + 100


    surface_elev = interpNaN(surface_elev);

    shift_amount2 = np.zeros(len(data[1,:]))
    for i in np.arange(len(data[1,:])):
        shift_amount2[i] = np.round((top-surface_elev[i])/dx)
        select_inds = np.arange(len(time)-shift_amount2[i])
        new_data2[int(shift_amount2[i]):,i] = new_data1[select_inds.astype(int),i]
        if np.mod(i-1,steps) == 0:
            if disp_flag == 1:
                print(str(np.round(10*(i-1)/steps)+'% Complete - Elevation Shift'))


    shift_amount = shift_amount1-shift_amount2
    new_data = new_data2
    depth_axis = top-np.arange(0,dx*(len(time)),dx)

    ## This computes the bed elevation if it is supplied
    if 'bed' in locals():
        bed_elev = surface_elev - thickness;
    else:
        bed_elev = np.ones(surface_elev.shape)*np.NaN;
        
    multiple = surface_elev-multiple_thickness;

    return {'new_data':new_data2, 'shift_amount':shift_amount, 'depth_axis':depth_axis, 'surface_elev':surface_elev, 'bed_elev':bed_elev, 'multiple':multiple}