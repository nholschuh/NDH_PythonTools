import numpy as np

def fresnel_reflection_coefficient(perm1, perm2, incident_angle_deg=0, return_type='power'):
    """
    Compute Fresnel reflection and transmission coefficients
    for H- and V-polarized light at the boundary between two media.

    Conventions:
        - H (Horizontal): E-field perpendicular to the plane of incidence (s-pol)
        - V (Vertical):   E-field in the plane of incidence (p-pol)

    Parameters:
        perm1 (float): Relative permittivity of medium 1 (incident medium)
        perm2 (float): Relative permittivity of medium 2 (transmission medium)
        incident_angle_deg (float): Angle of incidence in degrees
        return_type (str): 'power' (default) or 'amplitude'

    Returns:
        dict: Reflection and transmission for H and V polarizations
              in either amplitude or power depending on return_type
    """
    assert return_type in ('power', 'amplitude'), "return_type must be 'power' or 'amplitude'"
    
    # Convert angle to radians
    theta_i = np.radians(incident_angle_deg)
    
    # Refractive indices
    n1 = np.sqrt(perm1)
    n2 = np.sqrt(perm2)
    
    # Snell's Law
    sin_theta_t = n1 / n2 * np.sin(theta_i)
    
    # Total Internal Reflection
    if np.abs(sin_theta_t) > 1.0:
        base = 1.0 if return_type == 'power' else 1.0
        return {
            "R_H": base,
            "R_V": base,
            "T_H": 0.0,
            "T_V": 0.0,
            "total_internal_reflection": True
        }
    
    theta_t = np.arcsin(sin_theta_t)
    
    # H-polarization (s)
    r_H = (n1 * np.cos(theta_i) - n2 * np.cos(theta_t)) / \
          (n1 * np.cos(theta_i) + n2 * np.cos(theta_t))
    t_H = 2 * n1 * np.cos(theta_i) / \
          (n1 * np.cos(theta_i) + n2 * np.cos(theta_t))
    
    # V-polarization (p)
    r_V = (n2 * np.cos(theta_i) - n1 * np.cos(theta_t)) / \
          (n2 * np.cos(theta_i) + n1 * np.cos(theta_t))
    t_V = 2 * n1 * np.cos(theta_i) / \
          (n2 * np.cos(theta_i) + n1 * np.cos(theta_t))

    if return_type == 'amplitude':
        return {
            "R_H": r_H,
            "R_V": r_V,
            "T_H": t_H,
            "T_V": t_V,
            "total_internal_reflection": False
        }
    else:
        return {
            "R_H": np.abs(r_H)**2,
            "R_V": np.abs(r_V)**2,
            "T_H": np.abs(t_H)**2 * (n2 * np.cos(theta_t)) / (n1 * np.cos(theta_i)),
            "T_V": np.abs(t_V)**2 * (n2 * np.cos(theta_t)) / (n1 * np.cos(theta_i)),
            "total_internal_reflection": False
        }