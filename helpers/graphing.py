import plotly.express as px
import streamlit as st
import plotly.graph_objs as go
from plotly.subplots import make_subplots


def graphing_line_arg(df, x, st=st, *args):
    """graphing_line_arg which accept a DataFrame and then can draw
    as much y axes as much using the args option

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
    if arg != []:
        st.plotly_chart(fig_n)
    else:
        None
        st.markdown("Select columns from the drop down list ☝🏼")
