import streamlit as st
import pandas as pd
from typing import List, Tuple
from handlers.make_graphs import (
    make_graphs,
    data_stats_for_gaguges,
)
from handlers.read_csv_gauges import (
    compute_statistics_df,
)
import time

date_formats_all_options = [
    "%m-%d-%y %H:%M:%S",
    "%m-%d-%Y %H:%M:%S",
    "%m/%d/%y %H:%M:%S",
    "%m/%d/%Y %H:%M:%S",
    "%d-%m-%y %H:%M:%S",
    "%d-%m-%Y %H:%M:%S",
    "%d/%m/%y %H:%M:%S",
    "%d/%m/%Y %H:%M:%S",
    "%d-%b-%y %H:%M:%S",
    "%d-%b-%Y %H:%M:%S",
    "%d/%b/%y %H:%M:%S",
    "%d/%b/%Y %H:%M:%S",
    "%b/%d/%y %H:%M:%S",
    "%b/%d/%Y %H:%M:%S",
    "%b-%d-%y %H:%M:%S",
    "%b-%d-%Y %H:%M:%S",
    "%d-%b-%y %I:%M:%S %p",
    "%m-%d-%Y %I:%M:%S %p",
    "%m/%d/%Y %I:%M:%S %p",
    "%d/%m/%Y %I:%M:%S %p",
    "%d-%m-%Y %I:%M:%S %p",
    "%d/%b/%y %I:%M:%S %p",
]


def row_counting(source_file: str) -> int:
    row_count: int = 0
    with open(source_file, "r") as f:
        for line in f:
            row_count += 1
    return row_count


@st.cache_data
def load_df_kuster(source_file: str, row: int) -> Tuple[pd.DataFrame, List[int]]:
    # Reading the source file of the kuster txt file and load it to the pdf
    # DataFrame a and hand it to the next code
    start_time = time.time()

    df = pd.read_csv(
        source_file,
        skiprows=row,
        header=None,
        sep=r"\s+",
        names=["date", "time", "pressure", "temperature"],
        engine="python",
    )
    df["date_time"] = df["date"] + " " + df["time"]
    # Searching all possible options of the date_formats
    # for date_format in date_formats:
    for date_format in date_formats_all_options:
        try:
            df["date_time_corrected"] = pd.to_datetime(
                df["date_time"],
                format=date_format,
            )
            # If parsing succeeds, break out of the loop
            break
        except ValueError:
            # If parsing fails, try the next format
            continue
    df = df.drop(columns=["date_time"])
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


def Gauges_data_kuster(source_file, row=20):
    """
    This function accept the txt file and make the streamlit
    graph for kuster gauges data
    """
    # Load data to df
    df, range_data = load_df_kuster(source_file, row)
    range_data_selection = st.slider(
        "Range:",
        min_value=min(range_data),
        max_value=max(range_data),
        value=(min(range_data), max(range_data)),
    )
    # Creating the masked df from the index
    df_lst = df[range_data_selection[0] : range_data_selection[1]]
    # Make the stats of min and max in the function below
    with st.expander(label="Stats of Gauge Values"):
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
    end_time_graphing = time.time()
    execution_time_graphing = end_time_graphing - start_time
    st.success(
        f"Done ... Draw table took {execution_time_draw:.2f} sec ,\
              Graphing took {execution_time_graphing:.2f} sec"
    )
