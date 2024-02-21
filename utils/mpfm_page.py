import streamlit as st
from helpers.mpfm_helper import mpfm_data


def mpfm_page():
    st.title("Multi-phase Meter Data 🔬")
    st.markdown(
        """
                The below is to view and the multi phase meter of type __ROXAR__ online \n
                The page can view the data, download the summary values to excel and
                graph the data using a custom graph up to 4 values.
                """
    )
    source_data = st.file_uploader(
        label="Uplaod MPFM data to web page", type=["csv", "log", "txt"]
    )
    st.write("---")
    try:
        mpfm_data(source_data)
    except Exception as e:
        st.write("An error occured:" + str(e))
