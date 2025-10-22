import numpy as np
from CoolProp.CoolProp import PropsSI

# Conversion Factors
DEG_C_TO_K = 273.15
DEG_F_TO_K = lambda F: (F - 32) * 5/9 + DEG_C_TO_K
IN_TO_M = 0.0254

def calculate_heatpipe(evap_len, adia_len, cond_len, vapor_diam, wick_material, mesh, wire_diam, layers, working_fluid, op_temp, unit_system):

    # Take user inputs
    l_evap_input = float(evap_len)
    l_adia_input = float(adia_len)
    l_cond_input = float(cond_len)
    d_vap_input =  float(vapor_diam)
    wick_material_input = str(wick_material)
    mesh_input = float(mesh) # Assuming mesh number is per inch
    d_wire_input = float(wire_diam)
    layers = float(layers)
    working_fluid_input = str(working_fluid)
    op_temp_input = float(op_temp)
    unit_system = str(unit_system)

    # Set gravity
    g = 9.81

    # Internal Unit Conversion
    if unit_system == "SI":
        # Convert inputs from GUI units (cm, mm, in, °C) to standard SI units (m, K) for calculation
        l_evap_m = l_evap_input / 100
        l_adia_m = l_adia_input / 100
        l_cond_m = l_cond_input / 100
        d_vap_m = d_vap_input / 1000
        # Wire diameter is input in inches in SI mode
        d_wire_m = d_wire_input * IN_TO_M
        op_temp_k = op_temp_input + DEG_C_TO_K
        mesh_m = mesh_input / IN_TO_M

    else: # Imperial
        # Convert inputs from GUI units to standard SI units for calculation
        l_evap_m = l_evap_input * IN_TO_M
        l_adia_m = l_adia_input * IN_TO_M
        l_cond_m = l_cond_input * IN_TO_M
        d_vap_m = d_vap_input * IN_TO_M
        d_wire_m = d_wire_input * IN_TO_M
        op_temp_k = DEG_F_TO_K(op_temp_input)
        mesh_m = mesh_input / IN_TO_M

    rv = d_vap_m / 2 # Vapor core radius
    a_vap = np.pi * rv**2 # Vapor core cross-sectional area

    # Effective length
    l_eff = (l_evap_m / 2) + l_adia_m + (l_cond_m / 2)

    # Find fluid properties using CoolProp
    pv = PropsSI('P', 'T', op_temp_k, 'Q', 1, working_fluid_input) # Vapor pressure
    hf = PropsSI('Hmass', 'T', op_temp_k, 'Q', 0, working_fluid_input) # Liquid enthalpy
    hg = PropsSI('Hmass', 'T', op_temp_k, 'Q', 1, working_fluid_input) # Vapor enthalpy
    hfg = hg - hf # Latent heat of vaporization

    rhol = PropsSI('D', 'T', op_temp_k, 'Q', 0, working_fluid_input) # Liquid density
    rhov = PropsSI('D', 'T', op_temp_k, 'Q', 1, working_fluid_input) # Vapor density
    mul = PropsSI('V', 'T', op_temp_k, 'Q', 0, working_fluid_input) # Liquid dynamic viscosity
    muv = PropsSI('V', 'T', op_temp_k, 'Q', 1, working_fluid_input) # Vapor dynamic viscosity

    sigma = PropsSI('I', 'T', op_temp_k, 'Q', 0, working_fluid_input) # Surface tension

    k_l = PropsSI('L', 'T', op_temp_k, 'Q', 0, working_fluid_input) # Liquid thermal conductivity

    # Find wick thermal conductivity based on material
    if wick_material_input == "Stainless Steel Screen":
        k_w = 14.9
    elif wick_material_input == "Copper Screen":
        k_w = 400

    # Wick thickness and inner diameter calculation
    t_wick = layers * (2 * d_wire_m) # Total wick thickness
    d_i = d_vap_m + (2 * t_wick) # Inner diameter of the heat pipe wall

    # --- Capillary Limit Calculation ---
    rce = 1 / (2 * mesh_m) # Effective capillary radius for screen wick
    del_pc = (2 * sigma) / rce # Maximum capillary pressure difference

    # Vapor pressure drop (Assuming laminar flow Re < 2300, Ma < 0.2 -> C=1, fv*Rev=16)
    c = 1.0
    fv_Rev = 16 # Friction factor * Reynolds number for laminar flow
    del_pv = (c * fv_Rev * muv * l_eff) / (2 * (rv**2) * a_vap * rhov * hfg)

    # Wick properties for liquid pressure drop
    a_w = (np.pi * (d_i**2 - d_vap_m**2)) / 4 # Cross-sectional area of wick

    eps = 1 - ((1.05 * np.pi * mesh_m * d_wire_m) / 4)

    # Permeability for wrapped screen wick
    k_perm = (d_wire_m**2 * eps**3) / (122 * (1 - eps)**2)

    # Liquid pressure drop coefficient (Delta_Pl = del_pl_coeff * q)
    del_pl_coeff = (mul * l_eff) / (k_perm * a_w * hfg * rhol)

    # Normal hydrostatic pressure drop
    u_angle = 0 # Angle with respect to horizontal in radians
    del_pnorm = rhol * g * d_vap_m * np.cos(u_angle)

    # Solve for capillary limit heat transfer rate (q_capillary)
    q_capillary = (del_pc - del_pv - del_pnorm) / del_pl_coeff # Rearranged from Eq 4.12 simplification

    # --- Sonic Limit Calculation ---
    q_sonic = 0.474 * hfg * a_vap * ((rhov * pv)**(1/2))

    # --- Entrainment Limit Calculation ---
    # Hydraulic diameter and radius of the wick structure
    Pw = np.pi * (d_i + d_vap_m) # Wetted perimeter for wick hydraulic diameter
    d_hw = (4 * a_w) / Pw # Hydraulic diameter of wick
    rh_w = d_hw / 2 # Hydraulic radius of wick
    q_entrainment = a_vap * hfg * ((sigma * rhov) / (2 * rh_w))**(1/2)

    # --- Boiling Limit Calculation ---
    # Effective thermal conductivity of the liquid-saturated wick
    k_eff = (k_l * ((k_l + k_w) - (1 - eps) * (k_l - k_w))) / ((k_l + k_w) + (1 - eps) * (k_l - k_w))

    rn = 2.54e-7 # Nucleation cavity radius (approx 0.254 um)
    ri = d_i / 2 # Inner radius of pipe wall

    q_boiling_num = (4 * np.pi * l_evap_m * k_eff * op_temp_k * sigma) * (1/rn - 1/rce)
    q_boiling_den = (hfg * rhov * np.log(ri / rv))
    # Avoid division by zero or log(1) if ri=rv
    q_boiling = q_boiling_num / q_boiling_den if q_boiling_den != 0 else float('inf')

    results = {
        "Capillary Limit": f"{q_capillary:.2f} W",
        "Sonic Limit": f"{q_sonic:.2f} W",
        "Entrainment Limit": f"{q_entrainment:.2f} W",
        "Boiling Limit": f"{q_boiling:.2f} W",
    }
    return results