
def find_cresisfiles_xy(ant0_or_gre1,point0_outline1_grid2,location_input,filename_or_aggregateddata=0,remove_totaldata=1,subset_by_outline=1):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    %     This function finds cresis data based on some geographic input
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     ant0_or_gre1 - Antarctica [0] or Greenland [1] domain
    %     point0_outline1_grid2 - This is a flag, set to 0, 1, or 2, depending on the
    %                             type of information you provide to 'location input'
    %                             for the datasearch
    %     location_input - pog=0: This should be a 3 value array, with a target x coordinate
    %                             target y coordinate, and radius to search in meters.
    %                      pog=1: This should be an nx2 array with vertices defining                             
    %                             a polygon that should be use to search within
    %                      pog=2: This had been implemented in matlab to let you find data
    %                             that fall within a gridded dataset. Until this is needed
    %                             again, it will probably remain un-implemented
    %                             
    %     filename_or_aggregateddata - [0] or 1, indicating whether you want just the files
    %                                  names or also the data
    %     remove_totaldata - this defines whether or not you want to get the radargrams as well
    %                        as coordinate information when collecting all the data. [1] excludes
    %                        the radargrams
    %     subset_by_outline - this will only return data that fall within your bounding box
    %                         defined by location_input, [1]
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %     a dictionary containing either the filenames of interest, or the filenames and data
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """    

    ################ This is the import statement required to reference scripts within the package
    import os,sys,glob
    ndh_tools_path_opts = [
        '/mnt/data01/Code/',
        '/home/common/HolschuhLab/Code/'
    ]
    for i in ndh_tools_path_opts:
        if os.path.isdir(i): sys.path.append(i); sector_root_dir=i;
    ################################################################################################
    
    import NDH_Tools as ndh
    import numpy as np

    
    if ant0_or_gre1 == 0:
        # These are made by the "Write_SectorFiles" script on the external drive. First you bulk aggregate, then write sectorfiles, 
        # then copy this into the Code folder
        sectors = ndh.loadmat(sector_root_dir+'/NDH_Tools/CReSIS_Sectors_forDataSearch_Ant.mat')
    else:
        sectors = ndh.loadmat(sector_root_dir+'/NDH_Tools/CReSIS_Sectors_forDataSearch_Gre.mat')

    ################### We load in the x_coords, y_coords, etc, from the file
    sector_x = sectors['sector_x']
    sector_y = sectors['sector_y']
    sector_spacing = sectors['sector_spacing']

    ################## We adjust for matlab indexing
    sector_inds = sectors['sector_inds']-1

    ############## Get array of sector centers
    xy_grid = np.array(np.meshgrid(sector_x, sector_y))
    xy_x = xy_grid[1,:,:].flatten()
    xy_y = xy_grid[0,:,:].flatten()
    xy = np.stack([xy_x,xy_y]).T

    if point0_outline1_grid2 == 0:

        ################### Individually find the closes x and y coordinate index
        cc_temp = ndh.find_nearest(sector_x, location_input[0])
        rr_temp = ndh.find_nearest(sector_y, location_input[1])
        cc = cc_temp['index']
        rr = rr_temp['index']

        ################### Provide a buffer (integer index value) around the target point
        buffer_if_point = np.floor(location_input[2] / sector_spacing)

        ol = np.array([[sector_x[cc] - sector_spacing * (1 + 2 * buffer_if_point) / 2, sector_y[rr] - sector_spacing * (1 + 2 * buffer_if_point) / 2],
                       [sector_x[cc] + sector_spacing * (1 + 2 * buffer_if_point) / 2, sector_y[rr] - sector_spacing * (1 + 2 * buffer_if_point) / 2],
                       [sector_x[cc] + sector_spacing * (1 + 2 * buffer_if_point) / 2, sector_y[rr] + sector_spacing * (1 + 2 * buffer_if_point) / 2],
                       [sector_x[cc] - sector_spacing * (1 + 2 * buffer_if_point) / 2, sector_y[rr] + sector_spacing * (1 + 2 * buffer_if_point) / 2],
                       [sector_x[cc] - sector_spacing * (1 + 2 * buffer_if_point) / 2, sector_y[rr] - sector_spacing * (1 + 2 * buffer_if_point) / 2]])

        ############# Define Bottom inds and top inds
        bi = int(max([rr - buffer_if_point, 0]))
        ti = int(min([rr + buffer_if_point, len(sector_inds)-1]))
        bi2 = int(max([cc - buffer_if_point, 0]))
        ti2 = int(min([cc + buffer_if_point, len(sector_inds[0])-1]))

        ############ Find the sectors within the ol box
        chosen_sectors = sector_inds[bi:ti+1, bi2:ti2+1]
        chosen_sectors = np.array(chosen_sectors.flatten())

    elif point0_outline1_grid2 == 1:
        ol = location_input
        sector_list = sector_list.flatten()
        found_sectors = ndh.within(xy,ol)
        chosen_sectors = np.array(sector_list[found_sectors])

    elif point0_outline1_grid2 == 2:
        if 0:
            dx = location_input[0][1] - location_input[0][0]
            dy = location_input[1][1] - location_input[1][0]
            gx = [location_input[0][0] - dx] + location_input[0] + [location_input[0][-1] + dx]
            gy = [location_input[1][0] - dy] + location_input[1] + [location_input[1][-1] + dy]
            nm = np.zeros([len(location_input[2]) + 2])
            nm[1:-1, 1:-1] = location_input[2]
            new_mask = regrid(gx, gy, nm, sector_x, sector_y, 'nearest')
    
            chosen_sectors = np.array(sector_inds[np.where(new_mask == 1)])
            ol = [gx, gy, nm]
        else:
            print('point0_outline1_grid2=2 has no been implemented yet. Work through that now!')


    target_files = []
    sector_target = np.array(ndh.flatten_list(sectors['sector_files'][chosen_sectors]))
    sector_target = np.unique(sector_target)
    for file_ind in sector_target:
        file_ind = file_ind-1
        fci = sectors['filename'][file_ind][0][::-1]
        try:
            temp_filesearch = ndh.find_cresisfiles(fci[0],fci[1],fci[2],fci[3],fci[4])
            target_files.append(temp_filesearch['standard'][0])
        except:
            print('Something seems to be wrong with ',str(file_ind))
            #return {'filenames':[]}

    target_files = np.unique(target_files)

    if filename_or_aggregateddata == 0:
        return {'filenames':target_files}
    else:
        if subset_by_outline == 0:
            aggregated_data = ndh.cresis_dataaggregator(target_files,remove_totaldata,'',0)
        else:
            aggregated_data = ndh.cresis_dataaggregator(target_files,remove_totaldata,'',0,ol[:,:,0],1)
            
        return aggregated_data

    
