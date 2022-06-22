import os
import glob
import pdb
import numpy as np
import matplotlib.path as pltpath
from scipy.io import loadmat
import inspect

def is2_fileselect(xbounds, ybounds, fdir='/data/rd08/projects/IS2/ATL06', ant_or_green=0, filetype='ATL06', cycle=6, print_flag=0):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    % This function identifies the files and the segids for ICESat-2 data that falls within
    % a boundingbox of interest.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     xbounds -- two values that define the minimum x and maximum x coord (polar stereographic)
    %     ybounds -- two values that define the minumum y and maximum y coord (polar stereographic)
    %     fdir -- the absolute path to the directory where the ATL06/11 files are stored
    %     ant_or_green -- Specifices which region range to select from
    %     filetype -- string, currently only 'ATL06' is implemented
    %     cycle -- the cycle number for plotting, from 1-6 [default 6]
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %      This function will output a data dictionary containing all of the filenames for files that
    %      fall within your region of interest (under key: 'files') as well as the segment ids within 
    %      the associated files that fall within your region (under key:'segids')
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
    
    # This produces the path for the is2_fileselect script
    curpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    mf_name = curpath+'/SectorFiles_total.mat'
    sectors = loadmat(mf_name);
    
    ### Find which sector centers fall within the search poly
    buffer = 20000
    
    search_poly = np.array([[xbounds[0]-buffer,ybounds[0]-buffer],[xbounds[0]-buffer,ybounds[1]+buffer],[xbounds[1]+buffer,
        ybounds[1]+buffer],[xbounds[1]+buffer,ybounds[0]-buffer],[xbounds[0]-buffer,ybounds[0]-buffer]])
    
    search_poly_path = pltpath.Path(search_poly)
    inside = search_poly_path.contains_points(sectors['coord_centers'])
    inside_inds = np.nonzero(inside)[0]
    
    ### Loop through all contained sector_centers, and pull out the rgts/segids
    total_sector = np.empty((1))
    total_segids = np.empty((2))
    
    for i in range(0,len(inside_inds)):
        trgt = sectors['sector_rgt'][inside_inds[i]]
        trgt2= sectors['sector_segids'][inside_inds[i]]
        if np.max(trgt.shape) > 0:
            #print(i.shape)
            if np.max(trgt[0].shape) > 0:
                total_sector = np.r_[total_sector,trgt[0][0]]
                total_segids = np.c_[total_segids,trgt2[0]]

    total_sector = total_sector[1:]
    total_segids = total_segids[:,1:]
    
    ### Find the repeat RGTs, and select the appropriate min and max segid information
    unique_rgts = np.unique(total_sector)
    unique_segids = np.empty((2,0))
    for i in unique_rgts:
        check_inds = np.nonzero(total_sector == i)
        fill_in = np.array([[np.min(total_segids[0,check_inds])],[np.max(total_segids[1,check_inds])]]);
        unique_segids = np.c_[unique_segids,fill_in]
        
        
    outfiles = list();
    outsegids = list([]);
    outrgts = list();

    #pdb.set_trace()
    
    if ant_or_green == 0:
        region_nums = [10,11,12];
    elif ant_or_green == 1:
        region_nums = [3,4,5];
    
    ### Now we pull the filenames, and store the associated segids
    if filetype == 'ATL06':
        for i in range(0,len(unique_rgts)):
            for j in range(0,len(region_nums)):
                fstring = fdir+'*_%0.4d%0.2d%0.2d*.h5' % (unique_rgts[i],cycle,region_nums[j])
                files = glob.glob(fstring)
                if (len(files) > 0):
                    outfiles.extend(files[:])
                    outrgts.extend(np.ones(len(files))*unique_rgts[i].tolist())
                    outsegids.extend([unique_segids[:,i].tolist()]*len(files))
                if i % 10 == 0:
                    if print_flag == 1:
                        print('Finished rgt %d of %d' % (i, len(unique_rgts)))
            
    if filetype == 'ATL11':
        #fdir = '/data/rd08/projects/IS2/ATL11/'
        for i in range(0,len(unique_rgts)):
            for j in range(0,len(region_nums)):
                fstring = fdir+'ATL11_%0.4d%0.2d*.h5' % (unique_rgts[i],region_nums[j])
                files = glob.glob(fstring)
                if (len(files) > 0):
                    outfiles.extend(files[:])
                    outrgts.extend(np.ones(len(files))*unique_rgts[i].tolist())
                    outsegids.extend([unique_segids[:,i].tolist()]*len(files))
                if i % 10 == 0:
                    if print_flag == 1:
                        print('Finished rgt %d of %d' % (i, len(unique_rgts)))
                        
    ######### Here we filter files out based on whether or not they are the right region.
    region = np.array([[3,350000,446500],
              [4,446000,465000],
              [5,603000,623000],
              [10,1350000,1450000],
              [11,1440000,1570000],
              [12,1560000,1620000]])
    
    ki = []
    
    
    ############ This doesn't work because the bounds aren't as easy to define as above...
#   for ind,i in enumerate(outfiles):
#       if filetype == 'ATL11':
#           region_num = np.array(i[-17:-15],dtype='int')
#       elif filetype == 'ATL06':
#           region_num = np.array(i[-12:-10],dtype='int')
#           
#       row_ind = int(np.where(region_num == region[:,0])[0])
#       if np.any([np.all([outsegids[ind][0] > region[row_ind,0],outsegids[ind][1] < region[row_ind][2]]),
#                np.all([outsegids[ind][1] > region[row_ind,1],outsegids[ind][1] < region[row_ind][2]]),
#                np.all([outsegids[ind][0] < region[row_ind,1],outsegids[ind][1] > region[row_ind][2]])]):
#           ki.append(ind)

            
    ki = np.arange(0,len(outfiles))        
            
    outkeep = [outfiles[i] for i in ki]
    segkeep = [outsegids[i] for i in ki]
    rgtkeep = [outrgts[i] for i in ki]
        
    
    return {'files':outkeep, 'segids':segkeep, 'rgts':rgtkeep}
    
  