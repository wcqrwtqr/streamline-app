import pandas as pd
import streamlit as st
from helpers.handlers.make_graphs import make_graphs, make_graphs_optimized
import time
from concurrent.futures import ThreadPoolExecutor


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

    # OLD METHOD =================================================
    """
    df = pd.read_csv(
        source_file,
        sep="[,\t]",
        header=None,
        skiprows=row,
        names=["date", "time", "pressure", "temperature"],
        # parse_dates={"date_time_corrected": ["date", "time"]},
        # date_parser=lambda x: pd.to_datetime(x, format="%d-%m-%y %H:%M:%S"),
        engine="python",
    )

    df["date_time"] = df["date"] + " " + df["time"]
    df["date_time_corrected"] = pd.to_datetime(
        df["date_time"], format="%d-%m-%y %H:%M:%S"
    )
    """

    # Chunk METHOD START =================================================
    """
    df = pd.DataFrame()

    chunk_generator = pd.read_csv(
        source_file,
        sep="[,\t]",
        header=None,
        skiprows=row,
        names=["date", "time", "pressure", "temperature"],
        chunksize=10000,
        # parse_dates={"date_time_corrected": ["date", "time"]},
        # date_parser=lambda x: pd.to_datetime(x, format="%d-%m-%y %H:%M:%S"),
        engine="python",
    )

    for chunk in chunk_generator:
        # Your processing code here
        # For example, you can concatenate the date and time columns and convert them to datetime
        chunk["date_time_corrected"] = pd.to_datetime(
            chunk["date"] + " " + chunk["time"], format="%d-%m-%y %H:%M:%S"
        )
        df = pd.concat([df, chunk])
    """
    # Chunk METHOD END =================================================

    # concurrent method START =================================================

    """
    """
    chunk_size = 10000  # Specify the chunk size

    # Initialize an empty list to store the processed chunks
    processed_chunks = []

    # Define a generator to iterate over chunks of the CSV file
    chunk_generator = pd.read_csv(
        source_file,
        sep="[,\t]",
        header=None,
        skiprows=row,
        names=["date", "time", "pressure", "temperature"],
        chunksize=chunk_size,  # Specify the chunk size
        engine="python",
    )

    # Function to process each chunk
    def process_chunk(chunk):
        # Your processing code here
        # For example, you can concatenate the date and time columns and convert them to datetime
        chunk["date_time_corrected"] = pd.to_datetime(
            chunk["date"] + " " + chunk["time"],
            format="%d-%m-%y %H:%M:%S",
            # chunk["date"] + " " + chunk["time"],
            # format="ISO8601",
        )

        # Append the processed chunk to the list
        return chunk

    # Process each chunk in parallel using ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        # Submit processing tasks for each chunk and store the futures
        futures = [executor.submit(process_chunk, chunk) for chunk in chunk_generator]
    # Get the results from the futures as they complete
    for future in futures:
        processed_chunks.append(future.result())

    # Concatenate all processed chunks into a single DataFrame
    df = pd.concat(processed_chunks)

    # concurrent method END =================================================

    end_time_loaded = time.time()
    execution_time_loaded = end_time_loaded - start_time

    # st.write(df.head())
    df["time_diff"] = df["date_time_corrected"].diff().dt.seconds
    df["pressure_diff"] = df["pressure"].diff()

    # Calculate the rolling standard deviation for pressure and pressure derivative
    df["1st_derivative"] = (df["pressure_diff"] / df["time_diff"]) * 100
    df["2nd_derivative"] = (df["pressure_diff"].diff() / df["time_diff"]) * 100
    # window_size = 50  # You can adjust the window size as needed
    # df["pressure_std"] = df["pressure"].rolling(window=window_size, min_periods=1).std()
    # df["pressure_derivative_std"] = (
    #     df["1st_derivative"].rolling(window=window_size, min_periods=1).std()
    # )

    end_time_statistics = time.time()
    execution_time_statistics = end_time_statistics - start_time

    st.success(
        f"Done ... Load csv file took {execution_time_loaded:.2f} sec , statistics took {execution_time_statistics:.2f} sec"
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
    # make_graphs(df_lst, st)
    make_graphs_optimized(df_lst, st)
    end_time_graphing = time.time()
    execution_time_graphing = end_time_graphing - start_time
    st.success(
        f"Done ... Draw table took {execution_time_draw:.2f} sec , Graphing took {execution_time_graphing:.2f} sec"
    )
