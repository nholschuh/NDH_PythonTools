from pyproj import Transformer
import numpy as np

def polarstereo_inv(x,y,ant_or_green=0):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    %     This function will output a data dictionary containing polarstereographic
    %     coordinates and convert them to latitude and longitude
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     x -- x-polarstereographic coordinates
    %     y -- y-polarstereographic coordinates    
    %     ant_or_green -- this flag determines whether you are looking at antarctic or greenland data
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %     lat -- Latitude values for coordinate reprojection
    %     long -- Longitude values for coordinate reprojection
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 

    LL_proj = "epsg:4326"
    A_proj = "epsg:3031"
    G_proj = "epsg:3413"   # 45 W Center

    if ant_or_green == 0:
        transformer = Transformer.from_crs(A_proj, LL_proj)
    else:
        transformer = Transformer.from_crs(G_proj, LL_proj)
    
    
    lat,long = transformer.transform(x,y)
    
    

    if isinstance(x,type([])) == False:
        return {'lat':np.array(lat), 'long':np.array(long)}    
    else:
        return {'lat':lat[0], 'long':long[0]}