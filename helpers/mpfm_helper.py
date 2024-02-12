import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from helpers.graphing import graphing_line_arg


def calculate_averages(df, columns):
    return {column: np.average(df[column]) for column in columns}


def mpfm_data(source_file):
    """MPFM data processing generator

    :param source_file: file path
    :type source_file: string

    :returns: None
    :rtype: None"""

    df = pd.read_csv(source_file, sep="\t")
    df.dropna(inplace=True, axis=1)

    # Masking
    range_data = df.index.tolist()

    # Create a new column combining the date and time
    df["date_time"] = df["Date"] + " " + df["Clock"]
    header_list = df.columns.tolist()
    range_data_selection = st.slider(
        "Range:",
        min_value=min(range_data),
        max_value=max(range_data),
        value=(min(range_data), max(range_data)),
    )

    # Creating the masked df from the index
    expander = st.expander("Data Selection")
    df_header = expander.multiselect("Choose the data for the csv export", header_list, header_list[:-12])

    df_lst = df[range_data_selection[0]: range_data_selection[1]]
    df_lst2 = df_lst[df_header]

    # Averages calculation
    avg_columns = [
        "Pressure",
        "Temperature",
        "dP",
        "Std.OilFlowrate",
        "WaterFlowrate",
        "Std.GasFlowrate",
        "Act.GasFlowrate",
        "GOR(std)",
        "Std.Watercut",
        "OilDensity",
        "WaterDensity",
        "GasDensity",
    ]
    averages = calculate_averages(df_lst, avg_columns)

    avg_liquid = averages["Std.OilFlowrate"] + averages["WaterFlowrate"]
    API = 141.5 / (averages["OilDensity"] / 1000) - 131.5

    start = (
        df_lst["date_time"][range_data_selection[0]] + " " + df_lst["Date"][range_data_selection[0]]
    )
    end = (
        df_lst["date_time"][range_data_selection[1] - 1] + " " + df_lst["Date"][range_data_selection[1] - 1]
    )

    # Making the dataframe
    summary_data = {
        "Start Time": start,
        "End Time": end,
        "WHP": averages["Pressure"],
        "WHT": averages["Temperature"],
        "Diff dP": averages["dP"],
        "Oil Rate": averages["Std.OilFlowrate"],
        "Water Rate": averages["WaterFlowrate"],
        "Liquid Rate": avg_liquid,
        "Gas Rate": averages["Std.GasFlowrate"],
        "Actual Gas Rate": averages["Act.GasFlowrate"],
        "Total GOR": averages["GOR(std)"],
        "Gas SG": averages["GasDensity"],
        "Oil SG": averages["OilDensity"],
        "Oil API": API,
        "BSW": averages["Std.Watercut"],
        "Water SG": averages["WaterDensity"],
    }

    summary = pd.DataFrame([summary_data])
    st.markdown(f"*Available Data: {df_lst2.shape[0]}")
    gas_rate_float = "{:.4f}".format(averages["Std.GasFlowrate"])
    container = st.container(border=True)
    container.write("Averages and Max values")
    container.markdown(
        f"Data Average Values : Oil rate __*{int(averages["Std.OilFlowrate"])}*__ , Gas rate __{gas_rate_float}__ , GOR __{int(averages["GOR(std)"])}__"
    )
    container.markdown(
        f'Data Max Values : Oil rate __{int(df_lst["Std.OilFlowrate"].max())}__ , Gas rate __{df_lst["Std.GasFlowrate"].max()}__ , GOR __{int(df_lst["GOR(std)"].max())}__'
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Pressure vs Dp", "📈 Pressure vs Temp", "📈 Oil vs GOR", "📈 Oil vs Gas vs water", "📈 Water vs BSW"])
    graphing_line_arg(df_lst, "date_time", tab1, ["Pressure", "dP"])
    graphing_line_arg(df_lst, "date_time", tab2, ["Pressure", "Temperature"])
    graphing_line_arg(df_lst, "date_time", tab3, ["Std.OilFlowrate", "GOR(std)"])
    graphing_line_arg(df_lst, "date_time", tab4, ["Std.OilFlowrate", "Std.GasFlowrate", "WaterFlowrate"])
    graphing_line_arg(df_lst, "date_time", tab5, ["WaterFlowrate", "Std.Watercut"])


    # making the average table along with a graph
    with st.expander(label="Average table"):
        avg_selection = st.multiselect("select parameter", header_list[2:-1])
        col6, col7 = st.columns(2)
        if avg_selection != []:
            col6.write("Average table 👇🏼")
        col6.dataframe(df_lst[avg_selection].mean())
        graphing_line_arg(df_lst, "date_time", col6, avg_selection)

    # Showing the data set with the needed columns
    with st.expander(label="Data Set"):
        NN = st.selectbox("Interval", [1, 5, 10, 20, 30])
        st.write("👈🏼 Add/Remove from the sidebar list")
        st.dataframe(df_lst2.loc[:: int(NN)])
        st.markdown(f"*Available Data: {df_lst2.loc[::int(NN)].shape[0]}")

    with st.expander(label="Summary table"):
        st.markdown("Average Table")
        st.dataframe(summary)

    with st.expander(label="Custom Graph"):
        SS = st.multiselect("Select Headers", header_list[2:-2])
        graphing_line_arg(df_lst, "date_time", st, SS)

    with st.expander(label="Correlation"):
        selector = st.multiselect("select one", header_list[2:-2])
        cmp = st.selectbox(
            "select one",
            ["coolwarm", "BuPu", "coolwarm_r", "magma", "magma_r", "tab10"],
        )

        fig, ax = plt.subplots()
        sns.heatmap(df_lst[selector].corr(), cmap=cmp, annot=True, ax=ax)
        st.pyplot(fig)
        st.plotly_chart(fig)
        # fig, ax = plt.subplots()
        # ax = sns.heatmap(df_lst[selector].corr(), cmap=cmp, annot=True)
        # st.pyplot(fig)
        # st.plotly_chart(fig)
