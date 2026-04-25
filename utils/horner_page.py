import streamlit as st
from helpers.horner_plot_helper import Horner_plot_data
from PIL import Image
import os

package_dir = os.path.dirname(os.path.abspath(__file__))
st.set_page_config(layout="wide")


def horner_page():
    """Read the elapse time and pressure of a shut-in period and generate \
    Horner plot for calculating the skin factor and other parameters.

    This function does not accept any parameters and excute
    a gauges data in csv file with the follwoing formate
    Hours,Pressure
    19.407227,2690.043
    """
    st.title("Horner plot 📈 ")
    st.markdown(
        """
        Data generated from down hole memory gauges used to generate\
        Horner plot that is used in PTA analysis

        Ensure the csv file has two columns only elapse time called 'Hours'\
        and the second column is pressure called 'Pressure'
                """
    )
    source_data_bottom = st.file_uploader(
        label="Uplaod gauge data to web page", type=["csv"], key="file_bottom_unique"
    )
    st.write("---")
    try:
        # Execute the program

        Horner_plot_data(source_data_bottom)
    except Exception as e:
        st.write("An error occured:" + str(e))
