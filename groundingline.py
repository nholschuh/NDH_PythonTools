import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import mat73
import scipy.io

OnePath = '/mnt/NDH_data/Google_Drive2/'
ScriptPath = '/mnt/data01/Code/NDH_Tools/'
DataPath = '/mnt/data01/Data/'

import sys
sys.path.append('/mnt/data01/Code/')


def groundingline(num,m0_or_km1=0):
    
    from NDH_Tools import polarstereo_fwd
    """
    (C) Nick Holschuh - Amherst College - 2021 (Nick.Holschuh@gmail.com)
    plots the Antarctic Grounding Line
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    The inputs are as follows:

    num - This specifies the groundingline of interest:
          1: MODIS Groundingline
          2: IceSat Groundingline
          3: ASAID Groundingline
          4: MEASURES Groundingline
          5: Antarctica Outline
          6: Greenland Floatation Groundingline
          7: Greenland Outline
    m0_or_km1 - defines whether or not the output should be in m or km

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    The outputs are:

    newgl - the x/y coordinates of the plotted groundingline
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    # This section looks at how much of Antarctica is present in the plot, and
    # decides whether or not it should plot the entire groundingline data set
    # or just the subset that falls near the plotted zone.
    try:
        if m0_or_km1 == 0:
            mscaler = 1
        else:
            mscaler = 1/1000

        if num == 1:
            gl = mat73.loadmat(DataPath+'Antarctic_Groundinglines/MODIS_gl_ant/moa_gl.mat')['gl']

        elif num == 2:
            gl = mat73.loadmat(DataPath+'Antarctic_Groundinglines/IceSAT_gl_ant/ICEsat_gl.mat')['gl_3']
            ############### This was from the old matlab code, and should be implemented at some point
            #num2 = input(sprintf('1 - The landward limit of flexure\n2 - The point where ice is hydrostatically balanced\n3 - The break in slope associated with flexure\n'));
            #if num2 == 1
            #    gl = gl_1;
            #elseif num2 == 2
            #    gl = gl_2;
            #elseif num2 == 3
            #    gl = gl_3;


        elif num == 3:
            gl = mat73.loadmat(DataPath+'Antarctic_Groundinglines/ASAID_gl_ant/ASAID_groundingline.mat')['gl']
        elif num == 4:
            gl = mat73.loadmat(DataPath+'Antarctic_Groundinglines/measures_gl_ant/InSAR_gl.mat')['gl']
        elif num == 5:
            gl = np.array(pd.read_csv(OnePath+'Matlab_Code/NDH_Tools/CommonData_Searches/groundinglines/Ant_w_shelves.xy',header=None))
        elif num == 6:
            gl = np.array(pd.read_csv(DataPath+'Greenland_Groundinglines/NDH_Greenland_gl/greenland_gl.xy',header=None))
        elif num == 7:
            gl = np.array(pd.read_csv(DataPath+'Greenland_Groundinglines/NDH_Greenland_gl/Greenland_simplified_outline.xy',header=None))
        elif num == 8:
            gl = scipy.io.loadmat(OnePath+'Matlab_Code/NDH_Tools/CommonData_Searches/groundinglines/Antarctica_RoughGL.mat')['rough_gl']
        elif num == 9:
            gl = scipy.io.loadmat(OnePath+'Matlab_Code/NDH_Tools/CommonData_Searches/groundinglines/Greenland_RoughGL.mat')['rough_gl']; 
        elif num == 10:
            gl_data = gpd.read_file(DataPath+'Antarctic_Groundinglines/SIO_Groundingline/InSAR_GL_Antarctica_v02.shp')

            ############## Here, we build a numpy array, separating line strings with NaNs
            #### The first step is to initialize the 2-dimensional array
            gl = np.empty([2,0])
            for i in range(0,len(gl_data.geometry)):

                #### The file contains separate objects, some "linestrings", some "Multilinestrings".
                #### -- the explode method separates linestrings into series, and multilinestrings into linestrings
                gl_subset = gl_data.iloc[i].explode()

                #### This first section will work if the object was a Multilinestrings. If not, we need to abandon the loop
                try:
                    for k in range(0,len(gl_subset.geometry)):
                        gl_subset_3 = gl_subset.geometry[k]
                        next_array = np.array([gl_subset_3.xy[0],gl_subset_3.xy[1]])
                        gl = np.concatenate([gl,next_array,np.array([[np.nan],[np.nan]])],axis=1)
                except:
                    gl_subset_3 = gl_subset.geometry
                    next_array = np.array([gl_subset_3.xy[0],gl_subset_3.xy[1]])
                    gl = np.concatenate([gl,next_array,np.array([[np.nan],[np.nan]])],axis=1)   
            gl = gl.transpose()
            gl2 = polarstereo_fwd(gl[:,1],gl[:,0])
            gl = np.stack([gl2['x'],gl2['y']]).transpose()
        elif num==11:
            gl_data = gpd.read_file(DataPath+'Antarctic_Groundinglines/SIO_Groundingline/scripps_antarctica_polygons_v1.shp')

            ############## Here, we build a numpy array, separating line strings with NaNs
            #### The first step is to initialize the 2-dimensional array
            gl = np.empty([2,0])
            print(gl_data)
            for i in range(0,len(gl_data.geometry)):

                #### The file contains separate objects, some "linestrings", some "Multilinestrings".
                #### -- the explode method separates linestrings into series, and multilinestrings into linestrings
                gl_subset = gl_data.iloc[i].explode()

                #### This first section will work if the object was a Multilinestrings. If not, we need to abandon the loop
                try:
                    for k in range(0,len(gl_subset.geometry)):
                        gl_subset_3 = gl_subset.geometry[k]
                        next_array = np.array([gl_subset_3.xy[0],gl_subset_3.xy[1]])
                        gl = np.concatenate([gl,next_array,np.array([[np.nan],[np.nan]])],axis=1)
                except:
                    gl_subset_3 = gl_subset.geometry
                    next_array = np.array([gl_subset_3.xy[0],gl_subset_3.xy[1]])
                    gl = np.concatenate([gl,next_array,np.array([[np.nan],[np.nan]])],axis=1)   
            gl = gl.transpose()
            gl2 = polarstereo_fwd(gl[:,1],gl[:,0])
            gl = np.stack([gl2['x'],gl2['y']]).transpose()       


        gl = gl*mscaler;max(gl[:,1])
    
    except:
        print('The data files for this function aren\'t available on your machine. Sorry this is mostly for Nick\'s use...')
        gl = []
    
    return gl
