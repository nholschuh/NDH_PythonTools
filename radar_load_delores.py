import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
import glob
import os

###########################################################
################## NDH Tools self imports
from .elevation_shift import elevation_shift
from .depth_shift import depth_shift
from .distance_vector import distance_vector
from .polarstereo_inv import polarstereo_inv
############################################################

def radar_load_delores(fn,plot_flag=0,elevation1_or_depth2=1,trace_spacing=1,load_data=1,
                       pick_dir='/mnt/data01/Data/RadarData/Delores_GHOST/Picks_ReflexW_PCK',pick_tol=5,fc=3e6):
    """
    % (C) Nick Holschuh - Amherst College -- 2026 (Nick.Holschuh@gmail.com)
    %
    %     Loads a DELORES ground-based impulse GPR profile, stored as a ReflexW .##R/.##T pair,
    %     into the same structure that radar_load produces for CReSIS data, so the two can be
    %     handled by the same code (depth_shift, plotting, crossovers, etc).
    %
    %     The system is on the ground, so the surface is taken to be time 0 (Surface = 0).
    %     Coordinates come from the ReflexW trace headers, which store polar stereographic
    %     x/y (EPSG:3031) -- Latitude/Longitude are back-projected from those.
    %
    %     ReflexW layout (little-endian):
    %       .R header -- int32 nsamples/ntraces at 0x1A4/0x1A8, int32 data format at 0x1C4
    %                    (2 = int16, 3 = float32), float64 sample interval (ns) at 0x1F4
    %       .T traces -- each trace is a header (156 bytes for int16, 158 for float32) then the
    %                    samples; in the trace header, float64 elevation at byte 38, distance at 46,
    %                    x/y at 54/62
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     fn -- the .T (or .R) filename, or a list of them to be concatenated in order
    %     plot_flag -- 0 or 1, for whether or not you want a plot included
    %     elevation1_or_depth2 -- 1 for true elevation, 2 for depth in ice, 0 for an empty object
    %     trace_spacing -- keep every Nth trace
    %     load_data -- 0 to read only the trace-header geometry (fast; no 'Data', no depth product)
    %     pick_dir -- folder of ReflexW .PCK bed picks, used to fill 'Bottom' (None to skip)
    %     pick_tol -- picks are placed on the nearest trace by x/y, if within this many metres
    %     fc -- center frequency (Hz), which ReflexW does not store
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %     radar_data -- CReSIS-style keys: 'Data' (nsamples x ntraces; this is the processed ReflexW
    %                   amplitude, not power), 'Time' (s), 'Surface' (s, zeros), 'Bottom' (s, from the
    %                   ReflexW picks, NaN where unpicked), 'Elevation', 'Latitude', 'Longitude',
    %                   'GPS_time' (NaN, not stored), plus 'x', 'y', 'distance', 'im_end',
    %                   'orig_ind', 'filename', 'fc'
    %     depth_data -- the depth or elevation product
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    if isinstance(fn,list) == 0:
        fn = [fn]

    concat_list = ['Elevation','GPS_time','Latitude','Longitude','Surface','Bottom','x','y']

    ############## Here we loop through the profiles and concatenate them
    for fn_ind,fn_temp in enumerate(fn):
        fn_base = fn_temp[:-1]

        ############## The .R header
        hdr = np.fromfile(fn_base+'R',dtype=np.uint8).tobytes()
        nsamples,ntraces = [int(x) for x in np.frombuffer(hdr[0x1A4:0x1AC],'<i4')]
        sample_type = {2:'<i2',3:'<f4'}[int(np.frombuffer(hdr[0x1C4:0x1C8],'<i4')[0])]
        dt = np.frombuffer(hdr[0x1F4:0x1FC],'<f8')[0]*1e-9

        ############## The .T traces -- trace length from the file size, since the header length varies
        t_fn = fn_base+'T'
        trace_bytes = os.path.getsize(t_fn)//ntraces
        header_bytes = trace_bytes-nsamples*np.dtype(sample_type).itemsize
        traces = np.memmap(t_fn,dtype=np.uint8,mode='r',shape=(ntraces,trace_bytes))[::trace_spacing]
        geom = np.ascontiguousarray(traces[:,38:70]).view('<f8')

        radar_temp = {}
        radar_temp['Elevation'] = geom[:,0]
        radar_temp['x'] = geom[:,2]
        radar_temp['y'] = geom[:,3]
        ll = polarstereo_inv(radar_temp['x'],radar_temp['y'])
        radar_temp['Latitude'] = ll['lat']
        radar_temp['Longitude'] = ll['long']
        radar_temp['GPS_time'] = np.full(len(geom),np.nan)
        radar_temp['Surface'] = np.zeros(len(geom))
        radar_temp['Bottom'] = np.full(len(geom),np.nan)
        if load_data == 1:
            radar_temp['Data'] = np.ascontiguousarray(traces[:,header_bytes:]).view(sample_type).T.astype(float)

        ############## Bed picks (TWTT in ns) from the ReflexW pick files, matched by profile name
        # columns: profile, trace, distance, -, x, y, elevation, TWTT (ns), depth (m), amplitude.
        # Picks are placed by x/y rather than trace number -- some pick files were made on a longer or
        # re-cut version of the profile, so their trace numbers are offset from (or run past) the file
        if pick_dir is not None:
            profile = os.path.basename(t_fn)
            tree = cKDTree(np.stack([radar_temp['x'],radar_temp['y']]).T)
            for pck in glob.glob(f'{pick_dir}/{profile.split("_")[1]}*.PCK'):
                picks = pd.read_csv(pck,sep=r'\s+',header=None)
                picks = picks[picks[0].str.upper()==profile.upper()]
                if len(picks) == 0:
                    continue
                sep,trace_ind = tree.query(picks[[4,5]].values.astype(float))
                keep = sep < pick_tol
                radar_temp['Bottom'][trace_ind[keep]] = picks[7].values[keep].astype(float)*1e-9

        if fn_ind == 0:
            radar_data = radar_temp
            radar_data['Time'] = np.arange(nsamples)*dt
            radar_data['im_end'] = [0,len(geom)]
            radar_data['orig_ind'] = np.arange(0,len(geom))*trace_spacing
            radar_data['filename'] = [os.path.basename(t_fn)]
        else:
            if nsamples != len(radar_data['Time']) or dt != radar_data['Time'][1]-radar_data['Time'][0]:
                raise ValueError(f'{os.path.basename(t_fn)} has a different time axis than the first file')
            for key in concat_list:
                radar_data[key] = np.concatenate([radar_data[key],radar_temp[key]])
            if load_data == 1:
                radar_data['Data'] = np.concatenate([radar_data['Data'],radar_temp['Data']],axis=1)
            radar_data['im_end'].append(len(radar_data['x']))
            radar_data['orig_ind'] = np.concatenate([radar_data['orig_ind'],np.arange(0,len(geom))*trace_spacing])
            radar_data['filename'].append(os.path.basename(t_fn))

    radar_data['distance'] = distance_vector(radar_data['x'],radar_data['y'])
    radar_data['fc'] = fc

    ############# Here we do the depth or elevation shift
    if load_data == 0 or elevation1_or_depth2 == 0:
        depth_data = 'No depth data requested'
    elif elevation1_or_depth2 == 1:
        depth_data = elevation_shift(radar_data['Data'],radar_data['Time'],radar_data['Surface'],radar_data['Elevation'],radar_data['Bottom'])
    elif elevation1_or_depth2 == 2:
        depth_data = depth_shift(radar_data['Data'],radar_data['Time'],radar_data['Surface'],radar_data['Elevation'],radar_data['Bottom'])
    else:
        depth_data = 'No depth data requested'

    ############# The data are signed amplitude, so plot them linearly with a symmetric color scale
    if plot_flag == 1 and load_data == 1:
        if isinstance(depth_data,dict):
            image = depth_data['new_data']
            y_axis = depth_data['depth_axis']
        else:
            image = radar_data['Data']
            y_axis = radar_data['Time']*1e9
        clim = np.percentile(np.abs(image[:,::10]),98)

        plt.figure(figsize=(15,7))
        imdata = plt.imshow(image,extent=[radar_data['distance'][0]/1000,radar_data['distance'][-1]/1000,y_axis[-1],y_axis[0]],
                            aspect='auto',cmap='gray_r',vmin=-clim,vmax=clim)
        plt.colorbar(imdata)
        plt.xlabel('Distance (km)')
        if elevation1_or_depth2 == 2:
            plt.ylabel('Depth (m)')
        elif elevation1_or_depth2 == 1:
            plt.ylabel('Elevation w.r.t WGS84 (m)')
            plt.gca().invert_yaxis()
        else:
            plt.ylabel('Two-way travel time (ns)')

    return radar_data,depth_data
