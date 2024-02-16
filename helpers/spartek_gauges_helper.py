import pandas as pd
import streamlit as st
from helpers.handlers.make_graphs import make_graphs, make_graphs_optimized
from helpers.handlers.derived_pressure import calc_derivative_np
from helpers.handlers.read_csv_gauges import (
    read_csv_standard,
    read_csv_chunck,
    read_csv_concurrency,
)
import time


@st.cache_data
def load_df_spartek(source_file, row: int):
    """This helper funciton to cache the dataframe to memoery so there is no
    extensive computation evey time we change the values

    :param source_file: file path
    :type source_file: string
    :param row: number of rows
    :type row: int

    :returns: df , range_data
    :rtype: dataframe
    """
    start_time = time.time()

    df = read_csv_standard(source_file, row, is_spartek=True)
    # df = read_csv_chunck(source_file, row, is_spartek=True)
    # df = read_csv_concurrency(source_file, row, is_spartek=True)

    end_time_loaded = time.time()
    execution_time_loaded = end_time_loaded - start_time

    # Get the time in secods so I can get the differensial values
    df["time_diff"] = df["date_time_corrected"].diff().dt.seconds
    # Calcualte the change in rate
    df["pressure_diff"] = df["pressure"].diff()
    df["temperature_diff"] = df["temperature"].diff()
    df["1st_derivative"] = (df["pressure_diff"] / df["time_diff"]) * 100
    # df["1st_derivative_t"] = (df["temperature_diff"] / df["time_diff"]) * 100
    # df["2nd_derivative"] = (df["pressure_diff"].diff() / df["time_diff"]) * 100

    # df_new = df[["elpse", "pressure"]]
    # elpse_array = df_new["elpse"].values
    # pressure_array = df_new["pressure"].values
    # derive_result = calc_derivative_np(elpse_array, pressure_array, 0.0)
    # derive_result_df = pd.DataFrame(derive_result)
    # df.loc[:, "derived_pressure"] = derive_result_df

    end_time_statistics = time.time()
    execution_time_statistics = end_time_statistics - start_time

    st.success(
        f"Done ... Load csv file took {execution_time_loaded:.2f} sec , statistics took {execution_time_statistics:.2f} sec"
    )

    range_data = df.index.tolist()

    return df, range_data


def Gauges_data_Spartek(source_file, row=20):
    """
    This function accept the csv file and make the streamlit
    calculcation
    """
    df, range_data = load_df_spartek(source_file, row)
    range_data_selection = st.slider(
        "Range:",
        min_value=min(range_data),
        max_value=max(range_data),
        value=(min(range_data), max(range_data)),
    )

    # Creating the masked df from the index
    df_lst = df[range_data_selection[0] : range_data_selection[1]]
    # Showing the graphs
    st.markdown(
        f'Max __Temperature__: {df_lst["temperature"].max()} - Max __Pressure__: {df_lst["pressure"].max()}'
    )
    st.markdown(f"*Available Data: {df_lst.shape[0]}")

    start_time = time.time()
    with st.expander(label="Table of Data"):
        NN = st.selectbox("Interval", [1, 2, 5, 10, 25, 50, 100])
        if NN is None:  # This code is to address int|None condition
            NN = 1
        st.dataframe(df_lst.loc[:: int(NN)])
        st.markdown(f"*Available Data: {df_lst.loc[::int(NN)].shape[0]}")
        st.download_button(
            label="Download data", data=df_lst.loc[:: int(NN)].to_csv(), mime="text/csv"
        )

    end_time_draw = time.time()
    execution_time_draw = end_time_draw - start_time

    make_graphs(df_lst, st)
    # make_graphs_optimized(df_lst, st)

    end_time_graphing = time.time()
    execution_time_graphing = end_time_graphing - start_time
    st.success(
        f"Done ... Draw table took {execution_time_draw:.2f} sec , Graphing took {execution_time_graphing:.2f} sec"
    )
