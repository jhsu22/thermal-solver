import pandas as pd
from pathlib import Path
import numpy as np

# Helper function for input validation
def validate_input(value, name, check_positive=True):
    """Tries to convert value to float and checks if positive."""
    if not value: # Check if empty
        raise ValueError(f"Input '{name}' cannot be empty.")
    try:
        num_value = float(value)
        if check_positive and num_value <= 0:
            raise ValueError(f"Input '{name}' must be positive.")
        return num_value
    except ValueError:
        raise ValueError(f"Invalid numeric input for '{name}': {value}")

def get_piping_dimensions(material, nominal_dia, schedule=None, ptype=None):
    BASE_PATH = Path(__file__).parent.parent
    PIPE_DIMENSIONS_PATH = BASE_PATH / "tables" / "pipe_dimensions.csv"
    COPPER_TUBING_PATH = BASE_PATH / "tables" / "seamless_copper_tubing.csv"

    try:
        if "Copper" in material:
            properties = pd.read_csv(COPPER_TUBING_PATH)
            if not ptype:
                 raise ValueError("Copper pipe type (K, L, M) must be selected.")
            pipe_type = ptype.split(" ")
            pipe_data = properties.loc[
                (properties["Standard Size in"] == nominal_dia) &
                (properties["Type"] == pipe_type[-1])
            ]
        else:  # Material is steel
            properties = pd.read_csv(PIPE_DIMENSIONS_PATH)
            if not schedule:
                raise ValueError("Steel pipe schedule must be selected.")
            pipe_data = properties.loc[
                (properties["Nominal Diameter in"] == nominal_dia) &
                (properties["Schedule"] == schedule)
            ]

        if pipe_data.empty:
            raise ValueError(f"Pipe dimensions not found for: Material='{material}', Dia='{nominal_dia}', Schedule='{schedule}', Type='{ptype}'.")

        return pipe_data.iloc[0].to_dict()

    except FileNotFoundError:
        raise FileNotFoundError("Error: Pipe dimensions CSV file not found.")
    except Exception as e:
        raise Exception(f"Error reading pipe dimensions: {e}")


def get_fluid_properties(fluid):
    BASE_PATH = Path(__file__).parent.parent
    PROPERTIES_PATH = BASE_PATH / "tables" / "fluidpropertiesdensityvisc.csv"
    try:
        properties = pd.read_csv(PROPERTIES_PATH)
        fluid_data = properties.loc[properties["Substance"] == fluid]
        if fluid_data.empty:
            raise ValueError(f"Fluid properties not found for '{fluid}'.")
        return fluid_data.iloc[0].to_dict()
    except FileNotFoundError:
        raise FileNotFoundError("Error: Fluid properties CSV file not found.")
    except Exception as e:
        raise Exception(f"Error reading fluid properties: {e}")

