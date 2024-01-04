import streamlit as st
import plotly.express as px

"""
This module help calculate the air/oil ratio for the burning process
"""


def convert_api_and_oil_rate_to_ton(api, oil):
    "This function will convert the data"
    if api != 0.0:
        x_api = 1000 * (141.5 / (api + 131.5))
        x_ton = x_api * (oil / 6.29) / 1000
    return x_ton


def convert_air_suupply_to_ton(air):
    "This function convert the air supply to ton"
    x_ton = air * 60 * 24 / 35.3147 * 1.225 / 1000
    return x_ton


def calculate_the_values_of_air(API_val, air_rate, oil_rate):
    # Check if the values are no zero
    conv_oil = convert_api_and_oil_rate_to_ton(API_val, oil_rate)
    conv_air = convert_air_suupply_to_ton(air_rate)

    if conv_oil != 0:
        air_oil_ratio = conv_air / conv_oil * 100

        if air_oil_ratio <= 10:
            data = {
                "Oil rate bpd": oil_rate,
                "Air rate CFM": air_rate,
                "Air ratio %": f"{air_oil_ratio:.2f}",
                "Status": "🔻",
                "Comment": "Under size",
            }
            return air_oil_ratio, data
        elif air_oil_ratio >= 10 and air_oil_ratio <= 20:
            data = {
                "Oil rate bpd": oil_rate,
                "Air rate CFM": air_rate,
                "Air ratio %": f"{air_oil_ratio:.2f}",
                "Status": "✅",
                "Comment": "Suitable size",
            }
            return air_oil_ratio, data
        else:
            data = {
                "Oil rate bpd": oil_rate,
                "Air rate CFM": air_rate,
                "Air ratio %": f"{air_oil_ratio:.2f}",
                "Status": "🔺",
                "Comment": "Over size",
            }
            return air_oil_ratio, data


def air_compressor_helper():
    with st.form(key="file_form"):
        col1, col2, col3 = st.columns(3)
        API_val = col1.number_input(label="API", step=0.5, value=25.5)
        oil_rate = col2.number_input(label="Oil Rate", step=100, value=2500)
        air_rate = col3.number_input(label="Air Rate", step=100, value=200)
        submit = st.form_submit_button(label="Submit")
        if submit:
            y = []
            xy = []
            lis_x = list(range(200, 3200, 200))
            data_collection = []
            for rate in range(len(lis_x)):
                new_air_rate = air_rate + lis_x[rate]
                x, data = calculate_the_values_of_air(API_val, new_air_rate, oil_rate)
                y.append(x)
                xy.append(new_air_rate)
                data_collection.append(data)
            st.table(data_collection)
            fig = px.scatter(x=xy, y=y, title="Air oil Ratio for optimum burning")
            fig.add_hrect(y0=10, y1=20, line_width=0, fillcolor="green", opacity=0.1)
            st.plotly_chart(fig)
