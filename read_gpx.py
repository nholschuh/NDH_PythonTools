import numpy as np

def read_gpx(fn):
    """
    % (C) Nick Holschuh - Amherst College - 2022 (Nick.Holschuh@gmail.com)
    % This function write a gpx waypoint file or route file
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %    fn -- 
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    %    data_dictionary
    % 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
    fid = open(fn)
    line = fid.readline()
    file_strings = [line]

    while len(line) > 0:
        line = fid.readline()
        file_strings.append(line)

    file_string = ''
    for i in file_strings:
        file_string = file_string+i


    gpx_data1 = file_string.split('</wpt>')
    if len(gpx_data1[0]) != len(file_string):
        waypoints_flag = 1
        gpx_data = gpx_data1
        print('Waypoints')
        #print(len(gpx_data),len(file_string))

    gpx_data2 = file_string.split('</rtept>')
    if len(gpx_data2[0]) != len(file_string):
        waypoints_flag = 0
        gpx_data = gpx_data2
        #print('Route')

    gpx_data3 = file_string.split('</trkpt>')
    if len(gpx_data3[0]) != len(file_string):
        waypoints_flag = -1
        gpx_data = gpx_data3
        #print('Track')

    lats = []
    lons = []
    names = []
    counter = 0;
    for ind0,line in enumerate(gpx_data):
        if waypoints_flag == 1:
            line_parts1 = line.split('wpt')
        elif waypoints_flag == 0:
            line_parts1 = line.split('rtept')
        else:
            line_parts1 = line.split('trkpt')

        if len(line_parts1) > 1:
            line_parts = line_parts1[1].split('\"')

            if len(line_parts) > 3:
                if 'lat' in line:
                    lats.append(float(line_parts[1]))
                    lons.append(float(line_parts[3]))

                    if waypoints_flag >= 0:
                        names.append(line_parts[4].split('<name>')[1].split('</name>')[0])
                    else:
                        names.append('Track_%0.4d' % counter)
                    counter = counter+1;

    #close(fid)

    gpx_results = {'lat':lats,'lon':lons,'names':names,'waypoints_flag':waypoints_flag}
    return gpx_results