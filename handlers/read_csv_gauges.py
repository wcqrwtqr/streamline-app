import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from typing import Tuple, List

import streamlit as st

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


def compute_statistics_df(df: pd.DataFrame) -> pd.DataFrame:
    # Compute all the statistics data for the dataframe
    df["time_diff"] = df["date_time_corrected"].diff().dt.seconds
    df["pressure_diff"] = df["pressure"].diff()
    df["temperature_diff"] = df["temperature"].diff()
    df["1st_derivative"] = (df["pressure_diff"] / df["time_diff"]) * 100
    return df


def sep_and_names_modified(data_type: str) -> Tuple[str, List[str]]:
    """' This function is needed to select the separation and colum names
    for the type of gauges we use, so in case I want to add a new gauge
    then I can add a new case and add the name of the gauge.
    The function return the separator and column names
    """
    match data_type:
        case "metrolog":
            sep = "[,\t]"
            names = ["date", "time", "pressure", "temperature"]
        case "spartek":
            sep = r"\s+"
            names = ["date", "time", "AMPM", "elpse", "pressure", "temperature"]
        case "kuster":
            sep = (None,)
            names = ["date", "time", "pressure", "temperature"]
        case _:
            raise ValueError(f"Unknown data type: {data_type}")
    return sep, names


def sep_and_names(is_spartek: bool) -> Tuple[str, List[str]]:
    # choose the names of the header in case of metrolog or spartek
    if not is_spartek:
        sep = "[,\t]"
        names = ["date", "time", "pressure", "temperature"]
    else:
        sep = r"\s+"
        names = ["date", "time", "AMPM", "elpse", "pressure", "temperature"]
    return sep, names


def drop_and_make_datetime(df: pd.DataFrame, is_spartek: bool) -> pd.DataFrame:
    """This function is used to take the dataframe, and create the date_time
    column by combine the time and date columns form the type of gauges
    Now, this code support spartek and metrolog only.
    Retrun a dataframe
    """
    if is_spartek:
        df["date_time"] = df["date"] + " " + df["time"] + " " + df["AMPM"]
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
        df = df.drop(columns=["date", "time", "AMPM", "date_time"])
    else:
        df["date_time"] = df["date"] + " " + df["time"]
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
        df = df.drop(columns=["date", "time", "date_time"])
    return df


def read_csv_standard(source_file: str, row: int, is_spartek=False) -> pd.DataFrame:
    """This code used to load the data fro the spartek and metrolog
    only but can not be used for other guagues like kuster, so I made
    another code for kuster gauges alone
    Retruns dataframe
    """
    sep, names = sep_and_names(is_spartek)
    df = pd.read_csv(
        source_file,
        skiprows=row,
        header=None,
        sep=sep,
        names=names,
        engine="python",
    )
    df = drop_and_make_datetime(df, is_spartek)
    return df


def read_csv_standard_kuster(source_file: str, row: int, kind: str) -> pd.DataFrame:
    "I've added the third option of kuster so I modified the sep_name"
    sep, names = sep_and_names_modified("kuster")
    df = pd.read_csv(
        source_file,
        skiprows=row,
        header=None,
        sep=sep,
        names=names,
        engine="python",
    )
    st.write(df.head())
    # df = drop_and_make_datetime(df, is_spartek=False)
    df["date_time"] = df["date"] + " " + df["time"]
    return df


# The below code I've made earlier so I can be able to load data
# with big/huge numbers so it can use better and efficent loading
# of data, but later I did not use it.


def read_csv_chunck(
    source_file: str, row: int, is_spartek=False, chunk_size=10_000
) -> pd.DataFrame:
    sep, names = sep_and_names(is_spartek)
    df = pd.DataFrame()
    chunk_generator = pd.read_csv(
        source_file,
        skiprows=row,
        header=None,
        sep=sep,
        names=names,
        chunksize=chunk_size,
        engine="python",
    )

    for chunk in chunk_generator:
        # Your processing code here
        # For example, you can concatenate the date and time columns and
        # convert them to datetime
        if not is_spartek:
            chunk["date_time_corrected"] = pd.to_datetime(
                chunk["date"] + " " + chunk["time"], format="%d-%m-%y %H:%M:%S"
            )
            df = pd.concat([df, chunk])
        else:
            chunk["date_time_corrected"] = pd.to_datetime(
                chunk["date"] + " " + chunk["time"] + " " + chunk["AMPM"],
                format="%d-%b-%y %I:%M:%S %p",
            )
            df = pd.concat([df, chunk])

    df = drop_and_make_datetime(df, is_spartek)

    return df


def read_csv_concurrency(
    source_file: str, row: int, is_spartek=False, chunk_size=10_000
) -> pd.DataFrame:
    chunk_size = chunk_size  # Specify the chunk size
    sep, names = sep_and_names(is_spartek)

    # Initialize an empty list to store the processed chunks
    processed_chunks = []

    # Define a generator to iterate over chunks of the CSV file
    chunk_generator = pd.read_csv(
        source_file,
        skiprows=row,
        sep=sep,
        header=None,
        names=names,
        chunksize=chunk_size,
        engine="python",
    )

    # Function to process each chunk
    def process_chunk(chunk):
        # Your processing code here
        # For example, you can concatenate the date and time columns and
        # convert them to datetime
        if not is_spartek:
            chunk["date_time_corrected"] = pd.to_datetime(
                chunk["date"] + " " + chunk["time"],
                format="%d-%m-%y %H:%M:%S",
            )
        else:
            chunk["date_time_corrected"] = pd.to_datetime(
                chunk["date"] + " " + chunk["time"] + " " + chunk["AMPM"],
                format="%d-%b-%y %I:%M:%S %p",
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
    return df
