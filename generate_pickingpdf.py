################ This is the import statement required to reference scripts within the package
import os,sys,glob
ndh_tools_path_opts = [
    '/mnt/data01/Code/',
    '/home/common/HolschuhLab/Code/'
]
for i in ndh_tools_path_opts:
    if os.path.isfile(i): sys.path.append(i)
################################################################################################


def generate_pickingpdf(fn,picking_root_dir,frame_spacing=25,surf_dir='CSARP_surf_ndh',crop_type='100',clims=[], alternative_data_opt=0):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    %     This function does the standard load, transformation, and plotting
    %     that is common in the CReSIS radar analysis workflow
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """ 
    
    import NDH_Tools as ndh
    import matplotlib.pyplot as plt
    import numpy as np

    
    ######### Set-up the directory where picks are placed
    if not os.path.isdir(picking_root_dir+'To_Pick'):
        os.makedirs(picking_root_dir+'To_Pick') 
            
    #######################################################################################################
    ####################### We need to determine if this is a 2D file or a MUSIC File
    str_opt, str_ind = ndh.str_compare([fn],'music')
    if len(str_opt) > 0:
        
        seg = fn.split('/')[-2]
        frame = fn.split('/')[-1].split('.')[0]
        if picking_root_dir[-1] != '/':
            picking_root_dir = picking_root_dir+'/'

        ################ Here we do some directory checking to make sure all folders we need exist
        if not os.path.isdir(picking_root_dir+'To_Pick/'+seg):
            os.makedirs(picking_root_dir+'To_Pick/'+seg)     ### The pdf directory where pickfiles are stored 

        if not os.path.isdir(picking_root_dir+seg):
            os.makedirs(picking_root_dir+seg)                ### The directory for the segment

        if not os.path.isdir(picking_root_dir+seg+'/'+frame):
            os.makedirs(picking_root_dir+seg+'/'+frame)      ### The subdirectory for the frame


        ########### Now the data anlysis begins
        data = ndh.loadmat(fn)
        xy = ndh.polarstereo_fwd(data['Latitude'],data['Longitude'])
        distance = ndh.distance_vector(xy['x'],xy['y'])
    
        
        fig = plt.figure(figsize=(5,10))
        ax = plt.gca()
        
        #### Here we test to see if there are existing surface picks
        fn_list = fn.split('/')
        fn_list[-3] = surf_dir
        fn2 = '/'.join(fn_list)
        
        try:
            surfdata = ndh.loadmat(fn2)
            surf_dims = surfdata['surf']['y'][1].shape
            bot_ind = ndh.find_nearest(data['Time'],np.max(surfdata['surf']['y'][1]))
        except:
            print(fn2+' could not be found')
            fn2 = 0
            bot_ind = {'index':[len(data['Time'])-25]}

        #### Now we loop through the frames we want to plot and generate an image for
        frame_print = np.arange(0,len(xy['x']),frame_spacing)
        for ind1,i in enumerate(frame_print):
            ndh.remove_image(ax,1,verbose=0)
            ax.imshow(np.squeeze(np.log10(data['Tomo']['img'][:bot_ind['index'][0]+25,:,i])),cmap='bone_r')
            ax.set_aspect('auto')
            if fn2 != 0:
                ndh.remove_line(ax,1,verbose=0)
                #### Here we identify the indecies associated with the bottom picks and add them to the image
                bot_inds = ndh.find_nearest(data['Time'],surfdata['surf']['y'][1][:,i])
                plt.plot(np.arange(0,surf_dims[0],4),bot_inds['index'][::4],ls='none',marker='^',c='green',ms=4,alpha=0.1)
            else:
                pass

            plt.axis('off')
            plt.savefig('%s%s/%s/Frame_%0.4d_fs_%0.2d_crop_%0.4d.png' %(picking_root_dir,seg,frame,i,frame_spacing,bot_ind['index'][0]+25))


        print('Completed the image generation')
        
        ########## Website used to do the following:
        # https://stackoverflow.com/questions/9710118/convert-multipage-pdf-to-png-and-back-linux

        ########## This converts all the images to a single pdf
        pdfroot = picking_root_dir+'To_Pick/'+seg+'/'
        pdfend = '%s_fs_%0.2d_crop_%0.4d.pdf' %(frame,frame_spacing,bot_ind['index'][0]+25)
        pdfname=pdfroot+pdfend

        frames = '%s%s/%s/*.png' % (picking_root_dir,seg,frame)

        os.system("convert -adjoin "+frames+" -gravity center -scale '90<x770<' "+pdfname)
        ###########

        os.system('rm -r '+picking_root_dir+seg)
        
#################################################################################################################### 
#################################################################################################################### 
#################################################################################################################### 
####################################################################################################################  
####################################################################################################################        
    #######################################################################################################
    ####################### The alternative is a directory full of standard files
    str_opt, str_ind = ndh.str_compare([fn],'standard')
    if len(str_opt) > 0:    
        
        file_list = sorted(glob.glob(fn+'/Data_*.mat'))
        
        if len(file_list) > 0:
            ki = [];
            for ind,i in enumerate(file_list):
                if i.split('/')[-1][5] != 'i':
                    ki.append(ind)
            file_list = ndh.index_list(file_list,ki)
        else:
            file_list = sorted(glob.glob(fn+'/*.mat'))

            
        try:
            max_num = int(file_list[-1].split('/')[-1].split('.')[0].split('_')[-1])
            seg = file_list[-1].split('/')[-2]
            froot = '_'.join(file_list[-1].split('/')[-1].split('.')[0].split('_')[0:-1])
        except:
            max_num = len(file_list)
            seg = file_list[-1].split('/')[-2]
            froot = seg
        num_range = np.arange(1,max_num+1,1)

        

        ################ Here we do some directory checking to make sure all folders we need exist
        if not os.path.isdir(picking_root_dir+'To_Pick/'+seg):
            os.makedirs(picking_root_dir+'To_Pick/'+seg)     ### The pdf directory where pickfiles are stored 

        fig = plt.figure(figsize=(15,7))
        ax = plt.gca()  

        for ind1,file_num in enumerate(num_range):
            
            fn_frame = '%s/%s_%0.3d.mat' % (fn,froot,file_num)
            print(fn_frame)
            if os.path.isfile(fn_frame) == 0:
                fn_frame = file_list[ind1]

            radar_data,depth_data = ndh.radar_load(fn_frame,plot_flag=0,elevation1_or_depth2=0)

            if len(radar_data.keys()) > 0:
                bot_inds = ndh.find_nearest(radar_data['Time'],radar_data['Bottom'])['index'].astype(float)
                surf_inds = ndh.find_nearest(radar_data['Time'],radar_data['Surface'])['index'].astype(float)        
                bot_inds[bot_inds == 0] = np.NaN
                surf_inds[surf_inds == 0] = np.NaN


                if crop_type == '100':
                    bot_ind = np.nanmax(bot_inds)+100
                    crop_string = 'maxbotplus100'
                else:
                    bot_ind = len(radar_data['Time'])
                    crop_string = 'nocrop'
                    
                ndh.remove_image(ax,1,verbose=0)
                ndh.remove_line(ax,2,verbose=0)

                if np.isnan(bot_ind) == 1:
                    plt.plot(0,0)
                else:
                    ########### This accomodates files that have more than one data type
                    if alternative_data_opt == 1:
                        find_data_opts = ndh.str_compare(radar_data.keys,'Data2')
                        if len(find_data_opts[0]) > 0:
                            radar_data['Data'] = radar_data['Data2']

                    if len(clims) > 0:
                        imdata = plt.imshow(10*np.log10(radar_data['Data'][:int(bot_ind),:]),
                                            origin='lower',aspect='auto',cmap='gray_r',vmin=clims[0],vmax=clims[1])
                    else:
                        imdata = plt.imshow(10*np.log10(radar_data['Data'][:int(bot_ind),:]),
                                            origin='lower',aspect='auto',cmap='gray_r')                

                    plt.plot(np.arange(0,len(radar_data['distance'])),bot_inds,ls='--',c='green',alpha=0.2)
                    plt.plot(np.arange(0,len(radar_data['distance'])),surf_inds,ls='--',c='green',alpha=0.2)
                
            else:
                plt.plot(0,0)


            ax.invert_yaxis()

            plt.axis('off')
            frame_fn = '%s/To_Pick/%s/Frame_%0.3d.png' %(picking_root_dir,seg,file_num)
            plt.savefig(frame_fn)
            print('  --- Completed Image '+str(ind1)+' of '+str(len(num_range)))

        print('Completed the image generation')

        ########## Website used to do the following:
        # https://stackoverflow.com/questions/9710118/convert-multipage-pdf-to-png-and-back-linux

        ########## This converts all the images to a single pdf
        pdfroot = picking_root_dir+'To_Pick/'
        pdfend = 'StandardPicks_%s_crop_%s.pdf' %(seg,crop_string)
        pdfname=pdfroot+pdfend

        frames = '%s/To_Pick/%s/*.png' % (picking_root_dir,seg)

        os.system("convert -adjoin "+frames+" -gravity center -scale '90<x770<' "+pdfname)
        ###########

        if 0:
            os.system('rm -r '+picking_root_dir+'/To_Pick/'+seg)
            os.system('rmdir '+picking_root_dir+'/To_Pick/'+seg)
        else:
            print('rm -r '+picking_root_dir+'/To_Pick/'+seg)
            print('rmdir '+picking_root_dir+'/To_Pick/'+seg)           