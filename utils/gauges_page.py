import streamlit as st
from helpers.gauges_helper import Gauges_data_Spartek
from PIL import Image

def gauges_page():
    st.title("Down Hole Gauges _Spartek_ 🌡")
    st.markdown(
        """
                The below is to manipulate __SPARTEK__ Down Hole Memory Gauges row data\n
                The page can view the data, download the values after applying a reduction factor to excel
                """
    )
    with st.expander(label="Upload row data guidelines"):
        st.warning(
            "Ensure the txt file belongs to Spartek gauges and has the format as below"
        )
        # image = Image.open(os.path.join(package_dir, "Thumbnail/spartek.jpg"))
        # st.image(image)
    source_data = st.file_uploader(
        label="Uplaod gauges data to web page", type=["csv", "log", "txt"]
    )
    st.write("---")
    try:
        Gauges_data_Spartek(source_data)
        col1, col2 = st.columns(2)
    except Exception:
        st.subheader("No Data available!!")
        st.write("Select correct data for Metrolog gauges")
