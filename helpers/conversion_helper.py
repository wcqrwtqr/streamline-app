import streamlit as st
from typing import Dict


def bbl_to_other_units(bbl: int) -> Dict[str, float]:
    gpm = bbl / 34.285
    lpm = bbl / 9.043
    cmh = bbl / 150.72
    cmd = bbl / 6.28
    result = {"gpm": gpm, "l/min": lpm, "Cubic meter/h": cmh, "Cubic meter/d": cmd}
    return result


def conversion_helper():
    with st.expander("BBL/d to other units"):
        with st.form(key="bbl to other units"):
            col1, _ = st.columns(2)
            bbl = int(
                col1.number_input(
                    "bbl/d",
                    500,
                    step=200,
                )
            )
            submit = st.form_submit_button(label="Submit")
            if submit:
                result = bbl_to_other_units(bbl)
                st.table(result)
