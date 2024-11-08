import streamlit as st
import lasio
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")


def graphing_las_log_arg(df: pd.DataFrame, st=st, *args):
    """
    Make graph for the las file with all the data to be graphed by selecting
    the all the needed columns
    """
    for arg in args:
        # Create a subplot with secondary y-axis (for depth/time)
        fig_n = make_subplots(specs=[[{"secondary_y": True}]])

        my_string = " , ".join(arg) + " Plot"
        fig_n.update_layout(title_text=my_string)
        # Adjust the height of the plot
        fig_n.update_layout(title_text=my_string, height=1200)

        # Set the y-axis to represent time (or depth)
        # Reverse the y-axis for depth/time
        fig_n.update_yaxes(title_text="TIME", autorange="reversed")

        for idx, col in enumerate(arg):
            # secondary = idx % 2 == 1  # Determine if it's a secondary
            # axis or not

            # Add the trace with x and y flipped for a vertical plot
            fig_n.add_trace(
                go.Scatter(x=df[col], y=df.index, mode="lines", name=col),
                # secondary_y=secondary  # Assign to primary or secondary
                # y-axis
            )
            # Set x-axis titles based on the column being plotted
            fig_n.update_xaxes(title_text=col)  # For primary x-axis
            # if not secondary:
            #     fig_n.update_xaxes(title_text=col, row=1, col=1)  # For primary x-axis
            #     # fig_n.update_xaxes(title_text=col)  # For primary x-axis
            # else:
            #     fig_n.update_xaxes(title_text=col, row=1, col=1)  # For secondary x-axis
            #     # fig_n.update_xaxes(title_text=col)  # For secondary x-axis

        if arg:
            st.plotly_chart(fig_n)
        else:
            st.markdown("Select columns from the drop-down list ☝🏼")


@st.cache_data
def load_df_las(source_file):
    """
    Load the las file to dataframe
    using lasio
    """
    las = lasio.read(source_file)
    df = las.df()
    range_data = df.index.tolist()
    las_columns = df.columns

    return df, range_data, las_columns


def graph_las_data(source_file):
    """
    This function accept the las file and make the streamlit
    calculcation
    """
    df, range_data, las_columns = load_df_las(source_file)
    range_data_selection = st.slider(
        "Range:",
        min_value=min(range_data),
        max_value=max(range_data),
        value=(min(range_data), max(range_data)),
    )
    # Creating the masked df from the index
    df_lst = df[range_data_selection[0]: range_data_selection[1]]
    with st.expander(label="Averages"):
        st.table(df_lst.mean().sort_values(ascending=False))

    with st.expander(label="Graph las file"):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            columns_selector = st.multiselect("select header 1", las_columns)
            graphing_las_log_arg(df_lst, st, columns_selector)
        with col2:
            columns_selector = st.multiselect("select header 2", las_columns)
            graphing_las_log_arg(df_lst, st, columns_selector)
        with col3:
            columns_selector = st.multiselect("select header 3", las_columns)
            graphing_las_log_arg(df_lst, st, columns_selector)
        with col4:
            columns_selector = st.multiselect("select header 4", las_columns)
            graphing_las_log_arg(df_lst, st, columns_selector)

    with st.expander(label="Table of las data"):
        st.dataframe(df_lst)
