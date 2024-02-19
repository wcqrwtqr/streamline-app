import streamlit as st
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio


def graphing_line_arg(df, x, st=st, *args):
    """graphing_line_arg is provided that takes in a DataFrame and allows for the drawing of multiple y axes through the use of the `args` argument. This feature enables you to create as many y axes as needed. Without quotes.
    Parameters
    ----------
    df : DataFrame
        pandas Data Frame
    x : DataFrame Series
        choose the x axis from the data frame
    st :
        streamlit instance
    args :
        args of the y axes as much as you have
    """

    for arg in args:
        fig_n = make_subplots(specs=[[{"secondary_y": True}]])
        my_string = " , ".join(arg) + " Graph"
        fig_n.update_layout(title_text=my_string)
        fig_n.update_xaxes(title_text=x)
        for idx, col in enumerate(arg):
            bol = idx % 2 == 1
            fig_n.update_yaxes(title_text=col, secondary_y=bol)
            fig_n.add_trace(
                go.Scatter(x=df[x], y=df[col], mode="lines", name=col), secondary_y=bol
            )
        if arg:
            st.plotly_chart(fig_n)
        else:
            st.markdown("Select columns from the drop down list ☝🏼")


def graphing_line_2v(df, x: str, ym: str, ys: str):
    """Graphing function for two axis

    :param df: Dataframe
    :type df: string
    :param x: Dataframe for axis x
    :type x: string
    :param ym: Dataframe for axis y primary
    :type ym: string
    :param ys: Dataframe for axis y secondary
    :type ys: string

    :returns: graph object
    :rtype: figure"""

    xt = df[x]
    yp = df[ym]
    yt = df[ys]
    # Making the graph for the two values
    fig_n = make_subplots(specs=[[{"secondary_y": True}]])
    fig_n.update_layout(title_text=ym + " " + ys + " " + "Graph")
    fig_n.update_xaxes(title_text=x)
    fig_n.update_yaxes(title_text=ym, secondary_y=False)
    fig_n.update_yaxes(title_text=ys, secondary_y=True)
    fig_n.add_trace(go.Scatter(x=xt, y=yp, mode="lines", name=ym), secondary_y=False)
    fig_n.add_trace(go.Scatter(x=xt, y=yt, mode="lines", name=ys), secondary_y=True)
    # img = generate_image_from_plotly_graph(graph)
    # return fig_n, img
    return fig_n


def graphing_line_3v(df, x: str, ym: str, ys: str):
    """Graphing function for two axis

    :param df: Dataframe
    :type df: string
    :param x: Dataframe for axis x
    :type x: string
    :param ym: Dataframe for axis y primary
    :type ym: string
    :param ys: Dataframe for axis y secondary
    :returns: graph object
    :rtype: figure"""

    xt = df[x]
    yp = df[ym]
    yt = df[ys]
    # Making the graph for the two values
    fig_n = make_subplots(specs=[[{"secondary_y": True}]])
    fig_n.update_layout(title_text=ym + " " + ys + " " + "Graph")
    fig_n.update_xaxes(title_text=x)
    fig_n.update_yaxes(title_text=ym, secondary_y=False)
    fig_n.update_yaxes(title_text=ys, secondary_y=True)
    fig_n.add_trace(go.Scatter(x=xt, y=yp, mode="lines", name=ym), secondary_y=False)
    fig_n.add_trace(go.Scatter(x=xt, y=yt, mode="lines", name=ys), secondary_y=True)
    image_bytes = pio.to_image(fig_n, format="png")
    return fig_n, image_bytes
