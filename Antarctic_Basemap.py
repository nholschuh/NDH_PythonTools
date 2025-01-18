import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd

def Antarctic_Basemap(base=0,xs=[0],ys=[0],gl=0,ax=0,base_varname=0,m0_or_km1=0):
    """
    % (C) Nick Holschuh - Amherst College -- 2024 (Nick.Holschuh@gmail.com)
    %
    % 
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %      base -- the dataset to use as a base
            # 0 - REMA Hillshade w/o velocity
            # 1 - REMA Hillshade w velocity
            # 2 - Bed Elevation
            # 3 - Surface Elevation
            # 4 - B2 Hillshade w/o velocity
            # 5 - B2 Hillshade w velocity
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %      The updated xarray dataset
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """    

    if m0_or_km1 == 0:
        scalar = 1
    else:
        scalar = 1000

    if isinstance(ax,int) == 1:
        ax = plt.gca()
    
    vel_flag = 0
    if isinstance(base,str):
        base_data = xr.open_dataset(base)
    else:
        if base == 0:
            data = xr.open_dataset('/mnt/data01/Data/Antarctic_Imagery/REMA_Hillshade/REMA_200m_hillshade_fixed.nc')
            base_varname = 'hillshade'
            cmap='gray'
        elif base == 1:
            data = xr.open_dataset('/mnt/data01/Data/Antarctic_Imagery/REMA_Hillshade/REMA_200m_hillshade_fixed.nc')
            base_varname = 'hillshade'
            cmap='gray'
            vel_flag = 1
        elif base == 2:
            data = xr.open_dataset('/mnt/data01/Data/Antarctic_BedElevation/BedMachineAntarctica-v3-2022-10-11.nc')
            base_varname = 'bed'
            cmap='terrain'
        elif base == 3:
            data = xr.open_dataset('/mnt/data01/Data/Antarctic_BedElevation/BedMachineAntarctica-v3-2022-10-11.nc')
            base_varname = 'surface'
            cmap='Blues'
        elif base == 4:
            data = xr.open_dataset('/mnt/data01/Data/Antarctic_Imagery/AntarcticB2_Hillshade/B2_Surface_Hillshade.nc')
            base_varname = 'z'
            cmap='gray'
            data = data.isel(y=slice(None, None, -1))
        elif base == 5:
            data = xr.open_dataset('/mnt/data01/Data/Antarctic_Imagery/AntarcticB2_Hillshade/B2_Surface_Hillshade.nc')
            base_varname = 'z'
            cmap='gray'
            data = data.isel(y=slice(None, None, -1))
            vel_flag = 1
    
    
    if len(xs) > 1:
        subset_slices = {'x':slice(xs[0],xs[1]),'y':slice(ys[1],ys[0])}
        data = data.sel(subset_slices)
    else:
        xs = np.array([np.min(data['x'].values),np.max(data['x'].values)])
        ys = np.array([np.min(data['y'].values),np.max(data['y'].values)])

    if scalar > 1:
        data['x'] = data['x']/scalar
        data['y'] = data['y']/scalar
    
    data[base_varname].plot.imshow(cmap=cmap,add_colorbar=False,ax=ax)
    
    if vel_flag == 1:
        veldata = xr.open_dataset('/mnt/data01/Data/Antarctic_Velocity/antarctic_ice_vel_phase_map_v01.nc')
        if len(xs) > 1:
            veldata = veldata.sel(subset_slices)    
        speed = np.sqrt(veldata['VX'].values**2+veldata['VY'].values**2)
        veldata['STDX'].values = speed
        if scalar > 1:
            veldata['x'] = veldata['x']/scalar
            veldata['y'] = veldata['y']/scalar
        veldata['STDX'].plot.imshow(cmap='magma',add_colorbar=False,ax=ax,alpha=0.3,vmax=100)

    if gl == 1:
        gl = pd.read_table('/mnt/data01/Data/Antarctic_Groundinglines/MODIS_gl_ant/moa_gl.xy',header=None,delimiter=',')
        plt.plot(gl[0]/scalar,gl[1]/scalar,c='black')
        plt.xlim(xs/scalar)
        plt.ylim(ys/scalar)

    if scalar == 1:
        plt.xlabel('Easting (m)')
        plt.ylabel('Northing (m)')
    else:
        plt.xlabel('Easting (km)')
        plt.ylabel('Northing (km)')
        
    ax.set_aspect('equal')
    plt.title(' ')



    