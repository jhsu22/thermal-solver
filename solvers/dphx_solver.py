import numpy as np
from pathlib import Path
import pandas as pd
from solvers.waterinterpolator import WaterInterp
from CoolProp.CoolProp import PropsSI

# Conversion Factors
PA_TO_KPA = 0.001
PSI_TO_KPA = 6.89476
ATM_TO_KPA = 101.325
DEG_C_TO_K = 273.15
DEG_F_TO_K = lambda F: (F - 32) * 5/9 + DEG_C_TO_K
BTU_HR_FT2_F_TO_W_M2_K = 5.678263

def calculate_dphx(
        length, material, nominal_dia_inner, nominal_dia_outer,
        fluid1, fluid1_inlet_temp, fluid1_mass_flow,
        fluid2, fluid2_inlet_temp, fluid2_mass_flow, schedule, ptype):

    # Set pressure
    pressure_pa = 101325

# Tubing Lookup, set ID_a, ID_p, OD_p
    BASE_PATH = Path(__file__).parent.parent
    PIPE_DIMENSIONS_PATH = BASE_PATH / "tables" / "pipe_dimensions.csv"
    pipe_dimensions = pd.read_csv(PIPE_DIMENSIONS_PATH)
    if "Steel" in material:
        pipe_data_inner = pipe_dimensions.loc[pipe_dimensions["Nominal Diameter in"]==nominal_dia_inner & pipe_dimensions["Schedule"]==schedule]
        pipe_data_outer = pipe_dimensions.loc[pipe_dimensions["Nominal Diameter in"]==nominal_dia_outer & pipe_dimensions["Schedule"]==schedule]
        
        if pipe_data_inner.empty or pipe_data_outer.empty:
            raise ValueError(f"Pipe dimensions not found for Steel material with nominal diameter inner={nominal_dia_inner}, outer={nominal_dia_outer}, schedule={schedule}")
        
        pipe_dict_inner = pipe_data_inner.iloc[0].to_dict()
        pipe_dict_outer = pipe_data_outer.iloc[0].to_dict()
        ID_a = pipe_dict_outer["Outside Diameter in"]
        ID_p = pipe_dict_inner["Inner Diameter in"]
        OD_p = pipe_dict_inner["Inner Diameter in"]
    elif "Copper" in material:
        if not ptype or len(ptype) == 0:
            raise ValueError("Pipe type (ptype) cannot be empty for Copper material")
        
        pipe_data_inner = pipe_dimensions.loc[pipe_dimensions["Nominal Diameter in"]==nominal_dia_inner & pipe_dimensions["Type"]==ptype[-1]]
        pipe_data_outer = pipe_dimensions.loc[pipe_dimensions["Nominal Diameter in"]==nominal_dia_outer & pipe_dimensions["Type"]==ptype[-1]]
        
        if pipe_data_inner.empty or pipe_data_outer.empty:
            raise ValueError(f"Pipe dimensions not found for Copper material with nominal diameter inner={nominal_dia_inner}, outer={nominal_dia_outer}, type={ptype[-1]}")
        
        pipe_dict_inner = pipe_data_inner.iloc[0].to_dict()
        pipe_dict_outer = pipe_data_outer.iloc[0].to_dict()
        ID_a = pipe_dict_outer["Outside Diameter in"]
        ID_p = pipe_dict_inner["Inner Diameter in"]
        OD_p = pipe_dict_inner["Inner Diameter in"]
    ## Givens

    # Get pipe material
    pipe_mat = str(material)

    # Compare fluid 1 and fluid 2 temps

    if fluid1_inlet_temp > fluid2_inlet_temp:
        # mass flow rates
        warm_fluid = fluid1
        cool_fluid = fluid2
        m_w = float(fluid1_mass_flow)      # mass flow rate of warmer fluid
        m_c = float(fluid2_mass_flow)        # mass flow rate of cooler fluid
        
        # Inlet temps
        Temp1 = float(fluid1_inlet_temp)                 # inlet temp of warmer fluid
        temp1 = float(fluid2_inlet_temp)                  # inlet temp of cooler fluid
                
    else:
        # mass flow rates
        warm_fluid = fluid2
        cool_fluid = fluid1
        m_w = float(fluid2_mass_flow)      # mass flow rate of warmer fluid
        m_c = float(fluid1_mass_flow)        # mass flow rate of cooler fluid

        # inlet temps
        Temp1 =  float(fluid2_inlet_temp)               # inlet temp of warmer fluid
        temp1 = float(fluid1_inlet_temp)                  # inlet temp of cooler fluid
        
    # Check Larger Flow rate
    
    if m_w > m_c:
        m_w_greater = True
    else:
        m_w_greater = False
    
    # Temperature Loop
    t_loop = True
    
    Tavg = (Temp1 + temp1) * .5      # Tavg based on Temp1 and temp1
    tavg = (Temp1 + temp1) * .5      # tavg based on Temp1 and temp1
    Temp2 = (Temp1 + temp1) * .5      # initial guess Temp2
    temp2 = (Temp1 + temp1) * .5      # initial guess temp2
    while t_loop == True:
    # Get fluid properties
        rho_w = PropsSI('D', 'T', Tavg, 'P', pressure_pa, warm_fluid)
        rho_c = PropsSI('D', 'T', tavg, 'P', pressure_pa, cool_fluid)
        cp_w = PropsSI('Cpmass', 'T', Tavg, 'P', pressure_pa, warm_fluid)
        cp_c = PropsSI('Cpmass', 'T', tavg, 'P', pressure_pa, cool_fluid)
        k_w = PropsSI('L', 'T', Tavg, 'P', pressure_pa, warm_fluid)
        k_c = PropsSI('L', 'T', tavg, 'P', pressure_pa, cool_fluid)
        mu_w = PropsSI('V', 'T', Tavg, 'P', pressure_pa, warm_fluid)
        mu_c = PropsSI('V', 'T', tavg, 'P', pressure_pa, cool_fluid)
        nu_w = mu_w / rho_w
        nu_c = mu_c / rho_c
        pr_w = PropsSI('Prandtl', 'T', Tavg, 'P', pressure_pa, warm_fluid)
        pr_c = PropsSI('Prandtl', 'T', tavg, 'P', pressure_pa, cool_fluid)
        
        Length = float(length)       # exchanger length
        
        # Flow areas
        A_p = np.pi * ((ID_p**2) / 4)
        A_a = np.pi * ((ID_a**2 - OD_p**2) / 4)
        
        # Compare flow areas size
        # Compare flow areas size: True if A_p > A_a, else False
        A_p_larger = A_p > A_a
        
        if m_w_greater == A_p_larger:
        # Fluid velocities
            V_p = m_w / (rho_w * A_p)
            V_a = m_c / (rho_c * A_a)

            # Annulus Equivalent Diameter
            D_h = ID_a - OD_p
            D_e = (ID_a**2 - OD_p**2) / OD_p
            
            # Reynold Numbers
            
            # Calculate Reynolds number for tube
            Re_p = (V_p * ID_p) / nu_w
            
            # Calculate Reynolds number for annulus
            Re_a = (V_a * D_h) / nu_c
            
            # Nusselt Numbers (Nu = h*D/k)
            
            # Calculate Nusselt number for tube
            if Re_p < 2200:
                Nu_p = 1.86*(ID_p*Re_p*pr_w/Length)
            else:
                Nu_p = 0.023 * (Re_p ** 0.8) * (pr_w ** 0.3)
            
            # Calculate Nusselt number for annulus
            if Re_a < 2200:
                Nu_a = 1.86*(D_e*Re_a*pr_c/Length)
            else:
                Nu_a = 0.023 * (Re_a ** 0.8) * (pr_c ** 0.4)
                
            # Convection Coefficients
            
            h_i = Nu_p * k_w / ID_p
            h_p = h_i * ID_p / OD_p
            h_a = Nu_a * k_c / D_e
            
        else:
            # Fluid velocities
            V_p = m_c / (rho_c * A_p)
            V_a = m_w / (rho_w * A_a)

            # Annulus Equivalent Diameter
            D_h = ID_a - OD_p
            D_e = (ID_a**2 - OD_p**2) / OD_p
            
            # Reynold Numbers
            
            # Calculate Reynolds number for tube
            Re_p = (rho_w * V_p * ID_p) / mu_w
            
            # Calculate Reynolds number for annulus
            Re_a = (rho_c * V_a * D_h) / mu_c
            
            # Nusselt Numbers (Nu = h*D/k)
            
            # Calculate Nusselt number for tube
            if Re_p < 2200:
                Nu_p = 1.86*(ID_p*Re_p*pr_c/Length)
            else:
                Nu_p = 0.023 * (Re_p ** 0.8) * (pr_c ** 0.3)
            
            # Calculate Nusselt number for annulus
            if Re_a < 2200:
                Nu_a = 1.86*(D_e*Re_a*pr_w/Length)
            else:
                Nu_a = 0.023 * (Re_a ** 0.8) * (pr_w ** 0.4)
                
            # Convection Coefficients
            
            h_i = Nu_p * k_c / ID_p
            h_p = h_i * ID_p / OD_p
            h_a = Nu_a * k_w / D_e

        # Exchanger Coefficient
        
        U_o = (1/h_p + 1/h_a)**-1
        
        # Outlet Temperature Calculations
        
        R_factor = m_c * cp_c / (m_w * cp_w)
        
        A_o = np.pi * OD_p * Length
        
        E_counter = np.exp(U_o * A_o * (R_factor - 1)/(m_c * cp_c))
        
        T2_o = Temp2
        t2_o = temp2
            
            