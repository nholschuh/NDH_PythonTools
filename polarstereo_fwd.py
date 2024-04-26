from pyproj import Transformer
import numpy as np

def polarstereo_fwd(latitude,longitude,ant0_or_gre1=2):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    %     This function will output a data dictionary containing transformed coordinates. 
    %     It automatically detects (based on latitude) if your data should be converted 
    %     to Antarctic polarstereographic coordinates or the arctic sea ice projection 
    %     for Greenland.
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     latitude -- Latitude values for coordinate reprojection
    %     longitude -- Longitude values for coordinate reprojection
    %     ant0_or_gre1 -- an explicit declaration of antarctica or greenland for projection.
    %                     If set to 2, it will try to determine automatically based on lat
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %     x -- x-polarstereographic coordinates
    %     y -- y-polarstereographic coordinates
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 


    LL_proj = "epsg:4326"
    A_proj = "epsg:3031"
    G_proj = "epsg:3413"   # 45 W Center

    if ant0_or_gre1 == 2:
        if np.nanmedian(latitude) < 0:
            transformer = Transformer.from_crs(LL_proj, A_proj)
        else:
            transformer = Transformer.from_crs(LL_proj, G_proj)
    elif ant0_or_gre1 == 0:
        transformer = Transformer.from_crs(LL_proj, A_proj)
    elif ant0_or_gre1 == 1:
        transformer = Transformer.from_crs(LL_proj, G_proj)
    
    if isinstance(latitude,type(np.array([]))) == False:
        latitude = np.array(latitude)
        longitude = np.array(longitude)
    
    x,y = transformer.transform(latitude,longitude)

    if isinstance(x,type([])) == False:
         return {'x':np.array(x), 'y':np.array(y)}         
    else:
        return {'x':x[0], 'y':y[0]}