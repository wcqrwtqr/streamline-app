import streamlit as st
from helpers.air_compressor_helper import air_compressor_helper
import os
from PIL import Image


def air_compressor_page():
    st.title("Air-oil Ratio Calcuator 🔥")
    st.markdown(
        """
    This page is didcated to calcualte the percentage of the air to oil ratio to get
        the best air compressors capacity for the most efficient burning\n
    Ensure to get the rate between 10% and 20% to have a good burning
    """
    )
    with st.expander(label="Information and usage guidelines"):
        package_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            image = Image.open(
                os.path.join(package_dir, "../Thumbnail/EvergreenBurner.jpg")
            )
            st.image(image, caption="Evergreen Burner")
        except FileNotFoundError:
            st.error("Image not found at path: " + image)

        st.info(
            """ To get the air oil ratio update the following parameters\n
            Paramters:
            1- Update the API
            2- Oil rate in bbl per day BBL/d
            3- Air rate in Cubic Feet Minute CFM
            """
        )
    try:
        air_compressor_helper()
    except Exception as e:
        st.write("An error occured:" + str(e))
