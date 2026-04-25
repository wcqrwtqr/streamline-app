import streamlit as st
import pandas as pd
import numpy as np
from typing import List, Tuple
import plotly.graph_objs as go
from plotly.subplots import make_subplots


def regression(x: int, y: int) -> Tuple[int, int]:
    """
    Calculate the straing line regression so \
    we can use it as an input for the horner plot.

    Retrun the two values of the slope and the intercept \
    the intercept is the pi* inial pressure
    """
    n = np.size(x)
    # mean of x and y vector
    m_x, m_y = np.mean(x), np.mean(y)
    # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y * x) - n * m_y * m_x
    SS_xx = np.sum(x * x) - n * m_x * m_x
    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1 * m_x

    return (b_0, b_1)


@st.cache_data
def load_df_horner(source_file: str) -> Tuple[pd.DataFrame, List[int]]:
    """
    Load the csv file data in elapse time and pressure only and output the \
    dataframe and a list.

    Return data is a tuple of dataframe and list.
    """
    try:
        df = pd.read_csv(
            source_file,
            sep=",",
            header=None,
            skiprows=15,
            names=["Hours", "Pressure", "Delete"],
            encoding_errors="ignore",  # pandas ≥ 1.4
            encoding="utf-8",
        )
    except Exception as e:
        st.write("Error loading the file - ensure using the correct file\n" + str(e))
    df = df.drop(columns=["Delete"])
    range_data = df.index.tolist()
    return df, range_data


def Horner_plot_data(source_file):
    """
    Load the dataframe from the previous function and draw the horner\
    plot in the streamlit.

    Accept the csv file and generate the plots.
    """
    # Load data to df
    df, range_data = load_df_horner(source_file)
    range_data_selection = st.slider(
        "Range:",
        min_value=min(range_data),
        max_value=max(range_data),
        value=(min(range_data), max(range_data)),
    )
    df_lst = df[range_data_selection[0]: range_data_selection[1]]
    with st.expander(label="Table of Data"):
        NN = st.selectbox("Interval", [1, 2, 5, 10, 25, 50, 100])
        if NN is None:  # This code is to address int|None condition
            NN = 1
        st.dataframe(df_lst.loc[:: int(NN)])
        st.markdown(f"*Available Data: {df_lst.loc[:: int(NN)].shape[0]}")
        st.download_button(
            label="Download data", data=df_lst.loc[:: int(NN)].to_csv(), mime="csv"
        )

    with st.expander(label="Pressure plot"):
        graph = graphing_horner_1v(
            df_lst,
            "Hours",
            "Pressure",
            title="Pressure Buildup Profile Over Time",
            x_label="Time(Hourse)",
            y_label="Pressure(psi)",
        )
        st.plotly_chart(graph)

    with st.expander(label="Horner Plot"):
        # st.write(
        #     f"bugging - value of Hours[0] = {df_lst.Hours[range_data_selection[0]]}"
        # )
        # delta_t = df_lst.Hours - df_lst.Hours[0]
        delta_t = df_lst.Hours - df_lst.Hours[range_data_selection[0]]
        x_horner = np.log10((24 + delta_t) / delta_t)
        horner = pd.DataFrame(
            {
                "Time(hour)": df_lst.Hours,
                "logtime": x_horner,
                "Shut-in pressure(psia)": df.Pressure,
            }
        )
        # Graph the new horner plot after update dataframe
        with st.form(key="Horner_form"):
            col1, col2, col3 = st.columns(3)
            # index5 = 15_000
            index5 = col1.number_input(label="index", step=100, value=15000)
            q = col2.number_input(label="Oil Rate Q", step=100, value=2000)
            pwf = col3.number_input(
                label="pwf", step=10, value=3200
            )  # in psia, flowing pressure
            # the well is flowed for 24 hours, then shut-in for another
            # 24 hours (24-hour buildup)
            tp = col1.number_input(label="Shutin hours", step=1, value=12)
            poro = col1.number_input(label="Porosity", step=0.1, value=0.28)
            rw = col3.number_input(label="rw", step=0.1, value=0.40)
            h = col2.number_input(label="h", step=0.1, value=0.40)
            ct = 9e-06  # in psi^-1
            pi = col3.number_input(
                label="pi", step=100, value=3500
            )  # 86  # in ft3700  # initial pressure in psia
            mu_oil = 1  # in cP
            Bo = col2.number_input(
                label="Bo", step=0.1, value=1.20
            )  # 1.121  # in RB/STB
            re = np.inf  # reservoir is infinity in size
            # cut dataframe from index 0 to index of end of straight line
            dfhorner = horner.iloc[index5:, :]
            # linear regression to find slope and intercept of a straight line
            x5 = dfhorner.iloc[:, 1]
            y5 = dfhorner.iloc[:, 2]
            c5, m5 = regression(x5, y5)
            pi = c5  # initial pressure equals to intercept c5
            # calculate permeability
            k = -(162.6 * q * Bo * mu_oil) / (m5 * h)
            # calculate skin factor
            # determine b1hr: pressure value at t = 1 hour, in psia
            b1hr = c5 + m5 * np.log10(tp + 1)
            s = 1.1513 * (
                ((pwf - b1hr) / m5)
                - np.log10(k / (poro * mu_oil * ct * (rw**2)))
                + 3.2275
            )
            # Calculate pressure drop due to well damage
            delta_ps = ((141.2 * q * Bo * mu_oil) / (k * h)) * s
            delta_p_shutin = pi - df.Pressure[range_data_selection[0]]
            # st.write(
            #     f"bug old {df.Pressure[0]} against {df.Pressure[range_data_selection[0]]}"
            # )
            # delta_p_shutin = pi - df.Pressure[0]
            wellskin_contribution = (delta_ps / delta_p_shutin) * 100
            formation_drop = delta_p_shutin - delta_ps
            formation_contribution = 100 - wellskin_contribution
            # Calcualte the straight line for the horner plot
            graph = graphing_horner_1v(
                horner,
                "logtime",
                "Shut-in pressure(psia)",
                title="Complete Horner Build Plot",
                x_label="Log((tp+delta_t)/delte_t)",
                y_label="Shut-in pressure, pws (psi)",
                index5=index5,
                m5=m5,
                c5=c5,
            )

            submit = st.form_submit_button(label="Submit")
            if submit:
                st.plotly_chart(graph)
                st.write("Slope of linear-region Horner plot:", m5)
                st.write("Intercept of linear-region Horner plot:", c5, "psia")
                st.write(
                    "The initial reservoir pressure equals to the intercept:",
                    pi,
                    "psia",
                )
                st.write("Skin factor:", s)
                st.write("Pressure drop due to well skin:", delta_ps, "psia")
                st.write("Pressure drop before shut-in:",
                         delta_p_shutin, "psia")
                st.write(
                    "Well damage contribute to:",
                    wellskin_contribution,
                    "% of total pressure drop",
                )
                st.write(
                    "End of wellbore-storage period occurs approximately at:",
                    df.Hours[index5],
                    "hour",
                )
                st.write(
                    "Reservoir formation contribute to:",
                    formation_drop,
                    "psia of the total pressure drop,\nor in percent:",
                    formation_contribution,
                    "% of total pressure drop",
                )


