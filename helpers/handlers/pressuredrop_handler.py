import streamlit as st
import math


def darcy_weisbach(flow_rate, diameter, density, viscosity, length):
    # Convert units: 1 bbl/day = 5.615 m^3/s
    flow_rate_si = flow_rate * (5.615 / (24 * 3600))  # Convert bbl/day to m^3/s

    # Convert diameter to meters
    diameter_m = diameter * 0.0254  # Convert inches to meters

    # Reynolds number
    reynolds_number = (4 * flow_rate_si) / (math.pi * diameter_m * viscosity)

    # Friction factor using Colebrook equation (can be replaced with Moody chart or other methods)
    # This is just an approximation and might not be suitable for all conditions
    friction_factor = 0.079 / (reynolds_number**0.25)

    # Pressure drop calculation using Darcy-Weisbach equation
    pressure_drop_pa = (friction_factor * density * (flow_rate_si**2) * length) / (
        2 * diameter_m
    )

    # Convert pressure drop from Pa to psi
    pressure_drop_psi = pressure_drop_pa * 0.000145037737732

    return pressure_drop_psi


# flow_rate, diameter, density, viscosity, length
def pressure_drop_handler():
    with st.expander(label="Pressure Drop Calculator"):
        with st.form(key="Pressure Drop Calculator"):
            col1, col2, col3, col4, col5 = st.columns(5)
            flow_rate = col1.number_input(label="Flow Rate BBl/d", step=100, value=1000)
            diamter = col2.number_input(label="Size Diameter inch", step=0.5, value=3.0)
            density = col3.number_input(label="Denisty kg/m3", step=50, value=800)
            viscosity = col4.number_input(
                label="Viscosity kg/m2", step=0.1, value=0.001
            )
            length = col5.number_input(label="Length m", step=10, value=300)
            submit = st.form_submit_button(label="Submit")
            if submit:
                pressure_drop = darcy_weisbach(
                    flow_rate, diamter, density, viscosity, length
                )
                st.write(
                    f"Pressure drop across choke manifold: {pressure_drop:.2f}, psi"
                )
