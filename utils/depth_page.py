import streamlit as st
from helpers.depth_goes_helper import depth_data_goes
import os


package_dir = os.path.dirname(os.path.abspath(__file__))
st.set_page_config(layout="wide")


def depth_goes_page():
    # Read the data from GEOS depth meter a gauges data.
    st.title("GOES Depth")
    st.markdown(
        """
        Quickly and easily manipulate the data from GOES depth meter.
        View the data on the page or download it to Excel for \
            further analysis or processing.
                """
    )
    source_data_bottom = st.file_uploader(
        label="Uplaod detph csv data to web page",
        type=["csv"],
        key="file_bottom_unique",
    )
    st.write("---")
    try:
        # Execute the program
        depth_data_goes(source_data_bottom)
    except Exception as e:
        st.write("An error occured:" + str(e))
