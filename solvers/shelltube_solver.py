import numpy as np
import pandas as pd
from pathlib import Path
from CoolProp.CoolProp import PropsSI

# Conversion Factors
PA_TO_KPA = 0.001
PSI_TO_KPA = 6.89476
ATM_TO_KPA = 101.325
DEG_C_TO_K = 273.15
DEG_F_TO_K = lambda F: (F - 32) * 5/9 + DEG_C_TO_K
BTU_HR_FT2_F_TO_W_M2_K = 5.6782639
pressure_pa = 101325

BASE_PATH = Path(__file__).parent.parent
TUBE_DIMENSIONS_PATH = BASE_PATH/"tables"/"tubedimensions.csv"
SHELL_TUBE_COUNT = BASE_PATH/"tables"/"shelltubecounts.csv"

def calculate_shelltube(
        length, shell_id, tube_od, tube_bwg,
        arrangement, tube_pitch, passes, baffles,
        warm_fluid, warm_fluid_inlet_temp, warm_fluid_mass_flow,
        cool_fluid, cool_fluid_inlet_temp, cool_fluid_mass_flow):
    ## Givens

# mass flow rates
    m_w = float(warm_fluid_mass_flow)     # mass flow rate of warmer fluid
    m_c = float(cool_fluid_mass_flow)       # mass flow rate of cooler fluid

    # inlet temps
    Temp1 =  float(warm_fluid_inlet_temp)               # inlet temp of warmer fluid
    temp1 =  float(cool_fluid_inlet_temp)                # inlet temp of cooler fluid

    # Tubing Sizes
    OD_t = float(tube_od)    # Outer D of tubes
    N_p = int(passes)     # passes

    Length = float(length)       # exchanger length
    
    ## Get tube dimensions
    tube_dimensions = pd.read_csv(TUBE_DIMENSIONS_PATH)
    
    # Use tube_od and tube_bwg to find tube_id
    tube_data = tube_dimensions.loc[(tube_dimensions["tube_od_in"]==OD_t) & (tube_dimensions["bwg"]==int(tube_bwg))]
    
    if tube_data.empty:
        raise ValueError(f"Tube dimensions not found for tube_od_in={OD_t}, bwg={tube_bwg}")
    
    tube_dict = tube_data.iloc[0].to_dict()
    
    ## Get number of tubes
    num_t = pd.read_csv(SHELL_TUBE_COUNT)
    
    # Use tube_od_in, pitch_in, pitch_layout, shell_id_in, and n_pass to find Number of Tubes (N_t)
    
    if arrangement is None:
        raise ValueError("Arrangement cannot be None")
    
    num_t_data = num_t.loc[(num_t["tube_od_in"]==OD_t) &
                           (num_t["pitch_in"]==float(tube_pitch)) &
                           (num_t["pitch_layout"]==arrangement.lower()) &
                           (num_t["shell_id_in"]==float(shell_id))
                            ]
    
    if num_t_data.empty:
        raise ValueError(f"Tube count data not found for tube_od={OD_t}, pitch={tube_pitch}, arrangement={arrangement}, shell_id={shell_id}")
    
    num_t_dict = num_t_data.iloc[0].to_dict()
    
    ID_t = tube_dict["tube_id_cm"] / 100  # Inner D of tubes
    N_t = num_t_dict[str(N_p) + "_pass"]     # tubes

    # Shell Data

    D_s = float(shell_id)     # Shell Inner D
    N_b = float(baffles)     # # baffles
    Baffle_Spacing = Length / (N_b + 1)       # Baffle spacing
    Pitch_T = float(tube_pitch)     # Tube pitch

    Clearance = Pitch_T - OD_t     # Clearance between tubes


    # Fouling Factors

    R_di = 1.76e-4        # input fouling inner
    R_do = 1.76e-4        # input fouling outer

    wiswater = True            # input if warm fluid is water
    ciswater = True             # input if cool fluid is water

    # friction factor

    pipe_mat = "Steel"  # Default pipe material

    # Surface roughness based on pipe material
    if pipe_mat == "Copper":
        epsilon = 0.0000015  # Copper pipe roughness in meters
    else:  # Steel
        epsilon = 0.000046   # Steel pipe roughness in meters

    ## Fluid Properties
    m_w_greater = False        # assume m_w as smaller mass flow

    if m_w > m_c:               # verify
        m_w_greater = True     # correction 
        
    ## Water Properties Loop
    t_loop = True

    Temp2 = (Temp1 + temp1) * .5        # initial guess Temp2
    temp2 = (Temp1 + temp1) * .5       # initial guess temp2

    while t_loop == True:
        Tavg = (Temp1 + Temp2) * .5 + 273.15      # Tavg based on Temp1 and Temp2
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
            
        ## Flow Areas
            
            A_t = N_t * np.pi * ID_t**2 / (4 * N_p)    # flow area tubes
            A_s = D_s * Clearance * Baffle_Spacing / Pitch_T                # flow area shell
            
            A_s_greater = True
            
            if A_s < A_t:
                A_s_greater = False
                
        ## Shell Equivalent Diameters

        if arrangement.lower() == "square":
            D_e = (4 * Pitch_T**2 - np.pi * OD_t**2)/(np.pi * OD_t)

        if arrangement.lower() == "triangular":
            D_e = (3.46 * Pitch_T**2 - np.pi * OD_t**2)/(np.pi * OD_t)

        ## (Route higher mass flow rate through larger flow area)
        if m_w_greater == A_s_greater:
            V_s = m_w / (rho_w * A_s)
            G_s = m_w / A_s

            V_t = m_c / (rho_c * A_t)
            G_t = m_c / A_t

            # Reynolds Numbers
            Re_s = V_s * D_e / nu_w
            Re_t = V_t * ID_t / nu_c

            # Nusselt Numbers
            if Re_t < 2200:                                      # Condition for Nu laminar
                Nu_t = (1.86 * ID_t * Re_t * pr_c / Length)**(1/3)   # Nu number
            else:                                                # Condition for Nu turbulent
                Nu_t = (0.023) * Re_t**(4/5) * pr_c ** 0.4        # Nu number
                
            Nu_s = 0.36*Re_s**0.55 * pr_w**(1/3)

            # Convection Coefficients
            h_i = Nu_t * k_c / ID_t
            h_t = h_i * ID_t / OD_t

            h_o = Nu_s * k_w / D_e

        else:
            V_t = m_w / (rho_w * A_t)
            G_t = m_w / A_t

            V_s = m_c / (rho_c * A_s)
            G_s = m_c / A_s

            # Reynolds Numbers
            Re_t = V_t * ID_t / nu_w
            Re_s = V_s * D_e / nu_c

            # Nusselt Numbers
            if Re_t < 2200:                                        # Condition for Nu laminar
                Nu_t = (1.86 * ID_t * Re_t * pr_w / Length)**(1/3)   # Nu number
            else:                                                # Condition for Nu turbulent
                Nu_t = (0.023) * Re_t**(4/5) * pr_w ** 0.3        # Nu number
                
            Nu_s = 0.36*Re_s**0.55 * pr_c**(1/3)

            # Convection Coefficients
            h_i = Nu_t * k_w / ID_t
            h_t = h_i * ID_t / OD_t

            h_o = Nu_s * k_c / D_e

        ## Exchanger Coefficients
        U_o = (1/h_t + 1/h_o) ** -1  # Overall convection

        ## Capacitances
        h_cap_w = m_w * cp_w     # heat capacitance warm
        h_cap_c = m_c * cp_c     # heat capacitance cool

        ## Outlet Temperature Calculations (L = 

        R_factor = h_cap_c/h_cap_w        # ratio of heat cap, cool / warm

        A_o = N_t * np.pi * OD_t * Length      # surface area of heat transfer

        # Calculations for C1, C2, C3, and S

        Const1 = np.exp(U_o * A_o / h_cap_c * (R_factor**2 + 1)**0.5)
        Const2 = (R_factor + 1 - (R_factor**2 + 1)**0.5)
        Const3 = (R_factor + 1 + (R_factor**2 + 1)**0.5)

        S_factor = 2*(1 - Const1) / (Const2 - Const1*Const3)

        dsflk = U_o * A_o / h_cap_c

        T2_o = Temp2
        t2_o = temp2

        temp2 = S_factor*(Temp1-temp1) + temp1
        Temp2 = Temp1 - R_factor*(temp2-temp1)

        Tavg = (Temp1 + Temp2)/ 2
        tavg = (temp1 + temp2)/ 2

        T_error = abs((Temp2 - T2_o)/Temp2)
        t_error = abs((temp2 - t2_o)/temp2)

        if T_error < 0.0005 and t_error < 0.0005:
            t_loop = False

    print(Temp2)
    print(temp2)

    ## Log Mean Temperature Diffference (Counter Flow)

    LogMeanTempDiff = ((Temp1 - temp2) - (Temp2 - temp1)) / np.log((Temp1-temp2)/(Temp2 - temp1));

    ## Heat Balance for Fluids

    q_w = h_cap_w * (Temp1 - Temp2);
    q_c = h_cap_c * (temp2 - temp1);

    ## Heat Balance for the Exchanger

    F_factor = (R_factor**2 + 1)**0.5 * np.log((1-S_factor)/(1-R_factor*S_factor)) / ((R_factor - 1)* np.log((2 - S_factor*(R_factor + 1 - (R_factor**2 + 1)**0.5)) / (2 - S_factor *(R_factor + 1 + (R_factor**2 + 1)**0.5))))           # Correction Factor

    q = U_o * A_o * F_factor * LogMeanTempDiff        # Heat transferred

    ## Fouling Factors and Design Coefficient

    U_old = (1/U_o + R_di + R_do) ** -1  # heat transfer coefficient after 1 year

    q_old = q * U_old / U_o             # q afer 1 year

    # Recalculate Outlet Temperature Calculations

    R_factor = h_cap_c/h_cap_w;        # ratio of heat cap, cool / warm

    A_o = N_t * np.pi * OD_t * Length;      # surface area of heat transfer

    # Calculations for C1, C2, C3, and S

    Const1 = np.exp(U_old * A_o / h_cap_c * (R_factor**2 + 1)**0.5);
    Const2 = (R_factor + 1 - (R_factor**2 + 1)**0.5);
    Const3 = (R_factor + 1 + (R_factor**2 + 1)**0.5);

    S_factor = 2*(1 - Const1) / (Const2 - Const1*Const3);

    asdfjd = U_old * A_o / h_cap_c;

    t2_old = S_factor*(Temp1-temp1) + temp1
    T2_old = Temp1 - R_factor*(temp2-temp1)

    ## Area Required to Transfer Heat (Determination of Plate Area)

    A_old = q / (U_old * F_factor * LogMeanTempDiff);   # area required after 1 y
    L_old = A_old / (N_t * np.pi * OD_t);  # L required after 1 y

    ## Friction Factors

    if Re_t < 2200:      # laminar condition
        f_t = 64 / Re_t;        # f tubes
    else:
        f_t = 0.25 / (np.log10(epsilon/(3.7*ID_t) - 5.74/Re_t**0.9))**2;      # f tubes

    f_s = np.exp(0.576 - 0.19 * np.log(Re_s));        # f shell

    ## Pressure Drop Calculations

    if m_w_greater == A_s_greater:
        deltaP_s = rho_w * V_s**2 * D_s * f_s * (N_b + 1) / (2 * D_e)   # pressure drop in shell
        deltaP_t = rho_c * V_t**2 * (f_t * Length / ID_t + 4)  * N_p / 2     # pressure drop in tubes

    else:
        deltaP_s = rho_c * V_s**2 * D_s * f_s * (N_b + 1) / (2 * D_e)   # pressure drop in shell
        deltaP_t = rho_w * V_t**2 * (f_t * Length / ID_t + 4)  * N_p / 2     # pressure drop in tubes

    #return(f"{U_o:.2f},   {U_old:.2f}]")

    results = {
        "New Exchanger Coefficient": f"{U_o:.2f}",
        "1 y/o Exchanger Coefficient": f"{U_old:.2f}",
    }

    return results