import streamlit as st
from helpers.pvt_helper import pvt_helper


def pvt_page():
    st.title("PVT correlation")
    st.markdown(
        """
        This page is used to calculate the PVT parametes\n
        The calculations are computed based on the script done by https://github.com/yohanesnuwara/pyreservoir repositry\n
        Please visit his page and star his work
    """
    )
    try:
        pvt_helper()
    except Exception:
        st.subheader("No data selected")
        st.write("Select the correct data for the PVT")
