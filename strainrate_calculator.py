def strainrate_calculator(x_axis,y_axis,u,v,strain_selections=[1,1,1,1,1,0,1],debug_flag=0):
    '''
    % (C) Nick Holschuh - Penn State University - 2016 (Nick.Holschuh@gmail.com)
    % This calculates the maximum longitudinal strain ("along flow"), the
    % minimum longitudinal strain ("across flow"), and the maximum shear, using
    % properties of the eigenvectors and eigenvalues of DV tensor. This
    % solution is presented in (Hackl et al. 2009), although it is foundational
    % theory in continuum mechanics.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    % x_axis - The xaxis values that are associated with the velocity grids
    % y_axis - The yaxis values that are associated with the velocity grids
    % u - The velocity component in the orientation of the x axis
    % v - The velocity component in the orientation of the y axis
    % strain_selections - This input allows you to select which of the output
    %   products you would like to retain. It should be a matrix with 0s and 1s
    %   in the following positions, to indicate which values you are most
    %   interested in.
    %%%%%%%
    % 1 - Max Longitudinal Strain Rate
    % 2 - Min Longitudinal Strain Rate
    % 3 - Max Shear Strain Rate
    % 4 - Max Longitudinal Orientation
    % 5 - Min Longitudinal Orientation
    % 6 - Rotation Matrix
    % 7 - Vertical Strain Rate (assuming incompressibility)
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The Output is as follows:
    % sr - a Cell array, containing 6 entries.
    % 1 - The principle longitudinal strain rate (scaler)
    % 2 - The secondary longitudinal strian rate (scaler)
    % 3 - The maximum shear strain rate (scaler)
    % 4 - The orientation of maximum longitudinal strain (vector)
    % 5 - The orientation of minimum longitudinal strain (vector)
    % 6 - The rotation matrix (matrix, with positions corresponding to:
    %        [  1   2;
    %           3   4  ]
    % 7 - The vertical strain rate value
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%
    '''
    
    import numpy as np
    
    ##################################################################
    ##################################### Variable Initialization
    while len(strain_selections) < 7:
        strain_selections.append(0)

    # Initialize the principle eigenvector matrix (1), if desired
    if strain_selections[0] == 1:
        e1 = np.zeros(u.shape + (1,))
    else:
        e1 = 0
        
    # Initialize the principle eigenvector matrix (2), if desired
    if strain_selections[1] == 1:
        e2 = np.zeros(u.shape + (1,))
    else:
        e2 = 0

    # Initialize the principle eigenvector matrix (3), if desired
    if strain_selections[2] == 1:
        ss = np.zeros(u.shape + (1,))
    else:
        ss = 0

    # Initialize the principle eigenvector matrix (4), if desired
    if strain_selections[3] == 1:
        ev1 = np.zeros(u.shape + (2,))
    else:
        ev1 = 0

    # Initialize the secondary eigenvector matrix (5), if desired
    if strain_selections[4] == 1:
        ev2 = np.zeros(u.shape + (2,))
    else:
        ev2 = 0

    # Initialize the rotation matrix (6), if desired
    if strain_selections[5] == 1:
        rm = np.zeros(u.shape + (4,))
    else:
        rm = 0

    # Initialize the vertical strain rate matrix (7), if desired
    if strain_selections[6] == 1:
        vs = np.zeros(u.shape + (1,))
    else:
        vs = 0
    ##################################################################

    # Generate the change in velocity components
    du_y, du_x = np.gradient(u)
    dv_y, dv_x = np.gradient(v)

    dx = x_axis[1] - x_axis[0]
    dy = y_axis[1] - y_axis[0]

    dudx = du_x / dx
    dudy = du_y / dy
    dvdx = dv_x / dx
    dvdy = dv_y / dy

    # Fill in the components of the strain rate tensor
    shear1 = 0.5 * (dudy + dvdx)
    rotation1 = 0.5 * (dudy - dvdx)
    rotation2 = 0.5 * (dvdx - dudy)

    zeromat = np.zeros_like(shear1)

    # Initialize arrays to store results
    e1 = np.zeros_like(zeromat)
    e2 = np.zeros_like(zeromat)
    ss = np.zeros_like(zeromat)
    ev1 = np.zeros((len(zeromat), len(zeromat[0]), 2))
    ev2 = np.zeros((len(zeromat), len(zeromat[0]), 2))
    rm = np.zeros((len(zeromat), len(zeromat[0]), 4))
    vs = np.zeros_like(zeromat)

    for i in range(len(zeromat)):
        for j in range(len(zeromat[0])):
            # Compute eigenvalues and eigenvectors
            calc_mat = [[dudx[i, j], 0.5 * (dudy[i, j] + dvdx[i, j])],
                                               [0.5 * (dudy[i, j] + dvdx[i, j]), dvdy[i, j]]]
            
            #print(calc_mat)
            if strain_selections[3] == 1 or strain_selections[4] == 1:      
                e_val, e_vec = np.linalg.eig(calc_mat)
            else:
                e_val = np.linalg.eigvals([[dudx[i, j], 0.5 * (dudy[i, j] + dvdx[i, j])],
                                            [0.5 * (dudy[i, j] + dvdx[i, j]), dvdy[i, j]]])
            
            #print(e_val)
            #print('-----------------')

            # Store results based on strain_selections
            if strain_selections[0] == 1:
                e1[i, j] = e_val[0]
            if strain_selections[1] == 1:
                e2[i, j] = e_val[1]
            if strain_selections[2] == 1:
                ss[i, j] = (np.max(e_val) - np.min(e_val)) / 2
            if strain_selections[3] == 1:
                ev1[i, j] = e_vec[:, 0]
            if strain_selections[4] == 1:
                ev2[i, j] = e_vec[:, 1]
            if strain_selections[5] == 1:
                rm[i, j] = [0, rotation1[i, j], rotation2[i, j], 0]
            if strain_selections[6] == 1:
                vs[i, j] = -e_val[0] - e_val[1]

    # Debugging
    if debug_flag == 1:
        test_vs = -dudx - dudy
        import matplotlib.pyplot as plt
        plt.imshow(vs - test_vs)
        plt.clim(-0.01, 0.01)
        plt.colorbar()

    # Store results
    sr = [e1, e2, ss, ev1, ev2, rm, vs]
    sr_meta = ['Max Longitudinal Strain Rate',
               'Min Longitudinal Strain Rate',
               'Max Shear Strain Rate',
               'Max Longitudinal Orientation',
               'Min Longitudinal Orientation',
               'Rotation Matrix',
               'Vertical Strain Rate']
    newx = (x[1:]+x[:-1])/2
    newwy = (x[1:]+x[:-1])/2
    
    return sr,newx,newy,sr_meta