import pandas as pd
from pathlib import Path
import numpy as np

def get_piping_dimensions(material, nominal_dia, schedule=None, ptype=None):

    # Get project base path
    BASE_PATH = Path(__file__).parent.parent
    PIPE_DIMENSIONS_PATH = BASE_PATH / "tables" / "pipe_dimensions.csv"
    COPPER_TUBING_PATH = BASE_PATH / "tables" / "seamless_copper_tubing.csv"

    if "Copper" in material:
        properties = pd.read_csv(COPPER_TUBING_PATH)
        pipe_type = ptype.split(" ")

        pipe_data = properties.loc[
            (properties["Standard Size in"] == nominal_dia) &
            (properties["Type"] == pipe_type[-1])
            ]

    else:  # Material is steel
        properties = pd.read_csv(PIPE_DIMENSIONS_PATH)

        pipe_data = properties.loc[
            (properties["Nominal Diameter in"] == nominal_dia) &
            (properties["Schedule"] == schedule)
            ]

    if pipe_data.empty:
        raise ValueError("Pipe dimensions not found for the selected specifications.")

    return pipe_data.iloc[0].to_dict()

def get_fluid_properties(fluid):

    BASE_PATH = Path(__file__).parent.parent
    PROPERTIES_PATH = BASE_PATH / "tables" / "fluidpropertiesdensityvisc.csv"

    properties = pd.read_csv(PROPERTIES_PATH)
    fluid_data = properties.loc[properties["Substance"] == fluid]

    if fluid_data.empty:
        raise ValueError("Fluid properties not found for the selected fluid.")

    return fluid_data.iloc[0].to_dict()

def calculate_piping(length, material, nominal_dia, fluid, fluid_flow, schedule=None, ptype=None, unit_system="SI"):
    try:
        pipe_dims = get_piping_dimensions(material, nominal_dia, schedule, ptype)
        fluid_props = get_fluid_properties(fluid)

        # Gather initial values based on unit system
        if unit_system == "SI":
            # Diameter and flow area values from tables
            inside_diameter = pipe_dims.get('Inside Diameter cm')
            inside_diameter_std = inside_diameter / 100
            flow_area = pipe_dims.get('Flow Area cm^2')
            flow_area_std = flow_area / 10000
            dia_unit = "cm"
            area_unit = "cm²"

            # Density and viscosity values from tables
            fluid_density = fluid_props.get('Density (kg/m³)')
            density_unit = "kg/m³"
            fluid_viscosity = fluid_props.get('Dynamic Viscosity (Pa·s)')
            viscosity_unit = "Pa·s"

            # Roughness values based on material
            if material == "Steel":
                epsilon = 0.0046
            if material == "Copper":
                epsilon = 0.0015
            roughness_unit = "mm"

            pressure_unit = "kPa"

        else:  # Imperial
            # Diameter and flow area values from tables
            inside_diameter = pipe_dims.get('Inside Diameter ft')
            inside_diameter_std = inside_diameter
            flow_area = pipe_dims.get('Flow Area ft^2')
            flow_area_std = flow_area
            dia_unit = "ft"
            area_unit = "ft²"

            # Density and viscosity values from tables
            fluid_density = fluid_props.get('Density (lb/ft³)')
            density_unit = "lb/ft³"
            fluid_viscosity = fluid_props.get('Dynamic Viscosity (lb·s/ft²)')
            viscosity_unit = "lb·s/ft²"

            # Roughness values based on material
            if material == "Steel":
                epsilon = 0.000181
            if material == "Copper":
                epsilon = 5.91E-5
            roughness_unit = "in"

            pressure_unit = "ksi"

        error = 1
        friction_factor = 0.02 # Initial guess for iteration

        while error > 0.05:
            # Calculate velocity
            velocity = fluid_flow / flow_area_std

            # Calculate Reynolds number
            re = (fluid_density * velocity * inside_diameter_std) / fluid_viscosity

            # Calculate friction factor
            if re < 2100:
                friction_factor_new = 64 / re
            else:
                rel_roughness = epsilon / inside_diameter_std
                # Haaland equation for friction factor
                friction_factor_new = (1 / (-1.8 * np.log10((rel_roughness / 3.7) ** 1.11 + 6.9 / re))) ** 2

            error = abs(friction_factor_new - friction_factor) / friction_factor
            friction_factor = friction_factor_new

        # Calculate pressure drop
        del_p = ((friction_factor * length) / inside_diameter_std) * ((fluid_density * velocity**2) / 2)

        del_p_print = del_p / 1000

        return f"Pressure Drop: {del_p_print:.2f} {pressure_unit}"

    except (ValueError, FileNotFoundError) as e:
        return str(e)