def calculate_piping(length, material, nominal_dia, fluid, fluid_flow, schedule=None, ptype=None, unit_system="SI"):
    try:
        # --- Input Validation ---
        length_val = validate_input(length, "Length")
        fluid_flow_val = validate_input(fluid_flow, "Fluid Flow Rate")
        # Material, nominal_dia, fluid, schedule, ptype are validated during lookup

        # --- Get Properties (wrapped in try...except in helper functions) ---
        pipe_dims = get_piping_dimensions(material, nominal_dia, schedule, ptype)
        fluid_props = get_fluid_properties(fluid)

        # --- Calculations ---
        # Gather initial values based on unit system
        if unit_system == "SI":
            inside_diameter_cm = validate_input(pipe_dims.get('Inside Diameter cm'), "Inside Diameter (from CSV)")
            inside_diameter_std = inside_diameter_cm / 100
            flow_area_cm2 = validate_input(pipe_dims.get('Flow Area cm^2'), "Flow Area (from CSV)")
            flow_area_std = flow_area_cm2 / 10000
            dia_unit = "cm"
            area_unit = "cm²"

            fluid_density = validate_input(fluid_props.get('Density (kg/m³)', None), f"Density for {fluid}")
            density_unit = "kg/m³"
            fluid_viscosity = validate_input(fluid_props.get('Dynamic Viscosity (Pa·s)', None), f"Viscosity for {fluid}")
            viscosity_unit = "Pa·s"

            if material == "Steel": epsilon_mm = 0.046 # Updated based on common values
            elif material == "Copper": epsilon_mm = 0.0015
            else: raise ValueError(f"Unknown material for roughness: {material}")
            epsilon = epsilon_mm / 1000 # Convert mm to m
            roughness_unit = "mm"
            pressure_unit = "kPa"

        else:  # Imperial
            inside_diameter_ft = validate_input(pipe_dims.get('Inside Diameter ft'), "Inside Diameter (from CSV)")
            inside_diameter_std = inside_diameter_ft
            flow_area_ft2 = validate_input(pipe_dims.get('Flow Area ft^2'), "Flow Area (from CSV)")
            flow_area_std = flow_area_ft2
            dia_unit = "ft"
            area_unit = "ft²"

            fluid_density = validate_input(fluid_props.get('Density (lb/ft³)', None), f"Density for {fluid}")
            density_unit = "lb/ft³"
            fluid_viscosity = validate_input(fluid_props.get('Dynamic Viscosity (lb·s/ft²)', None), f"Viscosity for {fluid}")
            viscosity_unit = "lb·s/ft²"

            if material == "Steel": epsilon_in = 0.0018 # in
            elif material == "Copper": epsilon_in = 0.00006 # in
            else: raise ValueError(f"Unknown material for roughness: {material}")
            epsilon = epsilon_in / 12 # Convert in to ft
            roughness_unit = "in"
            pressure_unit = "psi" # Changed from ksi to psi

        error = 1.0
        friction_factor = 0.02 # Initial guess

        # Iteration setup
        max_iterations = 100
        tolerance = 0.005 # Stricter tolerance
        iteration = 0

        if flow_area_std <= 1e-9: # Avoid division by zero
             raise ValueError("Pipe flow area is too small or zero.")

        velocity = fluid_flow_val / flow_area_std

        # Check for zero velocity
        if abs(velocity) < 1e-9:
            return {f"Pressure Drop ({pressure_unit})": f"0.00"} # No flow, no pressure drop

        # Calculate Reynolds number
        if abs(fluid_viscosity) < 1e-12:
            raise ValueError("Fluid viscosity is zero, cannot calculate Reynolds number.")
        re = abs((fluid_density * velocity * inside_diameter_std) / fluid_viscosity) # Use abs for Re

        while error > tolerance and iteration < max_iterations:
            iteration += 1
            # Calculate friction factor
            if re < 2300: # Use 2300 for transition Reynolds number
                friction_factor_new = 64 / re
            else:
                rel_roughness = epsilon / inside_diameter_std
                # Explicit Colebrook equation (using Haaland as initial guess for iterative solver if needed, but direct Haaland is often sufficient)
                # Using Haaland directly for simplicity here:
                term1 = (rel_roughness / 3.7)**1.11
                term2 = 6.9 / re
                try:
                    friction_factor_new = (-1.8 * np.log10(term1 + term2))**-2
                except ValueError:
                     raise ValueError("Calculation error: Invalid value in friction factor logarithm.")


            if friction_factor > 1e-9: # Avoid division by zero if ff is near zero
                error = abs(friction_factor_new - friction_factor) / friction_factor
            else:
                error = 0 # Converged if ff is zero

            friction_factor = friction_factor_new

            if iteration == max_iterations:
                print("Warning: Max iterations reached for friction factor calculation.")

        # Calculate pressure drop
        del_p_std_units = ((friction_factor * length_val) / inside_diameter_std) * ((fluid_density * velocity**2) / 2)

        # Convert pressure drop to desired output unit
        if unit_system == "SI":
            del_p_print = del_p_std_units / 1000 # Pa to kPa
        else: # Imperial
            del_p_print = del_p_std_units / 144 # lbf/ft^2 to psi

        # Return results as dictionary for success
        return {
            f"Pressure Drop ({pressure_unit})": f"{del_p_print:.2f}",
            "Reynolds Number": f"{re:.2e}",
            "Friction Factor": f"{friction_factor:.4f}",
            "Velocity": f"{velocity:.3f} {'m/s' if unit_system == 'SI' else 'ft/s'}"
            }

    # Catch specific and general errors, return as strings
    except ValueError as ve:
        return f"Input Error: {ve}"
    except FileNotFoundError as fnfe:
        return f"Data File Error: {fnfe}"
    except ZeroDivisionError:
        return "Calculation Error: Division by zero occurred. Check inputs (e.g., diameters, flow area)."
    except OverflowError:
        return "Calculation Error: Numerical overflow. Check input magnitudes."
    except Exception as e:
        # Log the full error for debugging if needed
        # print(f"An unexpected error occurred: {type(e).__name__} - {e}")
        return f"An unexpected error occurred: {e}"