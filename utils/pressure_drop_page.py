import streamlit as st
from helpers.handlers.pressuredrop_handler import pressure_drop_handler

# from helpers.mpfm_helper import mpfm_data


def pressure_drop_page():
    st.title("Pressure Drop Calculator")
    st.markdown(
        """
                This is for pressure drop calculator
                """
    )
    try:
        pressure_drop_handler()
        # mpfm_data(source_data)
    except Exception as e:
        st.write("An error occured:" + str(e))
