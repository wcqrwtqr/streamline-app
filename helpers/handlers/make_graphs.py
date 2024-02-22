from helpers.handlers.graphing import graphing_line_arg
from helpers.handlers.graphing import graphing_line_2v
import concurrent.futures
import pandas as pd
from typing import Dict
import streamlit as st


# Template for the arg function which accept any number of arguments
# It might have some performance issues when dealing with big data
def graph_template(df: pd.DataFrame, st: st, label: str, y1: str, y2: str):
    with st.expander(label=label):
        graphing_line_arg(df, "date_time_corrected", st, [y1, y2])


# This function is to use the normal v2 function which is more efficient
def graph_template_v2(
    df: pd.DataFrame, st: st, label: str, xval: str, val1: str, val2: str
):
    with st.expander(label=label):
        val = graphing_line_2v(df, xval, val1, val2)
        st.plotly_chart(val)


# List of data to get it graphed
data_to_graphs: list[str] = [
    ["Pressure vs Temperature", "pressure", "temperature"],
    ["Pressure vs dp/dt", "pressure", "1st_derivative"],
]


# Make the graphing using the easy graphing_line_v2 function
def make_graphs_optimized(df: pd.DataFrame, st: st) -> None:
    # Loop over the list of strings and make the graphs
    for data_to_graph in data_to_graphs:
        with st.expander(label=data_to_graph[0]):
            graph = graphing_line_2v(
                df, "date_time_corrected", data_to_graph[1], data_to_graph[2]
            )
            st.plotly_chart(graph)


def make_graphs(df: pd.DataFrame, st: st):
    futures = []

    for data_to_graph in data_to_graphs:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit tasks for each graph
            futures.append(
                executor.submit(
                    graph_template_v2(
                        df,
                        st,
                        data_to_graph[0],
                        "date_time_corrected",
                        data_to_graph[1],
                        data_to_graph[2],
                    )
                )
            )

    # Wait for all tasks to complete
    # concurrent.futures.wait(futures)
    return futures


def data_stats_for_gaguges(df: pd.DataFrame):
    # Create dictionary and fill it with min and max values and
    # create a container with streamlit
    stats: Dict = {
        "Max": {
            "Pressure": df["pressure"].max(),
            "Temperature": df["temperature"].max(),
        },
        "Min": {
            "Pressure": df["pressure"].min(),
            "Temperature": df["temperature"].min(),
        },
    }
    container = st.container(border=True)
    container.write("Max and Min Values")
    container.table(stats)
    container.markdown(f"*Available Data: {df.shape[0]}")
