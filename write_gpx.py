import numpy as np

def write_gpx(new_filename,lats,lons,names,waypoints0_or_routes1=0,route_name='Temp Route',symbol='City (Large)'):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This function write a gpx waypoint file or route file
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %    lats -- latitudes for each waypoint
    %    lons -- longitudes for each waypoint
    %    names -- names for each waypoint
    %    waypoints0_or_routes1 -- if you want the values saved as waypoints or routes
    %    route_name -- string containing the name of the route
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    %    new_data -- the smoothed data
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    ############### Alternative Symbol Options
    # Flag, Blue
    #
    #
    #
    

    with_extensions = 0
    ################## Header
    first_lines_str = '<?xml version="1.0"?>\n<gpx version="1.1" creator="GDAL 3.6.3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ogr="http://osgeo.org/gdal" xmlns="http://www.topografix.com/GPX/1/1" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">\n'
    metadata_bounds_str = '<metadata><bounds minlat="%f" minlon="%f" maxlat="%f" maxlon="%f"/></metadata>\n' 

    ################## Route Entry strings
    rte_start_str = '<rte>\n<name>%s</name>'
    rte_entry_str = '<rtept lat="%f" lon="%f">\n  <name>%s</name>\n  <extensions>\n    <ogr:lat>%f</ogr:lat>\n    <ogr:lon>%f</ogr:lon>\n  </extensions>\n</rtept>\n'
    rte_entry_str_noextentions = '<rtept lat="%f" lon="%f">\n  <name>%s</name>\n </rtept>\n'
    rte_end_str = '</rte>\n</gpx>'

    ################## Waypoint Entry strings
    wpt_entry_str = '<wpt lat="%f" lon="%f">\n  <name>%s</name>\n  <extensions>\n    <ogr:lat>%f</ogr:lat>\n    <ogr:lon>%f</ogr:lon>\n  </extensions>\n</wpt>'
    wpt_entry_str_noextensions = '<wpt lat="%f" lon="%f">\n  <name>%s</name>\n <sym>%s</sym>\n</wpt>'
    wpt_end_str = '</gpx>'


    minlat = np.min(lats)
    minlon = np.min(lons)
    maxlat = np.max(lats)
    maxlon = np.max(lons)

    ################# Here we open the file for writing
    fid = open(new_filename,'wt');
    fid.write(first_lines_str)
    fid.write(metadata_bounds_str % (minlat,minlon,maxlat,maxlon))

    if waypoints0_or_routes1 == 1:
        fid.write(rte_start_str % (route_name))

    for ind0,wpt_name in enumerate(names):
        wpt_lat = lats[ind0]
        wpt_lon = lons[ind0]
        if waypoints0_or_routes1 == 0:
            if with_extensions == 0:
                fid.write(wpt_entry_str_noextensions % (wpt_lat,wpt_lon,wpt_name,symbol))
            else:
                fid.write(wpt_entry_str_noextensions % (wpt_lat,wpt_lon,wpt_name,wpt_lat,wpt_lon))
        else:
            if with_extensions == 0:
                fid.write(rte_entry_str_noextentions % (wpt_lat,wpt_lon,wpt_name))
            else:
                fid.write(rte_entry_str_noextentions % (wpt_lat,wpt_lon,wpt_name,wpt_lat,wpt_lon))

    if waypoints0_or_routes1 == 1:
        fid.write(rte_end_str)
    else:
        fid.write(wpt_end_str)

    fid.close()