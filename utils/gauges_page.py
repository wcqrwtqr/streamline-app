import streamlit as st
from helpers.spartek_gauges_helper import Gauges_data_Spartek
from helpers.metrolog_gauges_helper import Gauges_data_Metrolog
from helpers.kuster_gauges_helper import Gauges_data_kuster
from PIL import Image
import os


package_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(layout="wide")

def gauges_kuster_page():
    """Read the data from kuster gauges over txt files and plot them.

    This function does not accept any parameters and excute
    a gauges data.
    """
    st.title("Down Hole Gauges _Kuster_ 🌡")
    st.markdown(
        """
        Quickly and easily manipulate the data from __Kuster__ Down Hole Memory Gauges \
        with our provided tool. View the data on the page or download it to Excel for \
            further analysis or processing.
                """
    )
    source_data_bottom = st.file_uploader(
        label="Uplaod bottom gauge data to web page", type=["csv", "txt"],
        key="file_bottom_unique"
    )
    st.write("---")
    try:
        # Execute the program
        Gauges_data_kuster(source_data_bottom)
    except Exception as e:
        st.write("An error occured:" + str(e))


def gauges_spartek_page():
    st.title("Down Hole Gauges _Spartek_ 🌡")
    st.markdown(
        """
        Quickly and easily manipulate the data from __SPARTEK__ Down Hole Memory Gauges \
        with our provided tool. View the data on the page or download it to Excel for \
            further analysis or processing. 
                """
    )
    with st.expander(label="Upload row data guidelines"):
        st.warning(
            "Ensure the txt file belongs to Spartek gauges and has the format as below"
        )
        try:
            image = Image.open(os.path.join(
                package_dir, "../Thumbnail/spartek.jpg"))
            st.image(image)
        except FileNotFoundError:
            st.error("Image not found at path: " + image)
    source_data = st.file_uploader(
        label="Uplaod gauges data to web page", type=["csv", "log", "txt"]
    )
    st.write("---")
    try:
        # Execute the program
        Gauges_data_Spartek(source_data)
    except Exception as e:
        st.write("An error occured:" + str(e))


def gauges_metrolog_page():
    st.title("Down Hole Gauges _Metrolog_ 🌡")
    st.markdown(
        """
            Quickly and easily manipulate the data from __METROLOG__ Down Hole Memory Gauges \
            with our provided tool. View the data on the page or download it to Excel for \
                further analysis or processing. 
        """
    )
    source_data = st.file_uploader(
        label="Uplaod gauges data to web page", type=["csv", "log", "txt"]
    )
    st.write("---")
    try:
        # Execute the program
        Gauges_data_Metrolog(source_data)
    except Exception as e:
        st.write("An error occured:" + str(e))
