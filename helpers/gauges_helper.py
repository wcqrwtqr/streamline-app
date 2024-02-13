import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from helpers.graphing import graphing_line_arg


@st.cache_data
def load_df_spartek(source_file, row: int):
    '''This helper funciton to cache the dataframe to memoery so there is no
    extensive computation evey time we change the values

    :param source_file: file path
    :type source_file: string
    :param row: number of rows
    :type row: int

    :returns: df , range_data
    :rtype: dataframe"""

    '''
    df = pd.read_csv(
        source_file,
        sep=r"\s+",
        header=None,
        skiprows=row,
        # names=["date", "time", "AMPM", "elpse", "pressure", "temperature"],
        names=["date", "time", "AMPM", "elpse", "pressure", "temperature"],
        engine="python",
    )
    df["date_time"] = df["date"] + " " + df["time"] + " " + df["AMPM"]
    df["change rate"] = df["pressure"].diff()
    range_data = df.index.tolist()

    return df, range_data


def Gauges_data_Spartek(source_file, row=20):
    """Gauges_data_Spartek.

    Parameters
    ----------
    source_file :
        source_file
    row :
        row
    """
    """Gauges_data_Spartek.

    Parameters
    ----------
    source_file :
        source_file
    row :
        row
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
        st.dataframe(df_lst.loc[:: int(NN)])
        st.markdown(f"*Available Data: {df_lst.loc[::int(NN)].shape[0]}")
        st.download_button(
            label="Download data", data=df_lst.loc[:: int(NN)].to_csv(), mime="text/csv"
        )
    with st.expander(label="Gauges Chart"):
        graphing_line_arg(df_lst, "date_time", st, ["pressure", "temperature"])

    with st.expander(label="Pressure Change Rate"):
        graphing_line_arg(df_lst, "date_time", st, ["pressure", "change rate"])

    # Tried to make a Histogram but did not work
    # with st.expander(label="Pressure Change Rate Histogram"):
    #     fig, ax = plt.subplots()
    #     ax.hist(df['change rate'], bins=1)
    #     ax.set_xlabel('Pressure Change Rate')
    #     ax.set_ylabel('Frequency')
    #     ax.set_title('Histogram of Pressure Change Rates')
    #     st.pyplot(fig)
