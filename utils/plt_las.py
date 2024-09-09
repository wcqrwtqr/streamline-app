import streamlit as st
from helpers.plt_las_helper import graph_las_data
from PIL import Image
import os


package_dir = os.path.dirname(os.path.abspath(__file__))

def plt_las_page():
    st.title("PLT las file 🌡")
    st.markdown(
        """
        Quickly and easily manipulate the data from __SPARTEK__ Down Hole Memory Gauges \
        with our provided tool. View the data on the page or download it to Excel for \
            further analysis or processing.
                """
    )
    with st.expander(label="Upload row data guidelines"):
        st.warning(
            "Ensure the file is .las extenstion"
        )
        try:
            image = Image.open(os.path.join(package_dir, "../Thumbnail/spartek.jpg"))
            st.image(image)
        except FileNotFoundError:
            st.error("Image not found at path: " + image)
    source_data = st.file_uploader(
        label="Uplaod plt data to web page", type="las"
    )
    try:
        # Execute the program
        graph_las_data(source_data.name)
    except Exception as e:
        st.write("An error occured:" + str(e))
