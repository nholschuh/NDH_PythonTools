import numpy as np

def parse_srun(fn,debug_flag=0):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    %     This function will parse the results of the inverse model statistics
    %     from icepack
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     fn -- .out filename to parse
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %     stats: the statistics of the optimization problem
    %     meta: metadata about the performance of the inverse solver
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """     

    with open(fn) as f:
        lines = f.readlines() # list containing lines of file

        i = 1
        columns1 = [];
        columns2 = [];
        temp_data2 = [];
        debug_list = []

        for ind0,line in enumerate(lines):
            line = line.strip() # remove leading/trailing white spaces
            if debug_flag == 2:
                print(ind0,'-',line)

            ############################ Here, we pull out the values from X
            if ind0 == 30:
                columns1 = [item.strip() for item in line.split()]
            elif ind0>46:
                temp_data = [item.strip() for item in line.split()]
                if len(temp_data) == len(columns1):

                    if 'data1' not in locals():
                        data1 = np.expand_dims(np.array(temp_data).astype(float),1).T
                    else:
                        data1 = np.concatenate([data1,np.expand_dims(np.array(temp_data).astype(float),0)],axis=0)


            if ind0 > 32:
                temp_columns = [item.strip() for item in line.split(':')]
                if len(temp_columns) == 2:
                    if temp_columns[0][0:5] != 'Inter':
                        if ind0 < 46:
                            columns2.append(temp_columns[0])
                        temp_data2.append(temp_columns[1])

            if len(temp_data2) == 12:
                if 'data2' not in locals():
                    data2 = np.expand_dims(np.array(temp_data2).astype(float),1).T
                else:
                    data2 = np.concatenate([data2,np.expand_dims(np.array(temp_data2).astype(float),0)],axis=0)
                debug_list.append([ind0,temp_columns[0]])
                temp_data2 = [];

            if debug_flag == 1:
                if ind0> 141:
                    if ind0 < 157:
                        print(line)
                        print(temp_columns)
                        print(temp_data2)
                        pass

    stats = {'values': data1,'headers':columns1}
    meta = {'values': data2,'headers':columns2}
    
    return stats,meta