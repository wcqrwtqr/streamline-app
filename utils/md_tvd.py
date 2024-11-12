import pandas as pd
import numpy as np
import streamlit as st
import os
package_dir = os.path.dirname(os.path.abspath(__file__))


def md_tvd_page():
    # Streamlit File Upload and Setup
    st.title("MD to TVD Depth Conversion")
    uploaded_survey = st.file_uploader("Upload Survey CSV", type="csv")
    uploaded_md = st.file_uploader("Upload MD List CSV", type="csv")
    decimal_places = st.slider("Decimal places for TVD", 0, 4, 2)
    out_put_file_path = "Surveyresults.csv"

    if uploaded_survey and uploaded_md:
        # Load survey data
        survey_df = pd.read_csv(uploaded_survey)
        md_survey = survey_df.iloc[:, 0].astype(float)
        tvd_survey = survey_df.iloc[:, 1].astype(float)

        # Load MD input data
        md_df = pd.read_csv(uploaded_md)
        md_input = md_df.iloc[:, 0].astype(float)

        # Interpolation Function
        def calculate_tvd(md_value):
            if md_value < md_survey.min() or md_value > md_survey.max():
                st.warning(f"MD value {md_value} is out of range.")
                return None
            return np.interp(md_value, md_survey, tvd_survey)

        # Apply Interpolation to MD Input
        tvd_output = [calculate_tvd(md) for md in md_input]
        tvd_output_rounded = [round(val, decimal_places) if val is not None else None for val in tvd_output]

        # Data to DataFrame and Save
        result_df = pd.DataFrame({"MD": md_input, "TVD": tvd_output_rounded})
        result_df.dropna(inplace=True)
        result_df.to_csv(out_put_file_path, index=False)

        # Display Output
        st.write("Depth Survey Results", result_df)
        st.download_button("Download Results as CSV", data=result_df.to_csv(index=False), file_name=out_put_file_path)
