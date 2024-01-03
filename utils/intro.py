import streamlit as st
import os
from PIL import Image


def intro():
    st.title("main page")
    st.title("Oil field tool kit")
    st.subheader("👈🏼 Select service from menu bar")
    st.subheader("About the web site:")
    st.markdown(
        """
                    Upload row data from the MPFM ROXAR unit or from the Down hole memory gauges or csv files from the DAQ system and get
                    an instant graph and data set based on your requirements.\n
                    You can generate graphs and adjust it to the duration you desire and calculate the average values of the selected fields
                    then download it to csv.\n
                    """
    )
    st.write("---")
    st.write(
        "Feel free to follow me in my YouTube channel for more video on data processing"
    )

    package_dir = os.path.dirname(os.path.abspath(__file__))  # Note the pat to /utils
    image = Image.open(
        os.path.join(package_dir, "../Thumbnail/IMG_9889.JPG")
    )  # ../ to go back
    st.image(image, caption="Free Palestine")
