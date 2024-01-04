import streamlit as st
import simpy
from helpers.simulation_functions import (
    setup,
    main_list,
    clear_main_list,
    filter_main_list,
)


def simulation_helper():
    with st.form(key="simulation_form"):
        col1, col2, col3, col4 = st.columns(4)
        no_stations = int(col1.number_input("loading stations", 1))
        loading_time = int(col2.number_input("Loading time in minutes", 30, step=5))
        no_trucks = int(col3.number_input("No of trucks", 1))
        duration = int(col4.selectbox("Loading time in hours", [12, 24]))
        submit = st.form_submit_button(label="Submit")
        if submit:
            env = simpy.Environment()
            env.process(setup(env, no_stations, loading_time, 10, no_trucks))
            env.run(until=duration * 60)
            container = st.container(border=True)
            container.write(
                f"In the past {duration} hours **{filter_main_list(main_list)}** \
                trucks were filled"
            )
            st.table(main_list)
            clear_main_list()
