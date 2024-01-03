import streamlit as st
from utils.test import test
from utils.intro import intro


if __name__ == "__main__":
    # Make the pages here in a Dict
    page_name_to_func = {
        "Intro": intro,
        "test": test,
    }
    # Get the string of pages
    page_name = st.sidebar.selectbox("Choose page", page_name_to_func.keys())
    # make the pages
    page_name_to_func[page_name]()
