import streamlit as st
import pandas as pd
from typing import List, Tuple
from handlers.make_graphs import graph_template, graphing_line_arg


@st.cache_data
def load_df_depth(source_file: str, row: int) -> Tuple[pd.DataFrame, List[int]]:
    """
    Load DataFrame with depth that will take the source of csv file and put \
    it in required data frame.

    The data from the GOES unit had special characters such as ; and , which \
    is not common for us but this code will catch it and plot the data \
    accordingly.
    """
    df = pd.read_csv(
        source_file,
        skiprows=row,
        header=None,
        sep=r";",
        names=[
            "DATE",
            "TIME_LT",
            "LT2UTC",
            "LineDepth[m]",
            "LineTesion[Lbs]",
            "LineSpeed[m/min]",
            "Pressure_1[kpa]",
            "Pressure_2[kpa]",
            "ind",
        ],
        engine="python",
        decimal=",",  # added to handle comma as decimal separator
        parse_dates={"date_time_corrected": ["DATE", "TIME_LT"]},
        date_parser=lambda x: pd.to_datetime(x, format="%Y-%m-%d %H:%M:%S"),
    )
    df = df.drop(columns=["ind"])
    # Conversion factor from kPa to psi
    kPa_to_psi_factor = 0.14503773773
    # Create new columns for pressure in psi
    df["Pressure_1[psi]"] = df["Pressure_1[kpa]"] * kPa_to_psi_factor
    df["Pressure_2[psi]"] = df["Pressure_2[kpa]"] * kPa_to_psi_factor
    # Calculate the difference over 60 secs
    # This code is used to comupte the step change over 60 sec
    df["P1_acceptance_criteria"] = (
        df["Pressure_1[psi]"]
        .rolling(window=60, min_periods=1)
        .apply(lambda x: x.iloc[-1] - x.iloc[0])
    )
    df["P2_acceptance_criteria"] = (
        df["Pressure_2[psi]"]
        .rolling(window=60, min_periods=1)
        .apply(lambda x: x.iloc[-1] - x.iloc[0])
    )
    df = df.drop(columns=["Pressure_2[kpa]", "Pressure_1[kpa]"])
    range_data = df.index.tolist()
    return df, range_data


def depth_data_goes(source_file, row=5):
    """
    Depth data function will take the source csv file from Slickline unit and \
    plot it for check the depth and tension.

    Provide df and number of rows to skip form the csv file.
    """
    # Load the data by calling load_df_depth function
    df, range_data = load_df_depth(source_file, row)
    range_data_selection = st.slider(
        "Range:",
        min_value=min(range_data),
        max_value=max(range_data),
        value=(min(range_data), max(range_data)),
    )
    # Creating the masked df from the index
    df_lst = df[range_data_selection[0] : range_data_selection[1]]
    with st.expander(label="Table of Data"):
        NN = st.selectbox("Interval", [1, 2, 5, 10, 25, 50, 100])
        if NN is None:  # This code is to address int|None condition
            NN = 1
        st.dataframe(df_lst.loc[:: int(NN)])
        st.markdown(f"*Available Data: {df_lst.loc[::int(NN)].shape[0]}")
        st.download_button(
            label="Download data", data=df_lst.loc[:: int(NN)].to_csv(), mime="text/csv"
        )
    # Graph the data detph vs tension vs time
    graph_template(df_lst, st, "Depth vs Tension", "LineDepth[m]", "LineTesion[Lbs]")
    graph_template(df_lst, st, "Depth vs speed", "LineDepth[m]", "LineSpeed[m/min]")
    with st.expander(label="Time vs depth, tesnsion an speed"):
        graphing_line_arg(
            df,
            "date_time_corrected",
            st,
            ["LineTesion[Lbs]", "LineDepth[m]", "LineSpeed[m/min]"],
        )

    with st.expander(label="Time vs pressure1, pressure2, drop rate"):
        graphing_line_arg(
            df,
            "date_time_corrected",
            st,
            [
                "Pressure_1[psi]",
                "P1_acceptance_criteria",
                "Pressure_2[psi]",
                "P2_acceptance_criteria",
            ],
        )
