import streamlit as st
from helpers.plt_las_helper import graph_las_data
from PIL import Image
import os
import tempfile

package_dir = os.path.dirname(os.path.abspath(__file__))


def plt_las_page():
    """Read las files for the PLT data."""
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
            image = Image.open(os.path.join(
                package_dir, "../Thumbnail/spartek.jpg"))
            st.image(image)
        except FileNotFoundError:
            st.error("Image not found at path: " + image)
    source_data = st.file_uploader(
        label="Uplaod plt data to web page", type="las"
    )
    try:
        # Execute the program
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(source_data.read())
            tmp_file_path = tmp_file.name
        graph_las_data(tmp_file.name)
    except Exception as e:
        st.write("An error occured:" + str(e))



def kuster_las_page():
    """Read las files for the kuster gauges."""
    st.title("Kuster las file 🌡")
    st.markdown(
        """
        Quickly and easily manipulate the data from __Kuster__ Down Hole Memory Gauges \
        with our provided tool. View the data on the page or download it to Excel for \
            further analysis or processing.
                """
    )
    source_data = st.file_uploader(
        label="Uplaod kuster plt data to web page", type="las"
    )
    try:
        # Execute the program
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(source_data.read())
            tmp_file_path = tmp_file.name
        graph_las_data(tmp_file.name)
    except Exception as e:
        st.write("An error occured:" + str(e))
