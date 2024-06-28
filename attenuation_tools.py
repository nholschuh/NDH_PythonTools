import xarray as xr
import numpy as np
from scipy.special import erf, lambertw

################################## This includes a set of useful thermal models
################################## and conversion functions for attenuation rates

######################### Functions for calculating temperature or possible
######################### temperate ice thickness
# thermal_model
# meyer_temperateice

######################### Functions for getting the conductivity and associated attenuation
# IceConductivity
# attenuation_from_cond

######################### Getting the temperature from conductivity for pure ice, or 
######################### calculating the loss tangent
# PureIce_Temperature
# loss_tangent


###################################### Constants required for multiple functions
cice=1.68e8
cair=2.998e8
e_0 = 8.85418782e-12  # F/m (farads per meter)
e_prime = (cair / cice) ** 2

k = 8.6173324e-5  # eV/K - Boltzmann constant
spy = 3.154e+7  # seconds per year
rho_ice = 917  # kg/m^3
R = 8.314  # J/(mol*K)


####################################################################################
####################################################################################
################################

def thermal_model(z, T_atm, a=0.03, shear=0, geotherm=0.05, mode_flag=1):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %      This includes both an analytical and approximate model
    %      for the glacier temperature profile
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %      thickness - The ice thickness to calculate for
    %      T_atm - Atmospheric Temperature (K)
    %      a - Accumulation Rate
    %      shear - shear strain rate
    %      geotherm - W/m^2
    %      mode_flag - 1= Analytical solution from cuffey and patterson
    %                  2= 1-d numerical solution from Perol + Rice
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %      dictionary containing
    %          T - Temperature (in K) as a function of
    %          z - Depth (in m)
    %          melt-flag - 0 or 1, indicating if the bed is melting
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Note -- both of these models have issues. The analyitcal 
    """    
    meltflag = 0
    dz = 5

    if hasattr(z, '__iter__') == 0:
        z = np.arange(0,z,dz)

    thickness = np.max(z)
    P = rho_ice * 9.8 * thickness  # Pressure
    T_melt = 273.16 - 7.42e-8 * P  # Pressure Melting Point

    # Values from Cuffey and Patterson
    T_avg = (T_atm + T_melt) / 2
    C = 152.5 + 7.122 * T_avg  # Specific Heat Capacity
    K = 9.828 * np.exp(-5.7e-3 * T_avg)  # Thermal Conductivity
    alpha_t = K/(rho_ice*C)*spy # Thermal Diffusivity
    Pe = a * thickness * rho_ice * C / (K * spy)  # Peclet Number
    
    if Pe <= 0:
        Pe = 0.00001

    if mode_flag == 1:
        # Analytical solution to temperature profile from Cuffey and
        # Patterson (411), just solving for basal temperature
        gamma = a*thickness/alpha_t
        z_star = np.sqrt(2*alpha_t*thickness/a)

        T = -z_star*np.sqrt(np.pi)/2*geotherm/K*(erf(z/z_star)-erf(thickness/z_star)) + T_atm
        
        #theta_b = np.sqrt(np.pi / (2 * Pe)) * np.sqrt(erf(Pe / 2))
        #T = theta_b * geotherm * z / K + T_atm

        if np.max(T) > T_melt:
            meltflag=1
            T[T > T_melt] = T_melt;

    elif mode_flag == 2:
        # 1-D thermal solution (Perol, Rice, Platt, and Suckale - 2015)
        dlamda = 0.01
        lamda = np.arange(dlamda / 2, 1, dlamda)

        T_h = T_avg + (273.15 - T_melt)
        A_star = 3.5e-25
        
        if T_h < 263:
            Q = 60000
        else:
            Q = 115000

        A = A_star * np.exp((-Q / R) * ((1 / (T_avg + 7e-8 * P)) - (1 / T_h)))
        tg_prod = (2 * A**(-1/3)) * (shear / (2 * spy))**(4/3)

        T = np.zeros(len(z))
        T_noshear = np.zeros(len(z))
        for i in range(len(z)):
            diffusion_advection_scaler = erf(np.sqrt(Pe / 2) * (z[i] / thickness)) / erf(np.sqrt(Pe / 2))
            T_noshear[i] = T_melt + (T_atm - T_melt) * diffusion_advection_scaler

            scaler1 = np.sum((1 - np.exp(-lamda * Pe * z[i]**2 / (2 * thickness**2))) / (2 * lamda * np.sqrt(1 - lamda))) * dlamda 
            scaler2 = np.sum((1 - np.exp(-lamda * Pe / 2)) / (2 * lamda * np.sqrt(1 - lamda))) * dlamda 

            T[i] = T_melt + (T_atm - T_melt) * erf(np.sqrt(Pe / 2) * (z[i] / thickness)) / erf(np.sqrt(Pe / 2)) - \
                   tg_prod * thickness**2 / (K * Pe) * (scaler1 - erf(np.sqrt(Pe / 2) * (z[i] / thickness)) / erf(np.sqrt(Pe / 2)) * scaler2)

            if T[i] >= T_melt:
                T[i] = T_melt
                meltflag = 1

    return {'T':T[::-1], 'z':z, 'meltflag':meltflag}


####################################################################################
####################################################################################
################################


def meyer_temperateice(thickness, strainrate, Tsurf, accumulation=None):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Meyer, C. R., & Minchew, B. M. (2018).
    % Temperate ice in the shear margins of the Antarctic Ice Sheet: Controlling processes and preliminary locations.
    % Earth and Planetary Science Letters, 498, 17–26.
    % https://doi.org/10.1016/j.epsl.2018.06.028
    """ 
    if accumulation is None:
        diffusion0_or_advectiondiffusion1 = 0
    else:
        diffusion0_or_advectiondiffusion1 = 1

    strainrate = strainrate / 3.154e+7  # convert to per/seconds
    if accumulation is not None:
        accumulation = accumulation / 3.154e+7  # convert to m/s

    A = 2.4e-24
    cp = 2050
    Tm = 273.25
    K = 2.1
    n = 3

    Br = 2 * thickness**2 / (K * (Tm - Tsurf)) * (strainrate**(n + 1) / A)**(1 / n)
    Br[Br < 0.01] = 0.01

    if diffusion0_or_advectiondiffusion1 == 0:
        crit_strainrate = (K * (Tm - Tsurf) / (A**(-1 / n) * thickness**2))**(n / (n + 1))
    else:
        pe = rho_ice * cp * accumulation * thickness / K
        lamda = 0
        exp_value = -np.exp(-((pe**2) / (Br - lamda)) - 1)

        # Efficient calculation of lambertw using pre-computed values
        mean_exp_value = np.mean(exp_value)
        std_exp_value = np.std(exp_value)

        min_opt = mean_exp_value - 3 * std_exp_value
        opts = np.linspace(min_opt, 0, 10000)
        dopt = opts[1] - opts[0]

        exp_value[exp_value < min_opt] = min_opt
        exp_value_ind = np.ceil((exp_value - min_opt) / dopt).astype(int)
        exp_value_ind[exp_value_ind == 0] = 1

        lambertw_translate = lambertw(opts).real

        exp_value = lambertw_translate[exp_value_ind]

        crit_strainrate = 1 - (pe / (Br - lamda)) - (1 / pe) * (1 + exp_value)

    inds = np.where(strainrate < crit_strainrate)

    temperate_thickness = (1 - np.sqrt(2 / Br)) * thickness
    temperate_thickness[inds] = 0

    return temperate_thickness

