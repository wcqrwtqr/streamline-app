import streamlit as st
from helpers.conversion_helper import conversion_helper


def conversion_page():
    st.title("Unit Conversion")
    st.markdown(
        """
    This page is for conversion between type of flow rates and pressure values
    """
    )
    with st.expander(label="Usage guidelines"):
        st.info(
            """ To get the air oil ratio update the following parameters\n
            Paramters:
            """
        )
    try:
        conversion_helper()
    except Exception:
        st.subheader("No data selected")
        st.write("Select the correct data for the MPFM")
