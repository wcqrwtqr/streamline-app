import streamlit as st
from helpers.conversion_helper import conversion_helper


def conversion_page():
    st.title("Unit Conversion")
    st.markdown(
        """
    This page is for conversion between type of flow rates and pressure values
    """
    )
    try:
        conversion_helper()
    except Exception as e:
        st.write("An error occured:" + str(e))
