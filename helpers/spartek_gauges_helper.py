import streamlit as st
import pandas as pd
from typing import List, Tuple
from helpers.handlers.make_graphs import (
    make_graphs,
    make_graphs_optimized,
    data_stats_for_gaguges,
)
from helpers.handlers.read_csv_gauges import (
    read_csv_standard,
    read_csv_chunck,
    read_csv_concurrency,
    compute_statistics_df,
    # get_sgs_data,
    # get_sgs_data_std,
)
import time


@st.cache_data
def load_df_spartek(source_file: str, row: int) -> Tuple[pd.DataFrame, List[int]]:
    start_time = time.time()

    df = read_csv_standard(source_file, row, is_spartek=True)
    # df = read_csv_chunck(source_file, row, is_spartek=True)
    # df = read_csv_concurrency(source_file, row, is_spartek=True)

    end_time_loaded = time.time()
    execution_time_loaded = end_time_loaded - start_time

    df = compute_statistics_df(df)

    end_time_statistics = time.time()
    execution_time_statistics = end_time_statistics - end_time_loaded

    st.success(
        f"Done ... Load csv file took {execution_time_loaded:.2f} sec ,\
              statistics took {execution_time_statistics:.2f} sec"
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

    end_time_draw = time.time()
    execution_time_draw = end_time_draw - start_time

    make_graphs(df_lst, st)
    # make_graphs_optimized(df_lst, st)

    # sgs_df = get_sgs_data(df_lst)
    # with st.expander("SGS"):
    #     with st.form(key="Get Gradient Data"):
    #         col1, col2 = st.columns(2)
    #         threshold = col1.number_input("threshold", step=0.0001)
    #         no_steps = int(col2.number_input("No of steps", 10))
    #         submit = st.form_submit_button(label="Get SGS Data")
    #         if submit:
    #             sgs_df_std, sgs_size = get_sgs_data_std(
    #                 df_lst, threshold=threshold, no_steps=no_steps
    #             )
    #             st.write(f"No of points {sgs_size}")
    #             st.table(sgs_df_std)

    # sgs_df_std, sgs_size = get_sgs_data_std(df_lst, threshold=0.00001, no_steps=10)
    # st.table(sgs_df_std.head())
    # st.write(f"size{sgs_size}")
    # st.table(sgs_df_std.describe())

    # with st.expander(label="SGS"):
    #     sgs_df = get_sgs_data(df_lst)
    #     st.table(sgs_df)

    end_time_graphing = time.time()
    execution_time_graphing = end_time_graphing - start_time
    st.success(
        f"Done ... Draw table took {execution_time_draw:.2f} sec ,\
              Graphing took {execution_time_graphing:.2f} sec"
    )
