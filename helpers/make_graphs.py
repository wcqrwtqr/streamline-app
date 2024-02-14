from helpers.graphing import graphing_line_arg


def make_graphs(df, st):
    with st.expander(label="Gauges Chart"):
        graphing_line_arg(df, "date_time_corrected", st, ["pressure", "temperature"])

    with st.expander(label="Pressure 1st Derivative"):
        graphing_line_arg(df, "date_time_corrected", st, ["pressure", "1st_derivative"])

    with st.expander(label="Pressure 2nd Derivative"):
        graphing_line_arg(df, "date_time_corrected", st, ["pressure", "2nd_derivative"])

    with st.expander(label="Pressure 1st & 2nd Derivative"):
        graphing_line_arg(
            df,
            "date_time_corrected",
            st,
            ["1st_derivative", "pressure", "2nd_derivative"],
        )

    with st.expander(label="Pressure standard deviations"):
        graphing_line_arg(df, "date_time_corrected", st, ["pressure", "pressure_std"])

    # with st.expander(label="Pressure Derevative"):
    #     graphing_line_arg(
    #         df, "date_time_corrected", st, ["pressure", "pressure_derivative_std"]
    #     )
