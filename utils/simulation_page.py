import streamlit as st
from helpers.simulation_helper import simulation_helper


def simulation_page():
    st.title("Trucks Loading Simulation 🚚")
    st.markdown(
        """
                    The below is to __simulate__ the number of trucks that can be loaded in a loading station \n
                    The input below is used to change the simulation variables and see the final results below
                    """
    )
    with st.expander(label="Usage guidelines"):
        st.info(
            """Choose the number of __loading stations__, __time to fill__ each
                    truck, __number of trucks__ provided at a certain time
                    and see the number of trucks that can be
                    filled in the at a duration\n
                Paramters:
                1- Number of loading stations
                2- Time of filling duration (in minutes)
                3- Number of trucks provided at any given time
                4- Loading duration (12 or 24 hours)
                    """
        )
    try:
        simulation_helper()
    except Exception:
        st.subheader("No data selected")
        st.write("Select the correct data for the PVT")
