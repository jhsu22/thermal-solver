import numpy as np
from solvers.waterinterpolator import WaterInterp
from CoolProp.CoolProp import PropsSI

# Conversion Factors
PA_TO_KPA = 0.001
PSI_TO_KPA = 6.89476
ATM_TO_KPA = 101.325
DEG_C_TO_K = 273.15
DEG_F_TO_K = lambda F: (F - 32) * 5/9 + DEG_C_TO_K
BTU_HR_FT2_F_TO_W_M2_K = 5.678263

def vertical_plate_lw(inputs, unit_system):

    # Take user inputs
    tsurf_input = float(inputs['surface_temp'])
    pressure_input = float(inputs['pressure'])
    length_input = float(inputs['length'])
    width_input = float(inputs['width'])

    # Set gravity
    g = 9.81

    # Internal unit conversion for CoolProp
    if unit_system == "SI":
        tsurf_k = tsurf_input + DEG_C_TO_K
        pressure_pa = pressure_input
        width_m = width_input
        length_m = length_input

    elif unit_system == "Imperial":
        tsurf_k = DEG_F_TO_K(tsurf_input)
        pressure_pa = pressure_input * PSI_TO_KPA * 1000
        width_m = width_input * 0.3048
        length_m = length_input * 0.3048

    # Get pressure corresponding to Tsat
    tsat_k = PropsSI('T', 'P', pressure_pa, 'Q', 0, 'Water')
    print(tsat_k)

    # Calculate film temperature
    tfilm_k = (tsat_k + tsurf_k) / 2

    # Get property values using CoolProp
    # Liquid properties at film temperature
    rhol = PropsSI('D', 'T', tfilm_k, 'P', pressure_pa, 'Water')    # Density
    k = PropsSI('L', 'T', tfilm_k, 'P', pressure_pa, 'Water')       # Thermal Conductivity
    cp = PropsSI('Cpmass', 'T', tfilm_k, 'P', pressure_pa, 'Water') # Specific Heat
    mu = PropsSI('V', 'T', tfilm_k, 'P', pressure_pa, 'Water')      # Dynamic Viscosity

    # Saturated properties at Tsat
    hf = PropsSI('Hmass', 'T', tsat_k, 'Q', 0, 'Water')         # Enthalpy sat liq
    hg = PropsSI('Hmass', 'T', tsat_k, 'Q', 1, 'Water')         # Enthalpy sat gas
    hfg = hg - hf                                                                    # Latent heat
    pr = PropsSI('Prandtl', 'T', tsat_k, 'Q', 0, 'Water')       # Prandtl Number

    nu = mu / rhol                  # Kinematic Viscosity
    del_t = tsat_k - tsurf_k        # Temperature Difference
    area = length_m * width_m

    # Calculate corrected latent heat
    corrected_hfg = hfg + (0.68 * cp * del_t)

    # Calculate dimensionless heat flux
    p_numerator = k * length_m * del_t
    p_denominator = mu * corrected_hfg * (nu**2 / g)**(1/3)
    p = p_numerator / p_denominator

    # Find heat transfer coefficient
    term1 = (0.024 * p - 53) * pr**(1/2) + 89
    hl = (k / ((nu**2 / g)**(1/3))) * (1/p) * (term1**(4/3))

    # Calculate heat transfer rate
    q = hl * area * del_t

    # Calculate condensation rate
    cond_rate = q / corrected_hfg

    results = {
        "Heat Transfer Rate (W)": f"{q:.2f}",
        "Conductivity (W/mK)": f"{hl:.2f}",
        "Condensation Rate (kg/s)": f"{cond_rate:.2f}"
    }
    return results

