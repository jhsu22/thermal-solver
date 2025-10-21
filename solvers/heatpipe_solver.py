import numpy as np
from CoolProp.CoolProp import PropsSI

# Converison Factors
DEG_C_TO_K = 273.15
DEG_F_TO_K = lambda F: (F - 32) * 5/9 + DEG_C_TO_K
IN_TO_M = 0.0254

def calculate_heatpipe(evap_len, adia_len, cond_len, vapor_diam, wick_material, mesh, wire_diam, working_fluid, op_temp, unit_system):

    # Take user inputs
    l_evap_input = float(evap_len)
    l_adia_input = float(adia_len)
    l_cond_input = float(cond_len)
    d_vap_input =  float(vapor_diam)
    wick_material_input = str(wick_material)
    mesh_input = float(mesh)
    d_wire_input = float(wire_diam)
    working_fluid_input = str(working_fluid)
    op_temp_input = float(op_temp)
    unit_system = str(unit_system)

    # Set gravity
    g = 9.81

    # Internal Unit Conversion
    if unit_system == "SI":
        l_evap_m = l_evap_input * 100
        l_adia_m = l_adia_input * 100
        l_cond_m = l_cond_input * 100
        d_vap_m = d_vap_input * 1000
        d_wire_m = d_wire_input * IN_TO_M
        op_temp_k = op_temp_input + DEG_C_TO_K
        mesh_m = mesh_input * IN_TO_M

    else:
        l_evap_m = l_evap_input * IN_TO_M
        l_adia_m = l_adia_input * IN_TO_M
        l_cond_m = l_cond_input * IN_TO_M
        d_vap_m = d_vap_input * IN_TO_M
        d_wire_m = d_wire_input * IN_TO_M
        op_temp_k = DEG_F_TO_K(op_temp_input)
        mesh_m = mesh_input * IN_TO_M # m^-1

    # Find vapor area
    a_vap = (np.pi * d_vap_input**2) / 4

    # Effective length
    l_eff = ((l_evap_m / 2) + l_adia_m + (l_cond_m / 2))

    # Find fluid properties
    pv = PropsSI('P', 'T', op_temp_k, 'Q', 1, working_fluid_input)
    hf = PropsSI('Hmass', 'T', op_temp_k, 'Q', 0, working_fluid_input)
    hg = PropsSI('Hmass', 'T', op_temp_k, 'Q', 1, working_fluid_input)
    hfg = hg - hf

    rhol = PropsSI('D', 'T', op_temp_k, 'Q', 0, working_fluid_input)
    rhov = PropsSI('D', 'T', op_temp_k, 'Q', 1, working_fluid_input)
    mul = PropsSI('V', 'T', op_temp_k, 'Q', 0, working_fluid_input)
    muv = PropsSI('V', 'T', op_temp_k, 'Q', 1, working_fluid_input)

    sigma = PropsSI('I', 'T', op_temp_k, 'Q', 0, working_fluid_input)

    k_l = PropsSI('Conductivity', 'T', op_temp_k, 'Q', 0, working_fluid_input)

    k_w = 14.9

    t_wire = 3 * (2 * d_wire_m)

    d_i = d_vap_m + (2 * t_wire)

    # Find capillary limit
    rce = 1 / (2 * mesh_m)

    del_pc = (2 * sigma) / rce

    # Assume laminar flow Re < 2300, Ma < 0.2, fv_rev = 16
    c = 1

    # Vapor pressure drop
    del_pv = (c * 16 * muv) / (2 * ((d_vap_m / 2)**2) * a_vap * rhov * hfg)

    a_w = (np.pi * (d_i**2 - d_vap_m**2)) / 4           # Cross sectional area of wick

    eps = 1 - ((1.05 * np.pi * mesh_m * d_wire_m) / 4)

    k = (d_wire_m**2 * eps**3) / (122 * (1 - eps)**2)   # Wick permeability

    # Liquid presure drop
    del_pl = (mul * l_eff) / (k * a_w * hfg * rhol)

    u = 0

    # Normal hydrostatic pressure drop
    del_pnorm = rhol * g * d_vap_m * np.cos(u)

    q_capillary = (del_pc - del_pv - del_pnorm) / (del_pl)

    # Laminar flow check
    re_v = (4 * q_capillary) / (np.pi * d_vap_m * muv * hfg)

    if re_v < 2300:
        print('Laminar flow assumption correct')

    # Sonic limit
    q_sonic = 0.474 * hfg * a_vap * ((rhov * pv)**(1/2))

    # Entrainment limit
    d_hw = (4 * a_w) / (np.pi * (d_i + d_vap_m))

    q_entrainment = a_vap * hfg * (((sigma * rhov) / (2 * (d_hw / 2))**(1/2)))

    # Boiling limit
    k_eff = (k_l * ((k_l + k_w) - (1 - eps) * (k_l - k_w))) / ((k_l + k_w) + (1 - eps) * (k_l - k_w))

    q_boiling = (4 * np.pi * l_evap_m * k_eff * op_temp_k * sigma) / (hfg * rhov * np.log((d_i/2) / (d_vap_m/2))) * ((1 / (rce / 100)) - (1/rce))

    results = {
        "Capillary Limit": f"{q_capillary:.2f}",
        "Sonic Limit": f"{q_sonic:.2f}",
        "Entrainment Limit": f"{q_entrainment:.2f}",
        "Boiling Limit": f"{q_boiling:.2f}"
    }
    print(results)
    return results