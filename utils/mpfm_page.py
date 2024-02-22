import streamlit as st
from helpers.mpfm_helper import mpfm_data
import os
from PIL import Image


def mpfm_page():
    st.title("Multi-phase Meter Data 🔬")
    st.markdown(
        """
                The below is to view and the multi phase meter of type __ROXAR__ online \n
                The page can view the data, download the summary values to excel and
                graph the data using a custom graph.
                """
    )
    with st.expander(label="Information About MPFM"):
        package_dir = os.path.dirname(
            os.path.abspath(__file__)
        )  # Note the pat to /utils
        st.markdown(
            """
            Multiphase Flow Metering solutions offer critical information on well streams without \
            fluid separation. Vital information for optimizing production, flow assurance and \
            compliance to regulations with the most compact and cost-effective solutions.\n
            The device after being installed online it generate an **ASCII** file that has the raw \
            data it computed.
                    """
        )
        image = Image.open(os.path.join(package_dir, "../Thumbnail/roxar.jpg"))
        st.image(image, caption="Roxar Multiphase meter")
    source_data: str = st.file_uploader(
        label="Uplaod MPFM data to web page", type=["csv", "log", "txt"]
    )
    st.write("---")
    try:
        mpfm_data(source_data)
    except Exception as e:
        st.write("An error occured:" + str(e))