def vertical_plate_h(inputs, unit_system):

    # Take user inputs
    tsurf_input = float(inputs['surface_temp'])
    height_input = float(inputs['height'])
    pressure_input = float(inputs['pressure'])

    g = 9.81

    if unit_system == "SI":
        pressure_pa = pressure_input
        tsurf_k = tsurf_input + DEG_C_TO_K
        height_m = height_input
    else:
        pressure_pa = pressure_input * PSI_TO_KPA * 1000
        tsurf_k = DEG_F_TO_K(tsurf_input)
        height_m = height_input * 0.3048

    # Get saturation temperature
    tsat_k = PropsSI('T', 'P', pressure_pa, 'Q', 0, 'Water')

    tfilm_k = (tsat_k + tsurf_k) / 2

    # Get property values
    # Liquid properties at film temperature
    rhol = PropsSI('D', 'T', tfilm_k, 'P', pressure_pa, 'Water')
    k = PropsSI('L', 'T', tfilm_k, 'P', pressure_pa, 'Water')
    cp = PropsSI('Cpmass', 'T', tfilm_k, 'P', pressure_pa, 'Water')
    mu = PropsSI('V', 'T', tfilm_k, 'P', pressure_pa, 'Water')

    # Saturated properties at saturated temperature
    hf = PropsSI('Hmass', 'T', tsat_k, 'Q', 0, 'Water')
    hg = PropsSI('Hmass', 'T', tsat_k, 'Q', 1, 'Water')
    hfg = hg - hf
    pr = PropsSI('Prandtl', 'T', tsat_k, 'Q', 0, 'Water')

    nu = mu / rhol
    del_t = tsat_k - tsurf_k

    # Calculate corrected latent heat value
    corrected_hfg = hfg + .68 * (cp/1000) * del_t

    # Calculate dimensionless heat flux
    p = (k * height_m * del_t) / (mu * corrected_hfg*(1000) * (nu**2 / g)**(1/3))

    # Determine flow regime
    if p > 2530:
        regime = "Turbulent"
    else:
        regime = "Laminar"

    # Find heat transfer coefficient
    h = k / ((nu**2 / g)**(1/3)) * 1/p * ((0.024*3627-53*(2.29)**(1/2)+89)**(4/3))

    # Calculate heat transfer rate
    q = (h * height_m * del_t)/1000

    # Calculate condensation rate
    mcond = q / corrected_hfg

    results = {
        "Flow Regime": regime,
        "Heat Transfer Rate (W)": f"{q:.2f}",
        "Condensation Rate (kg/m*s)": f"{mcond:.2f}",
    }
    return results

def horizontal_tube_od(inputs, unit_system):

    # Take user inputs
    tsurf_input = float(inputs['surface_temp'])
    outer_diameter_input = float(inputs['outer_diameter'])
    pressure_input = float(inputs['pressure'])

    g = 9.81

    if unit_system == "SI":
        pressure_pa = pressure_input
        tsurf_k = tsurf_input + DEG_C_TO_K
        outer_diameter_m = outer_diameter_input
    else:
        pressure_pa = pressure_input * PSI_TO_KPA * 1000
        tsurf_k = DEG_F_TO_K(tsurf_input)
        outer_diameter_m = outer_diameter_input * 0.3048

    # Get saturation temperature
    tsat_k = PropsSI('T', 'P', pressure_pa, 'Q', 0, 'Water')

    tfilm_k = (tsat_k + tsurf_k) / 2

    # Get property values
    # Liquid properties at film temperature
    rhol = PropsSI('D', 'T', tfilm_k, 'P', pressure_pa, 'Water')
    k = PropsSI('L', 'T', tfilm_k, 'P', pressure_pa, 'Water')
    cp = PropsSI('Cpmass', 'T', tfilm_k, 'P', pressure_pa, 'Water')
    mu = PropsSI('V', 'T', tfilm_k, 'P', pressure_pa, 'Water')

    # Saturated properties at saturated temperature
    hf = PropsSI('Hmass', 'T', tsat_k, 'Q', 0, 'Water')
    hg = PropsSI('Hmass', 'T', tsat_k, 'Q', 1, 'Water')
    hfg = hg - hf
    rhov = PropsSI('D', 'T', tsat_k, 'Q', 1, 'Water')

    delt = tsat_k - tsurf_k

    # Find corrected latent heat
    corrected_hfg = hfg + 0.68 * (cp / 1000) * delt

    # Find heat transfer coefficient
    h_a  = g * rhol * (rhol - rhov) * (k**(3)) * (corrected_hfg * 1000)
    h_b = (mu * delt * (outer_diameter_m / 1000))
    h = 0.729 * (h_a / h_b)**(1/4)

    # Find heat transfer rate
    q = (h * ((outer_diameter_m / 1000) * np.pi) * delt) / 1000

    # Find condensation rate
    mcond = q / corrected_hfg

    results = {
        "Overall Heat Transfer Coefficient (W/m²K)": f"{h:.2f}",
        "Heat Transfer Rate (W)": f"{q:.2f}",
        "Condensation Rate (kg/s)": f"{mcond:.2f}"
    }
    return results

