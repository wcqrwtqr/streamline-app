from helpers.handlers.graphing import graphing_line_arg
from helpers.handlers.graphing import graphing_line_2v
import concurrent.futures


# Template for the arg function which accept any number of arguments
# It might have some performance issues when dealing with big data
def graph_template(df, st, label: str, y1: str, y2: str):
    with st.expander(label=label):
        graphing_line_arg(df, "date_time_corrected", st, [y1, y2])


# This function is to use the normal v2 function which is more efficient
def graph_template_v2(df, st, label: str, xval: str, val1: str, val2: str):
    with st.expander(label=label):
        val = graphing_line_2v(df, xval, val1, val2)
        st.plotly_chart(val)


# Make the graphing using the easy graphing_line_v2 function
def make_graphs_optimized(df, st):
    with st.expander(label="Pressure vs Temperature"):
        pressure_vs_temperature = graphing_line_2v(
            df, "date_time_corrected", "pressure", "temperature"
        )
        st.plotly_chart(pressure_vs_temperature)

    with st.expander(label="Pressure vs dp/dt"):
        press_1st = graphing_line_2v(
            df, "date_time_corrected", "pressure", "1st_derivative"
        )
        st.plotly_chart(press_1st)

    # with st.expander(label="Temperature vs dT/dt"):
    #     press_1st = graphing_line_2v(
    #         df, "date_time_corrected", "temperature", "1st_derivative_t"
    #     )
    #     st.plotly_chart(press_1st)


def make_graphs(df, st):
    futures = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit tasks for each graph
        futures.append(
            executor.submit(
                graph_template_v2(
                    df,
                    st,
                    "Pressure vs Temperature",
                    "date_time_corrected",
                    "pressure",
                    "temperature",
                )
            )
        )
        futures.append(
            executor.submit(
                graph_template_v2(
                    df,
                    st,
                    "Pressure vs 1st Derivative",
                    "date_time_corrected",
                    "pressure",
                    "1st_derivative",
                )
            )
        )
        # futures.append(
        #     executor.submit(
        #         graph_template_v2(
        #             df,
        #             st,
        #             "Pressure vs Derivative",
        #             "date_time_corrected",
        #             "pressure",
        #             "derived_pressure",
        #         )
        #     )
        # )

        # --- Using the graphing_line_arg function ##
        # futures.append(
        #     executor.submit(
        #         graph_template(
        #             df, st, "Pressure vs Temperature", "pressure", "temperature"
        #         )
        #     )
        # )
        # futures.append(
        #     executor.submit(
        #         graph_template(
        #             df, st, "Pressure vs 1st Derivative", "pressure", "1st_derivative"
        #         )
        #     )
        # )

    # Wait for all tasks to complete
    # concurrent.futures.wait(futures)
    return futures
