# import numpy as np
# from solvers.waterinterpolator import WaterInterp
# from CoolProp.CoolProp import PropsSI

# # Conversion Factors
# PA_TO_KPA = 0.001
# PSI_TO_KPA = 6.89476
# ATM_TO_KPA = 101.325
# DEG_C_TO_K = 273.15
# DEG_F_TO_K = lambda F: (F - 32) * 5/9 + DEG_C_TO_K
# BTU_HR_FT2_F_TO_W_M2_K = 5.678263

# def calculate_dphx(
#         length, material, nominal_dia,
#         fluid1, fluid1_inlet_temp, fluid1_outlet_temp, fluid1_mass_flow,
#         fluid2, fluid2_inlet_temp, fluid2_outlet_temp, fluid2_mass_flow, unit_system):
#         ## Givens

# # mass flow rates
#     m_w =      # mass flow rate of warmer fluid
#     m_c =        # mass flow rate of cooler fluid

#     # inlet temps
#     Temp1 =                 # inlet temp of warmer fluid
#     temp1 =                  # inlet temp of cooler fluid

#     # Tubing Sizes
#     ID_t =     # Inner D of tubes
#     OD_t =     # Outer D of tubes
#     N_t =      # # tubes
#     N_p =      # # passes

#     Length =        # exchanger length

#     # Shell Data

#     D_s =      # Shell Inner D
#     Baffle_Spacing =        # Baffle spacing
#     N_b =      # # baffles
#     Pitch_T =      # Tube pitch

#     Clearance = Pitch_T - OD_t     # Clearance between tubes

#     pitch = ""        # plate material, (square or triangle)

#     # Fouling Factors

#     R_di =         # input fouling inner
#     R_do =         # input fouling outer

#     wiswater =             # input if warm fluid is water
#     ciswater =             # input if cool fluid is water

#     # friction factor

#     pipe_mat = ""

#     epsilon = 