def horizontal_tube_od_id(inputs, unit_system):

    # Get user inputs
    tmean_input = float(inputs['mean_water_temp'])
    outer_diameter_input = float(inputs['outer_diameter'])
    inner_diameter_input = float(inputs['inner_diameter'])
    outside_coeff_input = float(inputs['outside_convection_coeff'])
    inside_coeff_input = float(inputs['inside_convection_coeff'])
    pressure_input = float(inputs['pressure'])

    # Set gravity depending on unit system
    g = 9.81

    if unit_system == "SI":
        pressure_pa = pressure_input
        tmean_k = tmean_input + DEG_C_TO_K
        od_m = outer_diameter_input
        id_m = inner_diameter_input
        h_o = outside_coeff_input
        h_i = inside_coeff_input
    else:  # Imperial
        pressure_pa = pressure_input * PSI_TO_KPA * 1000
        tmean_k = DEG_F_TO_K(tmean_input)
        od_m = outer_diameter_input * 0.3048
        id_m = inner_diameter_input * 0.3048
        h_o = outside_coeff_input * BTU_HR_FT2_F_TO_W_M2_K
        h_i = inside_coeff_input * BTU_HR_FT2_F_TO_W_M2_K

    tsat_k = PropsSI('T', 'P', pressure_pa, 'Q', 0, 'Water')

    hf = PropsSI('Hmass', 'T', tsat_k, 'Q', 0, 'Water')
    hg = PropsSI('Hmass', 'T', tsat_k, 'Q', 1, 'Water')
    hfg = hg - hf

    delt = tsat_k - tmean_k

    # Unit length value for per-meter calculations
    l = 1

    # Thermal conductivity
    k = 109

    # Calculate areas per unit length
    outer_area = np.pi * od_m * l
    inner_area = np.pi * id_m * l

    # Find overall heat transfer coefficient
    uinv = (1 / (h_o * inner_area)) + ((np.log(od_m / id_m)) / (2 * np.pi * k * l)) + (1 / (h_o * outer_area))
    u = 1 / uinv

    delt = tsat_k - tmean_k

    # Find heat transfer rate per unit length
    q_per_l = u * outer_area * delt

    # Find condensation rate
    mcond = (u*delt) / hfg

    results = {
        "Overall Heat Transfer Coefficient (W/m²K)": f"{u:.2f}",
        "Heat Transfer Rate Per Unit Length (W/m)": f"{q_per_l:.2f}",
        "Condensation Rate (kg/s)": f"{mcond:.2f}"
    }
    return results

def circular_heating_element(inputs, unit_system):

    # Get user inputs
    tsurf_input = float(inputs['surface_temp'])
    diameter_input = float(inputs['diameter'])
    pressure_input = float(inputs['pressure'])

    g = 9.81

    if unit_system == "SI":
        pressure_pa = pressure_input * ATM_TO_KPA * 1000
        tsurf_k = tsurf_input + DEG_C_TO_K
        diameter_m = diameter_input
    else:
        pressure_pa = pressure_input * ATM_TO_KPA * 1000
        tsurf_k = DEG_F_TO_K(tsurf_input)
        diameter_m = diameter_input * 0.3048

    # Get saturation temperature
    tsat_k = PropsSI('T', 'P', pressure_pa, 'Q', 0, 'Water')

    # Get water properties
    hf = PropsSI('Hmass', 'T', tsat_k, 'Q', 0, 'Water')
    hg = PropsSI('Hmass', 'T', tsat_k, 'Q', 1, 'Water')
    hfg = hg - hf

    sigma = PropsSI('I', 'T', tsat_k, 'Q', 0, 'Water')
    rhol = PropsSI('D', 'T', tsat_k, 'Q', 0, 'Water')
    mu = PropsSI('V', 'T', tsat_k, 'Q', 0, 'Water')
    cp = PropsSI('Cpmass', 'T', tsat_k, 'Q', 0, 'Water')
    rhov = PropsSI('D', 'T', tsat_k, 'Q', 1, 'Water')
    pr = PropsSI('Prandtl', 'T', tsat_k, 'Q', 0, 'Water')

    # Calculate temperature difference
    delt = tsurf_k - tsat_k

    # Surface fluid factor for calculations
    c_sf = 0.013

    # Calculate surface area
    radius = diameter_m / 2
    surface_area = np.pi * radius**2

    # Calculate heat transfer rate
    q_s1 = (mu * (hfg*1000))
    q_s2 = ((g * (rhol - rhov)) / (sigma)**(1/2))
    q_s3 = ((cp * delt) / (c_sf * (hfg * 1000) * pr)) ** (3)

    q_s = q_s1 * q_s2 * q_s3

    # Find required power
    q_boil = q_s * surface_area

    # Find evaporation rate
    mevap = q_boil / (hfg * 1000)

    results = {
        "Heat Transfer Rate (W)": f"{q_s:.2f}",
        "Required Power (W)": f"{q_boil:.2f}",
        "Evaporation Rate (kg/s)": f"{mevap:.2f}"
    }
    return results

def calculate_boilcond(problem_type, inputs, unit_system):
    if problem_type == "Vertical Plate (L & W)":
        return vertical_plate_lw(inputs, unit_system)
    elif problem_type == "Vertical Plate (H)":
        return vertical_plate_h(inputs, unit_system)
    elif problem_type == "Horizontal Tube (OD)":
        return horizontal_tube_od(inputs, unit_system)
    elif problem_type == "Horizontal Tube (OD & ID)":
        return horizontal_tube_od_id(inputs, unit_system)
    elif problem_type == "Circular Heating Element":
        return circular_heating_element(inputs, unit_system)
    else:
        raise ValueError("Invalid problem type")