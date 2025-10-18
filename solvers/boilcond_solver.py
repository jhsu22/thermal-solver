import numpy as np
from solvers.waterinterpolator import WaterInterp

def vertical_plate_lw(inputs, unit_system):

    tsurf_c = float(inputs['surface_temp'])
    tsat_c = float(inputs['saturated_temp'])
    length = float(inputs['length'])
    width = float(inputs['width'])
    hfg = float(inputs["latent_heat"])

    # Set gravity depending on unit system
    if unit_system == "SI":
        g = 9.81
    elif unit_system == "Imperial":
        g = 32.2

    # Calculate film temperature
    tfilm_c = (tsat_c + tsurf_c) / 2

    # Pull property values from water interpolator
    props = WaterInterp(tfilm_c)
    rhol = props['rho']
    k = props['k']
    cp = props['cp']
    mu = props['mu']
    nu = mu / rhol

    del_t = tsat_c - tsurf_c
    area = length * width

    corrected_hfg = (hfg * 1000) + (0.68 * cp * del_t)

    p_numerator = k * length * del_t
    p_denominator = mu * corrected_hfg * (nu**2 / g)**(1/3)
    p = p_numerator / p_denominator

    term1 = (0.024 * p - 53) * props['Pr']**(1/2) + 89
    hl = (k / ((nu**2 / g)**(1/3))) * (1/p) * (term1**(4/3))

    q = hl * area * del_t

    cond_rate = q / corrected_hfg

    results = {
        "Heat Transfer Rate (W)": f"{q:.2f}",
        "Conductivity (W/mK)": f"{hl:.2f}",
        "Condensation Rate (kg/s)": f"{cond_rate:.2f}"
    }
    return results

def vertical_plate_h(inputs):
    pass

def horizontal_tube_od(inputs):
    pass

def horizontal_tube_od_id(inputs):
    pass

def circular_heating_element(inputs):
    pass

def calculate_boilcond(problem_type, inputs, unit_system):
    if problem_type == "Vertical Plate (L & W)":
        return vertical_plate_lw(inputs, unit_system)
    elif problem_type == "Vertical Plate (H)":
        return vertical_plate_h(inputs)
    elif problem_type == "Horizontal Tube (OD)":
        return horizontal_tube_od(inputs)
    elif problem_type == "Horizontal Tube (OD & ID)":
        return horizontal_tube_od_id(inputs)
    elif problem_type == "Circular Heating Element":
        return circular_heating_element(inputs)
    else:
        raise ValueError("Invalid problem type")