import pandas as pd
import streamlit as st
from helpers.make_graphs import make_graphs


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

    df = pd.read_csv(
        source_file,
        sep=r"\s+",
        header=None,
        skiprows=row,
        names=["date", "time", "AMPM", "elpse", "pressure", "temperature"],
        engine="python",
    )

    # Combine the date time and AMPM
    df["date_time"] = df["date"] + " " + df["time"] + " " + df["AMPM"]
    df["date_time_corrected"] = pd.to_datetime(
        df["date_time"], format="%m/%d/%Y %I:%M:%S %p"
    )

    df = df.drop(columns=["date", "time", "AMPM", "date_time"])

    # Get the time in secods so I can get the differensial values
    df["time_diff"] = df["date_time_corrected"].diff().dt.second
    # Calcualte the change in rate
    df["pressure_diff"] = df["pressure"].diff()

    # Calculate the rolling standard deviation for pressure and pressure derivative
    df["1st_derivative"] = (df["pressure_diff"] / df["time_diff"]) * 100
    df["2nd_derivative"] = (df["pressure_diff"].diff() / df["time_diff"]) * 100

    # Calculate the rolling standard deviation for pressure and pressure derivative
    window_size = 50  # You can adjust the window size as needed
    df["pressure_std"] = df["pressure"].rolling(window=window_size, min_periods=1).std()
    df["pressure_derivative_std"] = (
        df["1st_derivative"].rolling(window=window_size, min_periods=1).std()
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

    with st.expander(label="Table of Data"):
        NN = st.selectbox("Interval", [1, 2, 5, 10, 25, 50, 100])
        if NN is None:  # This code is to address int|None condition
            NN = 1
        st.dataframe(df_lst.loc[:: int(NN)])
        st.markdown(f"*Available Data: {df_lst.loc[::int(NN)].shape[0]}")
        st.download_button(
            label="Download data", data=df_lst.loc[:: int(NN)].to_csv(), mime="text/csv"
        )

    make_graphs(df_lst, st)


# ********************************************************************
# *************** Gauges Function for Metrolg Gauges******************
# ********************************************************************


@st.cache_data
def load_df_metorlog(source_file, row: int):
    """This helper funciton to cache the dataframe to memoery so there is no
    extensive computation evey time we pressure  the values

    :param source_file: file path
    :type source_file: string
    :param row: number of rows
    :type row: int

    :returns: df , range_data
    :rtype: dataframe
    """
    df = pd.read_csv(
        source_file,
        sep="[,\t]",
        header=None,
        skiprows=row,
        names=["date", "time", "pressure", "temperature"],
        engine="python",
    )

    df["date_time"] = df["date"] + " " + df["time"]
    # st.write(df["date_time"].head())
    # df["date_time_corrected"] = pd.to_datetime(df["date_time"])
    df["date_time_corrected"] = pd.to_datetime(
        df["date_time"], format="%m/%d/%y %H:%M:%S"
    )
    df["time_diff"] = df["date_time_corrected"].diff().dt.total_seconds()
    # st.write("debug")

    df = df.drop(columns=["date", "time", "date_time"])
    df["pressure_diff"] = df["pressure"].diff()

    # Calculate the rolling standard deviation for pressure and pressure derivative
    df["1st_derivative"] = (df["pressure_diff"] / df["time_diff"]) * 100
    df["2nd_derivative"] = (df["pressure_diff"].diff() / df["time_diff"]) * 100
    window_size = 50  # You can adjust the window size as needed
    df["pressure_std"] = df["pressure"].rolling(window=window_size, min_periods=1).std()
    df["pressure_derivative_std"] = (
        df["1st_derivative"].rolling(window=window_size, min_periods=1).std()
    )
    range_data = df.index.tolist()
    return df, range_data


def Gauges_data_Metrolog(source_file, row=20):
    """Gauges data processing generator

    :param source_file: file path
    :type source_file: string
    :param row: number of rows
    :type row: int

    :returns: None
    :rtype: None"""

    df, range_data = load_df_metorlog(source_file, row)
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

    with st.expander(label="Table of Data"):
        NN = st.selectbox("Interval", [1, 2, 5, 10, 25, 50, 100])
        if NN is None:  # This code is to address int|None condition
            NN = 1
        st.dataframe(df_lst.loc[:: int(NN)])
        st.markdown(f"*Available Data: {df_lst.loc[::int(NN)].shape[0]}")
        st.download_button(
            label="Download data", data=df_lst.loc[:: int(NN)].to_csv(), mime="text/csv"
        )
    # make the graphs in one function
    make_graphs(df_lst, st)
