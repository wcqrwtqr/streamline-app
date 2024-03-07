# import pandas as pd
import streamlit as st

# from typing import Dict, List
from handlers.make_graphs import (
    make_graphs,
    # make_graphs_optimized,
    data_stats_for_gaguges,
)
from handlers.read_csv_gauges import (
    read_csv_standard,
    # read_csv_chunck,
    # read_csv_concurrency,
    compute_statistics_df,
)
import time

# from helpers.handlers.derived_pressure import calc_derivative_np
# from concurrent.futures import ThreadPoolExecutor


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
    start_time = time.time()

    df = read_csv_standard(source_file, row, is_spartek=False)
    # df = read_csv_chunck(source_file, row, is_spartek=False)
    # df = read_csv_concurrency(source_file, row, is_spartek=False)

    end_time_loaded = time.time()
    execution_time_loaded = end_time_loaded - start_time

    # st.write(df.head())
    df = compute_statistics_df(df)

    end_time_statistics = time.time()
    execution_time_statistics = end_time_statistics - start_time

    st.success(
        f"Done ... Load csv file took {execution_time_loaded:.2f} sec , \
        statistics took {execution_time_statistics:.2f} sec"
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

    # Make the stats of min and max in the function below
    data_stats_for_gaguges(df_lst)

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
    # make the graphs in one function
    end_time_draw = time.time()
    execution_time_draw = end_time_draw - start_time
    make_graphs(df_lst, st)
    # make_graphs_optimized(df_lst, st)
    end_time_graphing = time.time()
    execution_time_graphing = end_time_graphing - start_time
    st.success(
        f"Done ... Draw table took {execution_time_draw:.2f} sec , \
            Graphing took {execution_time_graphing:.2f} sec"
    )
