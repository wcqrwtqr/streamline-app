import streamlit as st
from helpers.nodal_helper import nodal_helper


def nodal_page():
    st.title("Nodal Analysis IPR/VLR")
    st.markdown(
        """
        This page is for making nodal analysis acknowledgement for https://github.com/FreddyEcu-Ch/Oil-and-Gas-Resources\n Please visit his page and star his work
    """
    )

    # ======================= IPR curve tab ================================
    try:
        nodal_helper()  # IPR
    except Exception:
        st.subheader("No data selected")
        st.write("Select the correct data for the PVT")