def graphing_horner_1v(
    df: pd.DataFrame,
    x: str,
    ym: str,
    title: str,
    x_label: str,
    y_label: str,
    index5: int | None = None,
    m5: float | None = None,
    c5: float | None = None,
):
    """
    Graphing code that can graph the values from the DataFrame \
    for two axes only and can by used and called several times as \
    much as you need.

    This function was modifed to add the ability to make a star at \
    a given point.

    This function is only for the Horner plot only.
    """
    xt = df[x]
    yp = df[ym]

    fig_n = make_subplots(specs=[[{"secondary_y": True}]])

    fig_n.update_layout(
        title_text=title,
        hovermode="x unified",
        height=600,
    )
    fig_n.update_xaxes(title_text=x_label)
    fig_n.update_yaxes(title_text=y_label)

    # Main line
    fig_n.add_trace(
        go.Scatter(
            x=xt,
            y=yp,
            mode="lines",
            name=ym,
        )
    )

    # Optional red star marker at a specific point
    if index5 is not None:
        fig_n.add_trace(
            go.Scatter(
                x=[df[x].iloc[index5]],
                y=[df[ym].iloc[index5]],
                mode="markers",
                name="end of linear region",
                marker=dict(
                    symbol="star",  # or "asterisk"
                    color="red",
                    size=12,
                ),
            )
        )
        # 2) Regression / straight line segment using m5 and c5
        if m5 is not None and c5 is not None:
            # Equivalent to:
            # x_cut = horner.drop(horner.index[0])
            # x_reg5 = x_cut.iloc[:, 1]
            # y_reg5 = m5 * x_reg5 + c5
            x_cut = df.drop(df.index[0])
            x_reg5 = x_cut.iloc[:, 1]  # second column, like your code
            y_reg5 = m5 * x_reg5 + c5

            fig_n.add_trace(
                go.Scatter(
                    x=x_reg5,
                    y=y_reg5,
                    mode="lines",
                    name="reg line",
                    line=dict(color="orange", width=2),
                    showlegend=True,
                )
            )

    return fig_n
