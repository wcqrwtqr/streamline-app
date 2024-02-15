from helpers.handlers.graphing import graphing_line_arg
import concurrent.futures


def graph_template(df, st, label: str, y1: str, y2: str):
    with st.expander(label=label):
        graphing_line_arg(df, "date_time_corrected", st, [y1, y2])


def make_graphs(df, st):
    futures = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit tasks for each graph

        futures.append(
            executor.submit(
                graph_template(
                    df, st, "Pressure vs Temperature", "pressure", "temperature"
                )
            )
        )
        futures.append(
            executor.submit(
                graph_template(
                    df, st, "Pressure vs 1st Derivative", "pressure", "1st_derivative"
                )
            )
        )

    # Wait for all tasks to complete
    concurrent.futures.wait(futures)
    # return futures
