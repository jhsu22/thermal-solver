import numpy as np
from pathlib import Path
import pandas as pd
from CoolProp.CoolProp import PropsSI
import math # Import math for exp

# Conversion Factors
DEG_C_TO_K = 273.15
DEG_F_TO_K = lambda F: (F - 32) * 5/9 + DEG_C_TO_K
IN_TO_M = 0.0254

def calculate_dphx(
        length, material, nominal_dia_inner, nominal_dia_outer,
        fluid1, fluid1_inlet_temp, fluid1_mass_flow,
        fluid2, fluid2_inlet_temp, fluid2_mass_flow, schedule, ptype):

    # Set default pressure (Atmospheric)
    pressure_pa = 101325

    # Convert string inputs to numerical types
    length = float(length)
    fluid1_inlet_temp_C = float(fluid1_inlet_temp) # Keep Celsius for initial comparison
    fluid2_inlet_temp_C = float(fluid2_inlet_temp) # Keep Celsius for initial comparison
    fluid1_mass_flow = float(fluid1_mass_flow)
    fluid2_mass_flow = float(fluid2_mass_flow)

    # Pipe Dimension Lookup
    BASE_PATH = Path(__file__).parent.parent
    PIPE_DIMENSIONS_PATH = BASE_PATH / "tables" / "pipe_dimensions.csv"
    COPPER_PIPE_PATH = BASE_PATH / "tables" / "seamless_copper_tubing.csv"
    copper_pipe_dimensions = pd.read_csv(COPPER_PIPE_PATH)
    pipe_dimensions = pd.read_csv(PIPE_DIMENSIONS_PATH)

    # Change 1: Standardized pipe dimensions lookup and conversion to meters
    ID_p_m = 0.0
    OD_p_m = 0.0
    ID_a_m = 0.0

    if "Steel" in material:
        pipe_data_inner = pipe_dimensions.loc[
            (pipe_dimensions["Nominal Diameter in"] == nominal_dia_inner) &
            (pipe_dimensions["Schedule"] == schedule)
        ]
        pipe_data_outer = pipe_dimensions.loc[
            (pipe_dimensions["Nominal Diameter in"] == nominal_dia_outer) &
            (pipe_dimensions["Schedule"] == schedule)
        ]

        if pipe_data_inner.empty or pipe_data_outer.empty:
            raise ValueError(f"Pipe dimensions not found for Steel material with nominal diameter inner={nominal_dia_inner}, outer={nominal_dia_outer}, schedule={schedule}")

        pipe_dict_inner = pipe_data_inner.iloc[0].to_dict()
        pipe_dict_outer = pipe_data_outer.iloc[0].to_dict()

        # Convert inches to meters
        ID_p_m = pipe_dict_inner["Inside Diameter cm"] * 100
        OD_p_m = pipe_dict_inner["Outside Diameter cm"] * 100
        ID_a_m = pipe_dict_outer["Inside Diameter cm"] * 100

    elif "Copper" in material:
        if not ptype or len(ptype) == 0:
            raise ValueError("Pipe type (ptype) cannot be empty for Copper material")

        pipe_type = ptype.split(" ")[-1] # Get 'K', 'L', or 'M'

        pipe_data_inner = copper_pipe_dimensions.loc[
            (copper_pipe_dimensions["Standard Size in"] == nominal_dia_inner) &
            (copper_pipe_dimensions["Type"] == pipe_type)
        ]
        pipe_data_outer = copper_pipe_dimensions.loc[
            (copper_pipe_dimensions["Standard Size in"] == nominal_dia_outer) &
            (copper_pipe_dimensions["Type"] == pipe_type)
        ]

        if pipe_data_inner.empty or pipe_data_outer.empty:
            raise ValueError(f"Pipe dimensions not found for Copper material with nominal diameter inner={nominal_dia_inner}, outer={nominal_dia_outer}, type={pipe_type}")

        pipe_dict_inner = pipe_data_inner.iloc[0].to_dict()
        pipe_dict_outer = pipe_data_outer.iloc[0].to_dict()

        # Convert cm or inches to meters
        ID_p_m = pipe_dict_inner["Inside Diameter cm"] / 100.0 # cm to m
        OD_p_m = pipe_dict_inner["Outside Diameter in"] * IN_TO_M # in to m
        ID_a_m = pipe_dict_outer["Inside Diameter cm"] / 100.0 # cm to m

    # Calculate Flow Areas in m^2
    A_p = np.pi * (ID_p_m**2) / 4.0
    A_a = np.pi * (ID_a_m**2 - OD_p_m**2) / 4.0

    # Fluid Assignment
    # Identify warm and cool fluids based on inlet temperatures
    if fluid1_inlet_temp_C > fluid2_inlet_temp_C:
        warm_fluid = fluid1
        cool_fluid = fluid2
        m_w = fluid1_mass_flow
        m_c = fluid2_mass_flow
        Temp1 = fluid1_inlet_temp_C + DEG_C_TO_K # Warm fluid inlet temp in K
        temp1 = fluid2_inlet_temp_C + DEG_C_TO_K # Cool fluid inlet temp in K
    else:
        warm_fluid = fluid2
        cool_fluid = fluid1
        m_w = fluid2_mass_flow
        m_c = fluid1_mass_flow
        Temp1 = fluid2_inlet_temp_C + DEG_C_TO_K # Warm fluid inlet temp in K
        temp1 = fluid1_inlet_temp_C + DEG_C_TO_K # Cool fluid inlet temp in K

    # Iteration Loop for Temperature Convergence
    t_loop = True
    iterations = 0
    max_iterations = 20 # Safety break for the loop

    # Initial Guesses for outlet temperatures (midpoint in K)
    Temp2 = (Temp1 + temp1) * 0.5
    temp2 = (Temp1 + temp1) * 0.5

    # Store previous iteration average temps for convergence check
    Tavg_prev = Temp1 # Initialize with inlet temps
    tavg_prev = temp1

    while t_loop and iterations < max_iterations:
        iterations += 1

        # Calculate average temperatures for property lookup (in K)
        Tavg = (Temp1 + Temp2) * 0.5
        tavg = (temp1 + temp2) * 0.5

        # --- Fluid Property Lookup using CoolProp (at average temps) ---
        try:
            rho_w = PropsSI('D', 'T', Tavg, 'P', pressure_pa, warm_fluid)
            cp_w = PropsSI('Cpmass', 'T', Tavg, 'P', pressure_pa, warm_fluid)
            k_w = PropsSI('L', 'T', Tavg, 'P', pressure_pa, warm_fluid)
            mu_w = PropsSI('V', 'T', Tavg, 'P', pressure_pa, warm_fluid)
            pr_w = PropsSI('Prandtl', 'T', Tavg, 'P', pressure_pa, warm_fluid)
            nu_w = mu_w / rho_w

            rho_c = PropsSI('D', 'T', tavg, 'P', pressure_pa, cool_fluid)
            cp_c = PropsSI('Cpmass', 'T', tavg, 'P', pressure_pa, cool_fluid)
            k_c = PropsSI('L', 'T', tavg, 'P', pressure_pa, cool_fluid)
            mu_c = PropsSI('V', 'T', tavg, 'P', pressure_pa, cool_fluid)
            pr_c = PropsSI('Prandtl', 'T', tavg, 'P', pressure_pa, cool_fluid)
            nu_c = mu_c / rho_c
        except ValueError as e:
            raise ValueError(f"CoolProp Error: {e}. Check fluid names and temperature/pressure ranges.")

        # Convection Coefficient Calculations
        # Annulus Equivalent Diameters (using meters)
        D_h = ID_a_m - OD_p_m # Hydraulic diameter for friction
        D_e = (ID_a_m**2 - OD_p_m**2) / OD_p_m # Equivalent diameter for heat transfer

        # Check which fluid goes where (higher mass flow in larger area)
        A_p_larger = A_p > A_a
        m_w_greater = m_w > m_c

        # Case 1: Warm fluid in pipe (m_w, A_p), Cool fluid in annulus (m_c, A_a)
        if (m_w_greater and A_p_larger) or (not m_w_greater and not A_p_larger):
            V_p = m_w / (rho_w * A_p)
            V_a = m_c / (rho_c * A_a)
            Re_p = (V_p * ID_p_m) / nu_w
            Re_a = (V_a * D_h) / nu_c # Use D_h for annulus Reynolds number

            # Nusselt Numbers
            if Re_p < 2300:
                Nu_p = 1.86*(ID_p_m*Re_p*pr_w/length)
            else: # Turbulent
                Nu_p = 0.023 * (Re_p ** 0.8) * (pr_w ** 0.3)

            # Annulus (Cool fluid heating -> Pr exponent = 0.4)
            if Re_a < 2300:
                Nu_p = 1.86 * (D_e * Re_a * pr_c / length)
            else: # Turbulent
                Nu_a = 0.023 * (Re_a ** 0.8) * (pr_c ** 0.4)

            # Convection Coefficients
            h_i = Nu_p * k_w / ID_p_m # Inside pipe (warm fluid)
            h_o = Nu_a * k_c / D_e # Annulus (cool fluid), use D_e for Nu_a -> h_o calculation

        # Case 2: Cool fluid in pipe (m_c, A_p), Warm fluid in annulus (m_w, A_a)
        else:
            V_p = m_c / (rho_c * A_p)
            V_a = m_w / (rho_w * A_a)
            Re_p = (V_p * ID_p_m) / nu_c
            Re_a = (V_a * D_h) / nu_w # Use D_h for annulus Reynolds number

            # Nusselt Numbers
            # Pipe (Cool fluid heating -> Pr exponent = 0.4)
            if Re_p < 2300:
                Nu_p = 1.86*(ID_p_m*Re_p*pr_c/length)
            else: # Turbulent
                Nu_p = 0.023 * (Re_p ** 0.8) * (pr_c ** 0.4)

            # Annulus (Warm fluid cooling -> Pr exponent = 0.3)
            if Re_a < 2300:
                Nu_a = 1.86*(D_e*Re_a*pr_w/length)
            else: # Turbulent
                Nu_a = 0.023 * (Re_a ** 0.8) * (pr_w ** 0.3)

            # Convection Coefficients
            h_i = Nu_p * k_c / ID_p_m # Inside pipe (cool fluid)
            h_o = Nu_a * k_w / D_e # Annulus (warm fluid), use D_e for Nu_a -> h_o calculation

        # Simplified Overall Heat Transfer Coefficient (neglecting wall resistance and fouling)
        h_p = h_i * (ID_p_m / OD_p_m)
        U_o = (1/h_p + 1/h_o)**(-1)

        # Effectiveness-NTU Calculation
        C_w = m_w * cp_w
        C_c = m_c * cp_c
        C_min = min(C_w, C_c)
        C_max = max(C_w, C_c)
        Cr = C_min / C_max

        A_o_total = np.pi * OD_p_m * length # Total heat transfer area (outer surface of inner pipe)

        NTU = U_o * A_o_total / C_min

        # Effectiveness (epsilon) for counterflow
        if Cr == 1.0: # Avoid division by zero if C_min == C_max
            epsilon = NTU / (1.0 + NTU)
        else:
            exp_term = math.exp(-NTU * (1.0 - Cr))
            epsilon = (1.0 - exp_term) / (1.0 - Cr * exp_term)

        # Calculate Heat Transfer Rate
        q = epsilon * C_min * (Temp1 - temp1) # Temp1 = T_h_in, temp1 = T_c_in

        # Calculate Outlet Temperatures using energy balance
        Temp2_new = Temp1 - q / C_w
        temp2_new = temp1 + q / C_c

        # --- Convergence Check ---
        Tavg_new = (Temp1 + Temp2_new) / 2.0
        tavg_new = (temp1 + temp2_new) / 2.0

        # Check relative change in average temperatures
        T_error = abs(Tavg_new - Tavg_prev) / Tavg_prev if Tavg_prev != 0 else 0
        t_error = abs(tavg_new - tavg_prev) / tavg_prev if tavg_prev != 0 else 0

        # Update outlet temps and previous average temps for next iteration
        Temp2 = Temp2_new
        temp2 = temp2_new
        Tavg_prev = Tavg_new
        tavg_prev = tavg_new

        # Check if converged
        if T_error < 0.005 and t_error < 0.005:
            t_loop = False

    if iterations == max_iterations:
        print("Warning: Max iterations reached, results may not be fully converged.")

    # Final Calculations (Post-Convergence)
    # Log Mean Temp Diff (Counter Flow)
    deltaT1 = Temp1 - temp2 # Hot in - Cold out
    deltaT2 = Temp2 - temp1 # Hot out - Cold in
    # Prevent division by zero or log(negative) if deltaTs are equal or cross
    if deltaT1 <= 0 or deltaT2 <= 0:
         LogMeanTempDiff = 0 # Or handle appropriately, indicates temp cross or zero difference
    elif abs(deltaT1 - deltaT2) < 1e-6: # Check if deltaTs are very close
         LogMeanTempDiff = deltaT1 # Or deltaT2
    else:
         LogMeanTempDiff = (deltaT1 - deltaT2) / np.log(deltaT1 / deltaT2)

    # Verify Heat Balance
    q_w = m_w * cp_w * (Temp1 - Temp2) # Heat lost by warm
    q_c = m_c * cp_c * (temp2 - temp1) # Heat gained by cold
    q_lmtd = U_o * A_o_total * LogMeanTempDiff # Heat calculated via LMTD

    # (Add Fouling Calculations here, recalculating U, q, and temps)

    # Results
    # Convert outlet temps back to Celsius for reporting
    Temp2_C = Temp2 - DEG_C_TO_K
    temp2_C = temp2 - DEG_C_TO_K

    results = {
        "Warm Fluid Outlet Temp (C)": f"{Temp2_C:.2f}",
        "Cool Fluid Outlet Temp (C)": f"{temp2_C:.2f}",
        "Overall Heat Transfer Coeff (Uo, W/m2K)": f"{U_o:.2f}",
        "Heat Transfer Rate (q, W)": f"{q:.2f}",
    }
    return results