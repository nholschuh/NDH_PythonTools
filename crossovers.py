import numpy as np


def crossovers(line1,line2):

    import numpy.core.umath_tests as ut
    
    x_down = line1[:,0]
    y_down = line1[:,1]
    x_up = line2[:,0]
    y_up = line2[:,1]   
    
    p = np.column_stack((x_down, y_down))
    q = np.column_stack((x_up, y_up))

    (p0, p1, q0, q1) = p[:-1], p[1:], q[:-1], q[1:]
    rhs = q0 - p0[:, np.newaxis, :]

    mat = np.empty((len(p0), len(q0), 2, 2))
    mat[..., 0] = (p1 - p0)[:, np.newaxis]
    mat[..., 1] = q0 - q1
    mat_inv = -mat.copy()
    mat_inv[..., 0, 0] = mat[..., 1, 1]
    mat_inv[..., 1, 1] = mat[..., 0, 0]

    det = mat[..., 0, 0] * mat[..., 1, 1] - mat[..., 0, 1] * mat[..., 1, 0]
    mat_inv /= det[..., np.newaxis, np.newaxis] 


    params = ut.matrix_multiply(mat_inv, rhs[..., np.newaxis])
    intersection = np.all((params > 0.0001) & (params < 0.9999), axis=(-1, -2))  
    p0_s = params[intersection, 0, :] * mat[intersection, :, 0]          

    xover_point = p0_s + p0[np.where(intersection)[0]]

    return {'intersection_ind':[np.where(intersection)[0],np.where(intersection)[1]], 'intersection_points':xover_point}