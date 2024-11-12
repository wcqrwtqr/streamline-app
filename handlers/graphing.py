import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots


def graphing_line_arg(df: pd.DataFrame, x: str, st=st, *args):
    """Old code I made to make the graphing of the data with args\
    so I can add as much as I want of graph values from the DataFrame."""
    for arg in args:
        fig_n = make_subplots(specs=[[{"secondary_y": True}]])
        my_string = " , ".join(arg) + " Graph"
        # Added this line using GPT to add a hover line and read the vlaues
        # Remove it if there is an issue in future
        fig_n.update_layout(
            title_text=my_string,
            hovermode="x unified",  # Enables crosshair line for hover
        )
        # fig_n.update_layout(title_text=my_string)
        fig_n.update_xaxes(title_text=x)
        for idx, col in enumerate(arg):
            bol = idx % 2 == 1  # Get the 1st or secondary acxes
            fig_n.update_yaxes(title_text=col, secondary_y=bol)
            fig_n.add_trace(
                go.Scatter(x=df[x], y=df[col], mode="lines", name=col), secondary_y=bol
            )
        if arg:
            st.plotly_chart(fig_n)
        else:
            st.markdown("Select columns from the drop down list ☝🏼")


def graphing_line_2v(df: pd.DataFrame, x: str, ym: str, ys: str):
    """Graphing code that can graph the values from the DataFrame\
    for two axes only and can by used and called serveral time as\
    much as you need."""
    xt = df[x]
    yp = df[ym]
    yt = df[ys]
    # Making the graph for the two values
    fig_n = make_subplots(specs=[[{"secondary_y": True}]])
    # Added below update_layout to see if I can add the hover in the graph
    # It worked nicely :)
    fig_n.update_layout(
        title_text=f"{ym} and {ys} Graph",
        hovermode="x unified",  # Enables crosshair line for hover
    )
    fig_n.update_layout(title_text=ym + " " + ys + " " + "Graph")
    fig_n.update_xaxes(title_text=x)
    fig_n.update_yaxes(title_text=ym, secondary_y=False)
    fig_n.update_yaxes(title_text=ys, secondary_y=True)
    fig_n.add_trace(go.Scatter(x=xt, y=yp, mode="lines",
                    name=ym), secondary_y=False)
    fig_n.add_trace(go.Scatter(x=xt, y=yt, mode="lines",
                    name=ys), secondary_y=True)

    return fig_n
