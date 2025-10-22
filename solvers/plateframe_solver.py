import numpy as np
import pandas as pd
from pathlib import Path
from solvers.waterinterpolator import WaterInterp
from CoolProp.CoolProp import PropsSI

pressure_pa = 101325

def calculate_plateframe(plates, length, width, hot_fluid, hot_fluid_inlet_temp, hot_fluid_mass_flow, 
                         cold_fluid, cold_fluid_inlet_temp, cold_fluid_mass_flow):

    ## Givens

    # mass flow rates
    m_w = float(hot_fluid_mass_flow)     # mass flow rate of warmer fluid
    m_c = float(cold_fluid_mass_flow)       # mass flow rate of cooler fluid

    # inlet temps
    Temp1 = float(hot_fluid_inlet_temp)                # inlet temp of warmer fluid
    temp1 = float(cold_fluid_inlet_temp)                 # inlet temp of cooler fluid

    # plate dimensions and properties
    b = .6       # plate width
    Len = 1       # plate height
    s = .0048       # plate spacing
    t = .001       # plate thickness
    N_s = 15         # number of plates
    k = 13       # thermal conductivity of plate

    Plate_material = "stainless steel (316SS)"        # plate material

    # fouling factors

    R_di = 3.52e-6
    R_do = 3.52e-6

    ## Fluid Properties
    wiswater = True            # check if warm fluid is water
    ciswater = True            # check if cool fluid is water

    m_w_greater = False        # assume m_w as smaller mass flow

    if m_w > m_c:                # verify
        m_w_greater = True     # correction 
    
    t_loop = True

    Temp2 = (Temp1 + temp1) * .5        # initial guess Temp2
    temp2 = (Temp1 + temp1) * .5       # initial guess temp2

    while t_loop == True:

        Tavg = (Temp1 + Temp2) * .5 + 273.15     # Tavg based on Temp1 and Temp2
        tavg = (temp1 + temp2) * .5 + 273.15     # tavg based on temp1 and temp2

        if wiswater == True:
            rho_w = PropsSI('D', 'T', Tavg, 'P', pressure_pa, 'Water')    # Density
            k_w = PropsSI('L', 'T', Tavg, 'P', pressure_pa, 'Water')       # Thermal Conductivity
            cp_w = PropsSI('Cpmass', 'T', Tavg, 'P', pressure_pa, 'Water') # Specific Heat
            mu_w = PropsSI('V', 'T', Tavg, 'P', pressure_pa, 'Water')      # Dynamic Viscosity
            pr_w = PropsSI('Prandtl', 'T', Tavg, 'Q', 0, 'Water')       # Prandtl Number
            nu_w = mu_w / rho_w                  # Kinematic Viscosity
            

        if ciswater == True:
            rho_c = PropsSI('D', 'T', tavg, 'P', pressure_pa, 'Water')    # Density
            k_c = PropsSI('L', 'T', tavg, 'P', pressure_pa, 'Water')       # Thermal Conductivity
            cp_c = PropsSI('Cpmass', 'T', tavg, 'P', pressure_pa, 'Water') # Specific Heat
            mu_c = PropsSI('V', 'T', tavg, 'P', pressure_pa, 'Water')      # Dynamic Viscosity
            pr_c = PropsSI('Prandtl', 'T', tavg, 'Q', 0, 'Water')       # Prandtl Number
            nu_c = mu_c / rho_c                  # Kinematic Viscosity
        
    

        ## Plate Dimensions and Properties

        A_o = b * Len     # plate surface area
        Flow_Area = s * b    # flow area
        D_h = 2 * s     # hydraulic flow

        ## Fluid Velocities

        if (N_s % 2) == 1:          # if Ns is odd
            V_w = m_w/(rho_w*Flow_Area)/((N_s + 1)/2)     # velocity warm
            V_c = m_c/(rho_c*Flow_Area)/((N_s + 1)/2)     # velocity cool
        else:
            if m_w_greater:
                V_w = m_w/(rho_w*Flow_Area)/((N_s + 2)/2)     # velocity warm
                V_c = m_c/(rho_c*Flow_Area)/((N_s)/2)     # velocity cool
            else:
                V_c = m_c/(rho_c*Flow_Area)/((N_s + 2)/2)     # velocity warm
                V_w = m_w/(rho_w*Flow_Area)/((N_s)/2)     # velocity cool
            
        

        ## Reynold's Numbers

        Re_w = V_w * D_h / nu_w
        Re_c = V_c * D_h / nu_c

        ## Nusselt Numbers

        if Re_w < 100:
            Nu_w = 1.86*(D_h * Re_w * pr_w / Len) ** (1/3) # Warm Nusselt
        else:
            Nu_w = .374 * Re_w ** 0.668 * pr_w ** (1/3)  # Cool Nusselt
        

        if Re_c < 100:
            Nu_c = 1.86*(D_h * Re_c * pr_c / Len) ** (1/3) # Warm Nusselt
        else:
            Nu_c = .374 * Re_c ** 0.668 * pr_c ** (1/3)  # Cool Nusselt
        

        ## Convection Coefficients
        h_i = Nu_w * k_w / D_h        # inner wall convection coefficient
        h_o = Nu_c * k_c / D_h        # outer wall convection coefficient

        ## Exchanger Coefficients
        U_o = (1/h_i + t/k + 1/h_o) ** -1   # Overall convection

        ## Capacitances
        h_cap_w = m_w * cp_w     # heat capacitance warm
        h_cap_c = m_c * cp_c     # heat capacitance cool

        h_cap_min = min (h_cap_w, h_cap_c)    # min heat cap

        ## Number of Transfer Units and Correction Factor

        N_factor = U_o * A_o * N_s / (h_cap_min)
        F_factor = 1 - 0.0166 * N_factor

        ## Outlet Temperature Calculations

        R_factor = h_cap_c/h_cap_w

        E_counter = np.exp(U_o * A_o * N_s * F_factor * (R_factor-1) / h_cap_c)

        Temp2_o = Temp2
        temp2_o = temp2

        Temp2 = (Temp1 * (R_factor - 1) - R_factor * temp1 * (1-E_counter)) / (R_factor * E_counter - 1)

        temp2 = (Temp1 - Temp2_o) / R_factor + temp1

        Tavg = (Temp1 + Temp2)/ 2
        tavg = (temp1 + temp2)/ 2
        
        print(temp2_o)
        print(temp2)

        T_error = abs((Temp2 - Temp2_o)/Temp2_o)
        t_error = abs((temp2 - temp2_o)/temp2_o)

        if (T_error < 0.0005) & (t_error < 0.0005):
            t_loop = False

    ## Log Mean Temperature Diffference

    LogMeanTempDiff = ((Temp1 - temp2) - (Temp2 - temp1)) / np.log((Temp1-temp2)/(Temp2 - temp1))

    ## Heat Balance for Fluids

    q_w = h_cap_w * (Temp1 - Temp2)
    q_c = h_cap_c * (temp2 - temp1)

    ## Heat Balance for the Exchanger

    q_o = -U_o * A_o * N_s * F_factor * LogMeanTempDiff

    ## Fouling Factors and Design Coefficient

    U = (1/U_o + R_di + R_do) ** -1

    ## Area Required to Transfer Heat (Determination of Plate Area)

    A_o = q_o / (U * F_factor * N_s * LogMeanTempDiff)

    ## Friction Factors

    if Re_w < 10:
        f_w = 280/Re_w
    else:
        if Re_w < 100:
            f_w = 100 / Re_w ** 0.589
        else:
            f_w = 12 / Re_w ** 0.183
        
    

    if Re_c < 10:
        f_c = 280/Re_c
    else:
        if Re_c < 100:
            f_c = 100 / Re_c ** 0.589
        else:
            f_c = 12 / Re_c ** 0.183
        
    

    ## Pressure Drop Calculations (V_p = 0)
    V_p = 0
    deltaP_w = f_w * Len * rho_w * V_w**2 / (D_h * 2) + (1.3 * rho_w * V_p)/2
    deltaP_c = f_c * Len * rho_c * V_c**2 / (D_h * 2) + (1.3 * rho_c * V_p)/2
    
    results = {
        "U_o": f"{U_o:.2f}",
        "q_o": f"{q_o:.2f}",
        "T2": f"{Temp2:.2f}",
        "t2": f"{temp2:.2f}",
        "deltaP_w": f"{deltaP_w:.2f}",
        "deltaP_c": f"{deltaP_c:.2f}",
    }
    return results