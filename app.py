import streamlit as st
from utils.intro import intro
from utils.mpfm_page import mpfm_page
from utils.air_compressor_page import air_compressor_page
from utils.pvt_page import pvt_page
from utils.simulation_page import simulation_page


if __name__ == "__main__":
    # Make the pages here in a Dict
    page_name_to_func = {
        "Intro": intro,
        "MPFM": mpfm_page,
        "Air Supply": air_compressor_page,
        "PVT": pvt_page,
        "Simulation": simulation_page,
    }
    # Get the string of pages
    page_name = st.sidebar.selectbox("Choose page", page_name_to_func.keys())
    # make the pages
    page_name_to_func[page_name]()
