
def rotation(input_vec,rotation_angle,dims=2,axis=0):

    import numpy as np

    if dims == 2:
        if axis == 0:
            ########## A rotation around x
            rotation = np.array([[np.cos(rotation_angle),-np.sin(rotation_angle)],[np.sin(rotation_angle),np.cos(rotation_angle)]])
        
    if dims == 3:
        if axis == 0:
            ########## A rotation around x
            rotation = np.array([[1,0,0],[0,np.cos(ref_axial_tilt),-np.sin(ref_axial_tilt)],[0,np.sin(ref_axial_tilt),np.cos(ref_axial_tilt)]])
        
        if axis == 1:
            ########## A rotation around y
            rotation = np.array([[np.cos(ref_axial_tilt),0,np.sin(ref_axial_tilt)],[0,1,0],[-np.sin(ref_axial_tilt),0,np.cos(ref_axial_tilt)]])
        
        if axis == 2:
            ########## A rotation around z
            rotation = np.array([[np.cos(ref_axial_tilt),-np.sin(ref_axial_tilt),0],[np.sin(ref_axial_tilt),np.cos(ref_axial_tilt),0],[0,0,1]])

    input_vec_rotated = np.matmul(input_vec,rotation)
    return input_vec_rotated