####################################################################################
####################################################################################
################################


def IceConductivity(temp_k, H, Cl, NH4, parameterset=0, frequency=0, param_override=None):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % Calculate the loss tangent and conductivity based on the given method.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    

    Compute attenuation rates from temperature and impurity values based on various models.

    Parameters:
    temp_k: float
        Temperature in Kelvin (273.15 = 0C)
    H: float
        Hydrogen Ion Concentration (microMol/L)
    Cl: float
        Sea-salt Chlorine Ion Concentration (microMol/L)
    NH4: float
        Ammonium Chlorine Ion Concentration (microMol/L)
    parameterset: int, optional
        Choice of conductivity model (default is 0):
        0 - Gudmensen, only T, Greenland
        1 - MacGregor 2007 (Siple Dome)
        2 - MacGregor 2015 (Greenland)
        3 - Wolff 1997 (can accommodate F dependence)
    frequency: float, optional
        Frequency of the instrument if parameterset = 3. Otherwise, leave blank (default is 0).
    param_override: dict, optional
        Dictionary to override specific parameter values (e.g., {'T_ref': 251, 'mu_h': 3.2}).

    Returns:
    sigma: float
        Total Conductivity of the Ice.
    sigma_components: numpy array
        Each of the components of conductivity [Total, Pure Ice, H+, Cl, NH4].
    """
    
    # Define constants
    e_0 = 8.85418782e-12  # F/m (farads per meter)
    
    # Parameter sets
    if parameterset == 0:
        # Gudmensen 1971
        sig_0 = 15.4  # microS/m
        E0 = 0.33  # eV
        T_ref = 251
        mu_h, EH, mu_Cl, E_Cl, mu_NH4, E_NH4 = [0] * 6
    elif parameterset == 1:
        # MacGregor et al 07
        sig_0 = 7.2
        E0 = 0.55
        T_ref = 273.15 - 21
        mu_h, EH = 3.2, 0.20
        mu_Cl, E_Cl = 0.43, 0.19
        mu_NH4, E_NH4 = 0.8, 0.23
    elif parameterset == 2:
        # MacGregor et al 15
        sig_0 = 9.2
        E0 = 0.51
        T_ref = 273.15 - 21
        mu_h, EH = 3.2, 0.21
        mu_Cl, E_Cl = 0.43, 0.19
        mu_NH4, E_NH4 = 0.8, 0.23
    elif parameterset == 3:
        # Wolff et al 97
        sig_0 = 9
        E0 = 0.58
        T_ref = 273.15 - 15
        mu_h, EH = 4, 0.21
        mu_Cl, E_Cl = 0.55, 0.23
        mu_NH4, E_NH4 = 1, 0.23

    # Override parameters if specified
    if param_override:
        for key, value in param_override.items():
            if key == 'sig_0': sig_0 = value
            elif key == 'E0': E0 = value
            elif key == 'T_ref': T_ref = value
            elif key == 'mu_h': mu_h = value
            elif key == 'EH': EH = value
            elif key == 'mu_Cl': mu_Cl = value
            elif key == 'E_Cl': E_Cl = value
            elif key == 'mu_NH4': mu_NH4 = value
            elif key == 'E_NH4': E_NH4 = value

    # Compute conductivities
    pure_sig = (sig_0 * np.exp((E0 / k) * ((1 / T_ref) - (1 / temp_k)))) / 1e6
    H_sig = (mu_h * H * np.exp((EH / k) * ((1 / T_ref) - (1 / temp_k)))) / 1e6
    Cl_sig = (mu_Cl * Cl * np.exp((E_Cl / k) * ((1 / T_ref) - (1 / temp_k)))) / 1e6
    NH4_sig = (mu_NH4 * NH4 * np.exp((E_NH4 / k) * ((1 / T_ref) - (1 / temp_k)))) / 1e6

    if parameterset != 3 or frequency == 0:
        sigma = pure_sig + H_sig + Cl_sig + NH4_sig
        sigma_components = np.array([sigma, pure_sig, H_sig, Cl_sig, NH4_sig])
    else:
        # Adjust for frequency
        omega = 2 * np.pi * frequency
        base_omega = 2 * np.pi * 300000  # 300 kHz
        tau = 8e-4
        alpha = 0.15
        scale_fac = (omega * e_0 * np.imag(100 / (1 + (1j * omega * tau)**(1 - alpha))) /
                     (base_omega * e_0 * np.imag(100 / (1 + (1j * base_omega * tau)**(1 - alpha)))))
        
        sigma = (pure_sig + H_sig + Cl_sig + NH4_sig) * scale_fac
        sigma_components = np.array([sigma, pure_sig, H_sig, Cl_sig, NH4_sig]) * scale_fac

    return sigma, sigma_components



####################################################################################
####################################################################################
################################

def attenuation_from_cond(sigma, radar_frequency, method=1):
    
    # Convert frequency to angular frequency
    ang_f = 2 * np.pi * radar_frequency
    
    # Calculate wavelength
    lamda = cice / radar_frequency
    
    # Calculate wave number
    k = 2 * np.pi / lamda

    if method == 1: #From Wikipedia, Loss Tangent
        ### Equation - tan(d) = e''/e'
        ###            sigma = e'' * e_0 * ang_f
        ###
        ###            tan(d) = sigma/(e' * e_0 * ang_f)
        ###            e_0 = 8.85418782 * 10^-12
        ###            ang_f = 2*pi*f
        ###
        ###            LF = exp(-d * k * z)
        ###            log_10(LF) = -d * k * z * log_10(e)
        ###            LF_dB = -d * k * z * 10*log_10(e)
        ###
        ###            dB/m == -d * k * 10*log_10(e)
        ###            dB/km == -d * k * 10*log_10(e) * 1000
        ###
        ###            k = 2*pi / lamda
        ###            lamda = V / f
        ###            lamda = (C/sqrt(e')) / f
        
        d = np.arctan(sigma / (e_prime * e_0 * ang_f))
        att_rate = d * k * 10 * np.log10(np.exp(1)) * 1000
        
    elif method == 2: # % From MacGregor et al 2007, Skin Depth
        ### Equation Att_Length = e_0 * sqrt(e') * c / sigma
        ###          Target_Att = 1000 * 10*log10(exp(1)) * (1/Att_Length)
        ###          sigma = 1000 * 10*log10(exp(1)) * e_0 * sqrt(e') * c
        ###          sigma units = S/m
        ###                        S = A/V
        ###                        V = kg*m^2/(A*s^3)
        ###          sigma units = A^2 * s^3 / (kg * m^3)
        
        att_rate = sigma * (1000 * 10 * np.log10(np.exp(1)) / (e_0 * np.sqrt(e_prime) * cair))
    
    return att_rate

####################################################################################
####################################################################################
################################

def loss_tangent(target_attenuation, radar_frequency, method=1):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %
    % Calculate the loss tangent and conductivity based on the given method.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    

    Parameters:
    target_attenuation: float
        The target attenuation in dB/km.
    radar_frequency: float
        The radar frequency in Hz.
    method: int, optional
        The method to use for the calculation (1 for Wikipedia method, 2 for MacGregor et al. 2007 method). Default is 1.
    cice: float, optional
        The speed of light in ice (default value is an example, replace with actual value if different).
    cair: float, optional
        The speed of light in air (default value is an example, replace with actual value if different).

    Returns:
    sigma: float
        The conductivity.
    d: float or None
        The loss tangent (None if method is 2).
    """

    if method == 1:
        # Wikipedia method
        lamda = cice / radar_frequency
        k = 2 * np.pi / lamda
        ang_f = 2 * np.pi * radar_frequency

        d = target_attenuation / (k * 10 * np.log10(np.exp(1)) * 1000)
        sigma = np.tan(d) * e_prime * e_0 * ang_f

    elif method == 2:
        # MacGregor et al. 2007 method
        sigma = target_attenuation / (1000 * 10 * np.log10(np.exp(1)) / (e_0 * np.sqrt(e_prime) * cair))
        d = np.nan

    return sigma, d






####################################################################################
####################################################################################
################################

def PureIce_Temperature(sigma):
    """
    % (C) Nick Holschuh - Amherst College -- 2022 (Nick.Holschuh@gmail.com)
    %  This function (derived from MacGregor et al 2007) calculates the temperature
    %  associated with a given conducutivity for pure ice.
    %  
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %      sigma -- Conductivity
    %
    %%%%%%%%%%%%%%%
    % The outputs are:
    %      T -- The associated temperature (in K)
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """    
    
    ##  Can be taken from MacGregor et al 2007
    sig_0 = 7.2; # microSimmons / m 
    E0 = 0.55; # 0.33 eV
    T = 1./((1/251) - (np.log(sigma*10^6) - np.log(sig_0))*k/E0);




