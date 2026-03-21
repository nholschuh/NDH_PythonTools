import pyvista as pv

def fence_initiate(vertical_exaggeration=5,give_example=1):
    """
    % (C) Nick Holschuh - Amherst College - 2026 (Nick.Holschuh@gmail.com)
    % This function uses PyVista to initiate an interactive fence diagram
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    % vertical_exaggeration - Scaling value for the vertical axis
    % give_example - 0: print nothing, 1: print just the code needed to finalize
    %                the html file, 2: print a full example of how to use fence functions
    %
    %%%%%%%%%%%%%%%
    % The output is a dictionary containing:
    %
    % plotter - The plotter object which can be passed into later functions
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    plotter = pv.Plotter()
    plotter.show_axes()
    plotter.enable_eye_dome_lighting() # Makes 3D features pop with subtle shadows
    plotter.set_scale(zscale=vertical_exaggeration)

    #plotter.view_isometric() # The classic 3D angled corner view
    plotter.view_xy()      # Top-down view
    # plotter.view_xz()      # Side-profile view

    #plotter.show_grid(
    #    xlabel='PS_x (m)',
    #    ylabel='PS_y (m)',
    #    zlabel='Elevation (m)',
    #    font_size=14,
    #    color='black',       # Color of the text and grid lines
    #    location='outer',    # Keeps the labels on the outside of the 3D box
    #    grid=False           # Set to True if you want physical grid lines drawn inside the box
    #)

    if give_example == 1:
        print('Add the following to your cell (fname should end in .html):')
        print(' ')
        print('plotter.reset_camera()')
        print('plotter.render()')
        print('plotter.export_html(fname)')
        print(' ')
    elif give_example == 2:
        print("""
            fname = 'Test_fence.html'
            plotter = ndh.fence_initiate(5)
            
            radar_data,depth_data =  ndh.radar_load('/mnt/data01/Data/RadarData/ElephantMoraine_Helicopter/IRFOC1B_2018330_ELM1_IBH0g_Y91a_001.mat')
            plotter, mesh1 = ndh.fence_add_radar(plotter,radar_data,depth_data,vmin=150,vmax=200)
            
            radar_data,depth_data =  ndh.radar_load('/mnt/data01/Data/RadarData/ElephantMoraine_Helicopter/IRFOC1B_2018331_ELM1_IBH0g_X57a_000.mat')
            plotter, mesh2 = ndh.fence_add_radar(plotter,radar_data,depth_data,vmin=150,vmax=200)
            
            dem_image = xr.open_dataset('DEM_and_Image_EM.nc')
            plotter, mesh3 = ndh.fence_add_surface(plotter,dem_image['x'].values,dem_image['y'].values,dem_image['dem'].values,dem_image['ah'].values)
            
            plotter.reset_camera()
            plotter.render() 
            plotter.export_html(fname)
        """)

    return plotter