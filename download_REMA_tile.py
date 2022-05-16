import geopandas as gpd
import numpy as np
from os.path import exists
import requests
from shapely.geometry import MultiPoint
import subprocess
import warnings

warnings.filterwarnings("ignore")

def download_REMA_tile(xs,ys,final_path='/mnt/data01/Data/Antarctic_SurfaceElevation/REMA_Tiles/',all_files=0):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This function downloads REMA tiles associated with the x and y
    % input coordinates provided to the function.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    % xs - x_coordinates (polarstereo) where you want REMA coverage
    % ys - y_coordinates (polarstereo) where you want REMA coverage
    % final_path - the path to place your REMA tiles
    % all_files - flag, whether to keep all the rema files [1] or just the elevation tif [0]   
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The function returns the following objects:
    %
    % file_list - a list of all the files you need to cover your area (and their full path)
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%
    """
    
    #### This section reads the tile shape file
    tile_file_exists = exists(final_path+'REMA_Tile_Index_Rel1_1.shp')
    if tile_file_exists == False:
        print('Downloading and Reading the tile shape file')
        ############# This handles the case where the tile shape file doesn't already exist
        url = 'https://data.pgc.umn.edu/elev/dem/setsm/REMA/indexes/REMA_Tile_Index_Rel1.1.zip'
        tile_file = final_path+'temp.zip'
        
        r = requests.get(url, verify=False)
        with requests.get(url, stream=True, verify=False) as r:
                r.raise_for_status()
                with open(tile_file, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): 
                        # If you have chunk encoded response uncomment if
                        # and set chunk_size parameter to None.
                        #if chunk: 
                        f.write(chunk)
        bash_command = 'unzip '+tile_file+' -d '+final_path
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        bash_command = 'rm '+tile_file
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()   
    else:
        print('Reading the tile shape file')
           

    data = gpd.read_file(final_path+'REMA_Tile_Index_Rel1_1.shp')  
    target = MultiPoint(np.array([xs,ys]))

    ######### Here is the debug plot information
    #data.plot()
    #for i in target:
    #    plt.plot(i.x,i.y,'o',color='red')
    
    ################# Here we find the indecies in the tile file to download
    ki = []
    for i in target:
        vals = data.buffer(10**-1).contains(i)
        vals = [vals]
        trash, ki_temp = np.where(vals)
        ki = np.concatenate([ki,ki_temp])

    ki = np.unique(ki).astype('int')
    

    ################# Here we loop through the files we need to download
    file_list = []
    
    for i in ki:
        url = data.iloc[i]['fileurl']
        fname = url.split('/')[-1].split('.')[0]+'_dem.tif'

        file_exists = exists(final_path+fname)
        if file_exists:
            print('Already Have File -- '+fname)
        else:
            ########## Here we set the filename
            local_filename = final_path+'temp.tar'

            ########## This does the downloading
            r = requests.get(url, verify=False)
            with requests.get(url, stream=True, verify=False) as r:
                    r.raise_for_status()
                    with open(local_filename, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192): 
                            # If you have chunk encoded response uncomment if
                            # and set chunk_size parameter to None.
                            #if chunk: 
                            f.write(chunk)
            if all_files == 0:
                bash_command = 'tar -xvf '+local_filename+' --directory '+final_path+' '+fname
            else:
                bash_command = 'tar -xvf '+local_filename+' --directory '+final_path
                                
           
            process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
                                
            bash_command = 'rm '+local_filename
            process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            print('Successfully Downloaded -- '+fname)
            
        file_list.append(final_path+fname)
            
    return file_list