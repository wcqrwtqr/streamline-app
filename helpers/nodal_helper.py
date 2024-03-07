import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from handlers.nodal_functions import aof, j, qo_t, j_darcy, sg_avg
from handlers.nodal_functions import (
    qo_ipr_compuesto,
    Qb,
    qo_vogel,
    qo_darcy,
    gradient_avg,
    f_darcy,
    pwf_darcy,
    pwf_vogel,
)
import streamlit as st


def IPR_curve(q_test, pwf_test, pr, pwf: list, pb):
    # Creating Dataframe
    df = pd.DataFrame()
    df["Pwf(psia)"] = pwf
    df["Qo(bpd)"] = df["Pwf(psia)"].apply(
        lambda x: qo_ipr_compuesto(q_test, pwf_test, pr, x, pb)
    )
    fig, ax = plt.subplots(figsize=(10, 10))
    x = df["Qo(bpd)"]
    y = df["Pwf(psia)"]
    # The following steps are used to smooth the curve
    X_Y_Spline = make_interp_spline(x, y)
    X_ = np.linspace(x.min(), x.max(), 500)
    Y_ = X_Y_Spline(X_)
    # Build the curve
    ax.plot(X_, Y_, c="g")
    ax.set_xlabel("Qo(bpd)", fontsize=14)
    ax.set_ylabel("Pwf(psia)", fontsize=14)
    ax.set_title("IPR", fontsize=18)
    ax.set(xlim=(0, df["Qo(bpd)"].max() + 10), ylim=(0, df["Pwf(psia)"][0] + 100))
    # Arrow and Annotations
    plt.annotate(
        "Bubble Point",
        xy=(Qb(q_test, pwf_test, pr, pb), pb),
        xytext=(Qb(q_test, pwf_test, pr, pb) + 100, pb + 100),
        arrowprops=dict(arrowstyle="->", lw=1),
    )
    # Horizontal and Vertical lines at bubble point
    plt.axhline(y=pb, color="r", linestyle="--")
    plt.axvline(x=Qb(q_test, pwf_test, pr, pb), color="r", linestyle="--")
    ax.grid()
    st.pyplot(fig)
    # plt.show()


# IPR Curve
def IPR_curve_methods(q_test, pwf_test, pr, pwf: list, pb, method, ef=1, ef2=None):
    # Creating Dataframe
    fig, ax = plt.subplots(figsize=(20, 10))
    df = pd.DataFrame()
    df["Pwf(psia)"] = pwf
    if method == "Darcy":
        df["Qo(bpd)"] = df["Pwf(psia)"].apply(
            lambda x: qo_darcy(q_test, pwf_test, pr, x, pb)
        )
    elif method == "Vogel":
        df["Qo(bpd)"] = df["Pwf(psia)"].apply(
            lambda x: qo_vogel(q_test, pwf_test, pr, x, pb)
        )
    elif method == "IPR_compuesto":
        df["Qo(bpd)"] = df["Pwf(psia)"].apply(
            lambda x: qo_ipr_compuesto(q_test, pwf_test, pr, x, pb)
        )
        # Stand the axis of the IPR plot
    x = df["Qo(bpd)"]
    y = df["Pwf(psia)"]
    # The following steps are used to smooth the curve
    X_Y_Spline = make_interp_spline(x, y)
    X_ = np.linspace(x.min(), x.max(), 500)
    Y_ = X_Y_Spline(X_)
    # Build the curve
    ax.plot(X_, Y_, c="g")
    ax.set_xlabel("Qo(bpd)")
    ax.set_ylabel("Pwf(psia)")
    ax.set_title("IPR")
    ax.set(xlim=(0, df["Qo(bpd)"].max() + 10), ylim=(0, df["Pwf(psia)"].max() + 100))
    # Arrow and Annotations
    plt.annotate(
        "Bubble Point",
        xy=(Qb(q_test, pwf_test, pr, pb), pb),
        xytext=(Qb(q_test, pwf_test, pr, pb) + 100, pb + 100),
        arrowprops=dict(arrowstyle="->", lw=1),
    )
    # Horizontal and Vertical lines at bubble point
    plt.axhline(y=pb, color="r", linestyle="--")
    plt.axvline(x=Qb(q_test, pwf_test, pr, pb), color="r", linestyle="--")
    ax.grid()
    return fig


def vlp_curve(THP, API, wc, sg_h2o, md, tvd, ID, C):
    # Creating Dataframe
    df = pd.DataFrame()
    df["Q"] = np.array([0, 1000, 2000, 3000, 4000, 5000])
    df["THP (psi)"] = THP
    df["Pgravity (psia)"] = gradient_avg(API, wc, sg_h2o) * tvd
    df["f"] = df["Q"].apply(lambda x: f_darcy(x, ID, C))
    df["F (ft)"] = df["f"] * md
    df["Pf (psia)"] = df["F (ft)"] * gradient_avg(API, wc, sg_h2o)
    df["Po (psia)"] = df["THP (psi)"] + df["Pgravity (psia)"] + df["Pf (psia)"]
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(df["Q"], df["Po (psia)"], c="g")
    ax.set_xlabel("Q (BPD)", fontsize=14)
    ax.set_ylabel("Po (psia)")
    ax.set(xlim=(df["Q"].min(), df["Q"].max()))
    ax.set_title("Po vs Q (VLP)", fontsize=16)
    ax.grid()
    return fig


def IPR_vlp_curve(
    THP, API, wc, sg_h2o, md, tvd, ID, C, q_test, pwf_test, pr, pb, method
):
    columns = [
        "Q(bpd)",
        "Pwf(psia)",
        "THP(psia)",
        "Pgravity(psia)",
        "f",
        "F(ft)",
        "Pf(psia)",
        "Po(psia)",
        "Psys(psia)",
    ]
    df = pd.DataFrame(columns=columns)
    df[columns[0]] = np.array(
        [750, 1400, 2250, 3000, 3750, 4500, 5250, 6000, 6750, 7500]
    )
    if method == "Darcy":
        df[columns[1]] = df["Q(bpd)"].apply(
            lambda x: pwf_darcy(q_test, pwf_test, x, pr, pb)
        )
    elif method == "Vogel":
        df[columns[1]] = df["Q(bpd)"].apply(
            lambda x: pwf_vogel(q_test, pwf_test, x, pr, pb)
        )
    df[columns[2]] = THP
    df[columns[3]] = gradient_avg(API, wc, sg_h2o) * tvd
    df[columns[4]] = df["Q(bpd)"].apply(lambda x: f_darcy(x, ID, C))
    df[columns[5]] = df["f"] * md
    df[columns[6]] = gradient_avg(API, wc, sg_h2o) * df["F(ft)"]
    df[columns[7]] = df["THP(psia)"] + df["Pgravity(psia)"] + df["Pf(psia)"]
    df[columns[8]] = df["Po(psia)"] - df["Pwf(psia)"]

    # Graphing the results
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(df["Q(bpd)"], df["Pwf(psia)"], c="red", label="IPR")
    ax.plot(df["Q(bpd)"], df["Po(psia)"], c="green", label="VLP")
    ax.plot(df["Q(bpd)"], df["Psys(psia)"], c="b", label="System Curve")
    ax.set_xlabel("Q(bpd)")
    ax.set_ylabel("Pwf(psia)")
    ax.set_xlim(df["Q(bpd)"].min(), df["Q(bpd)"].max())
    ax.set_title("Nodal Analysis")
    ax.grid()
    plt.legend()
    return fig


# This will be used to present the needed data on the webpage
def nodal_helper():
    with st.expander(label="Reservoir Inflow Behaviour - IPR Flow rates"):
        with st.form(key="file_form_nodalIPR"):
            col1, col2, col3 = st.columns(3)
            pr = col1.number_input(
                label="pr - Reservoir pressure (psia)", value=2900, step=100
            )  # psi
            pb = col1.number_input(
                label="pb - Bubble point pressure (psia)", value=2500, step=100
            )  # psi
            q_test = col2.number_input(
                label="q_test - Test oil flow rate (bpd)", value=1000, step=100
            )  # bpd
            pwf_test = col2.number_input(
                label="pwf_test - Flowing bottom pressure of test (psia)",
                step=100,
                value=2000,
            )  # bpd
            method = col3.selectbox(
                "select method",
                ["Vogel", "IPR_compuesto", "Darcy"],
            )
            pwf_graph = np.array([4000, 3500, 3000, 2500, 1000, 0])
            pwf = col3.number_input(
                label="pwf - Flowing bottom pressure (psia)", value=1500, step=100
            )
            st.divider()
            submit = st.form_submit_button(label="Submit")
            if submit:
                try:
                    col4, col5 = st.columns(2)
                    fig = IPR_curve_methods(q_test, pwf_test, pr, pwf_graph, pb, method)
                    x = aof(q_test, pwf_test, pr, pb)
                    PI = j(q_test, pwf_test, pr, pb)
                    q1 = qo_t(q_test, pwf_test, pr, pwf, pb)
                    q2 = qo_darcy(q_test, pwf_test, pr, pwf, pb)
                    q3 = qo_ipr_compuesto(q_test, pwf_test, pr, pwf, pb)
                    q4 = qo_vogel(q_test, pwf_test, pr, pwf, pb)
                    q5 = Qb(q_test, pwf_test, pr, pb, pb)
                    # Creating dataframe and putting all the values inside it
                    col4.write("AOF: {:.0f} BBL/d".format(x))
                    col4.write("PI: {:.1f} bpd/psi".format(PI))
                    col4.write("Qo: {:.1f} bpd".format(q1))
                    col4.write("Qo_darcy: {:.1f} bpd".format(q2))
                    col5.write("Qo_IPR: {:.1f} bpd".format(q3))
                    col5.write("Qo_vogel: {:.1f} bpd".format(q4))
                    col5.write("Qb_flow at bubble: {:.1f} bpd".format(q5))
                    st.divider()
                    st.caption("Solving for rates 0 to 5000 with step of 1000 BBL/d")
                    columns = [
                        "AOF",
                        "PI",
                        "Qo",
                        "Qo_darcy",
                        "Qo_IPR",
                        "Qo_vogel",
                        "Qb_flow at bubble",
                    ]
                    df = pd.DataFrame(columns=columns)
                    df[columns[0]] = np.array([0])
                    df[columns[0]] = x
                    df[columns[1]] = PI
                    df[columns[2]] = q1
                    df[columns[3]] = q2
                    df[columns[4]] = q3
                    df[columns[5]] = q4
                    df[columns[6]] = q5
                    st.dataframe(df)
                    st.divider()
                    st.caption("Solving for rates 0 to 5000 with step of 1000 BBL/d")
                    st.pyplot(fig)
                except Exception:
                    st.subheader("No data selected")
                    st.write("Select the correct data for the MPFM")

    # ====================== IPR with fluid propertry tab ================================
    with st.expander(
        label="Reservoir Inflow Behaviour - IPR Petrophysical and Fluid Properties"
    ):
        with st.form(key="file_form_nodal"):
            col1, col2, col3 = st.columns(3)
            pr = col1.number_input(
                label="pr - Reservoir pressure (psia)", value=4000
            )  # psi
            ko = col1.number_input(label="Effective premeablity md", value=10)
            h = col1.number_input(label="h Reservoir hieght ft", value=50)
            bo = col2.number_input(label="bo Formation volume factor rb/stb", value=1.2)
            uo = col2.number_input(label="uo Oil viscosity cp", value=1.2)
            re = col3.number_input(label="re Drainage radius ft", value=3000)
            rw = col3.number_input(label="rw Well radius ft", value=0.328)
            s = col3.number_input(label="s Skin", value=0)
            st.divider()
            submit = st.form_submit_button(label="Submit")
            if submit:
                try:
                    q1 = j_darcy(ko, h, bo, uo, re, rw, s)
                    AOF = q1 * pr
                    st.subheader("Results for AOF and PI")
                    columns = ["AOF", "PI"]
                    df = pd.DataFrame(columns=columns)
                    df[columns[0]] = np.array([0])
                    df[columns[0]] = AOF
                    df[columns[1]] = q1
                    st.dataframe(df)
                except Exception:
                    st.subheader("No data selected")
                    st.write("Select the correct data for the MPFM")

    # ====================== VLR tab ================================
    with st.expander(label="VLR"):
        with st.form(key="file_form_nodalp"):
            col1, col2, col3 = st.columns(3)
            THP = col1.number_input(label="THP - Pressure psi", value=250)  # psia
            wc = col1.number_input(label="wc - water cut %", value=0.75)
            sg_h2o = col1.number_input(label="SG", value=1.04)
            API = col2.number_input(label="API", value=30)
            Q = col2.number_input(label="Q - Flow rate bpd", value=2500)  # bpd
            ID = col2.number_input(label="ID inch", value=2.875)  # in
            tvd = col3.number_input(label="tvd - True vertical depth", value=6000)  # ft
            md = col3.number_input(label="md - Measured depth", value=6600)  # ft
            C = col3.number_input(label="C - Factor", value=120)
            st.divider()
            submit = st.form_submit_button(label="Submit")
            if submit:
                try:
                    SG_Avg = sg_avg(API, wc, sg_h2o)
                    Gavg = gradient_avg(API, wc, sg_h2o)
                    Pg = Gavg * tvd
                    f = f_darcy(Q, ID, C)
                    Pf = f_darcy(Q, ID, C) * md * Gavg
                    po = THP + Pf + Pg
                    fig = vlp_curve(THP, API, wc, sg_h2o, md, tvd, ID, C)
                    # fig, fig2 = vlp_curve(THP, API, wc, sg_h2o, md, tvd, ID, C)
                    # Creating dataframe and putting all the values inside it
                    columns = [
                        "THP",
                        "SG avg",
                        "Gradient avg",
                        "Pressure due gravity",
                        "f friction",
                        "Pf Pressure due friction",
                        "Po Total Head",
                    ]
                    df = pd.DataFrame(columns=columns)
                    df[columns[0]] = np.array([0])
                    df[columns[0]] = THP
                    df[columns[1]] = SG_Avg
                    df[columns[2]] = Gavg
                    df[columns[3]] = Pg
                    df[columns[4]] = f
                    df[columns[5]] = Pf
                    df[columns[6]] = po
                    st.dataframe(df)
                    st.pyplot(fig)
                except Exception:
                    st.subheader("No data selected")
                    st.write("Select the correct data for the IPR")

    # ====================== IPR vs VLP curve tab ================================
    with st.expander(label="IPR vs VLP"):
        with st.form(key="file_form_nodalvlp"):
            col1, col2 = st.columns(2)
            col1.subheader("IPR Data")
            pr = col1.number_input(
                label="pr - Reservoir pressure (psia)", value=4000
            )  # psi
            pb = col1.number_input(
                label="pb - Bubble point pressure (psia)", value=3000
            )  # psi
            pwf = col1.number_input(
                label="pwf - Flowing bottom pressure (psia)", value=4000
            )  # np.array([4000, 3500, 3000, 2500, 1000, 0])
            q_test = col1.number_input(
                label="q_test - Test oil flow rate (bpd)", value=1500
            )  # bpd
            pwf_test = col1.number_input(
                label="pwf_test - Flowing bottom pressure of test (psia)",
                value=2000,
            )  # bpd C = col1.number_input(label="C - Factor" , value=120)
            method = col1.selectbox(
                "select method",
                ["Vogel", "Darcy"],
            )
            col2.subheader("IPR Data")
            THP = col2.number_input(label="THP - Pressure psi", value=250)  # psia
            sg_h2o = col2.number_input(label="SG", value=1.04)
            wc = col2.number_input(label="wc - water cut %", value=0.75)
            API = col2.number_input(label="API", value=30)
            ID = col2.number_input(label="ID inch", value=2.875)  # in
            md = col2.number_input(label="md - Measured depth", value=6600)  # ft
            tvd = col2.number_input(label="tvd - True vertical depth", value=6000)  # ft
            st.divider()
            submit = st.form_submit_button(label="Submit")
            if submit:
                try:
                    SG_Avg = sg_avg(API, wc, sg_h2o)
                    Gavg = gradient_avg(API, wc, sg_h2o)
                    Pg = Gavg * tvd
                    f = f_darcy(q_test, ID, C)
                    Pf = f_darcy(q_test, ID, C) * md * Gavg
                    x = aof(q_test, pwf_test, pr, pb)
                    PI = j(q_test, pwf_test, pr, pb)
                    po = THP + Pf + Pg
                    fig = IPR_vlp_curve(
                        THP,
                        API,
                        wc,
                        sg_h2o,
                        md,
                        tvd,
                        ID,
                        C,
                        q_test,
                        pwf_test,
                        pr,
                        pb,
                        method,
                    )
                    # Creating dataframe and putting all the values inside it
                    columns = [
                        "THP",
                        "SG avg",
                        "Gradient avg",
                        "Pressure due gravity",
                        "f friction",
                        "Pf Pressure due friction",
                        "Po Total Head",
                        "AOF",
                        "PI",
                    ]
                    df = pd.DataFrame()
                    df[columns[0]] = np.array([0])
                    df[columns[0]] = THP
                    df[columns[1]] = SG_Avg
                    df[columns[2]] = Gavg
                    df[columns[3]] = Pg
                    df[columns[4]] = f
                    df[columns[5]] = Pf
                    df[columns[6]] = po
                    df[columns[7]] = x
                    df[columns[8]] = PI
                    st.dataframe(df)
                    st.pyplot(fig)
                except Exception:
                    st.subheader("No data selected")
                    st.write("Select the correct data for the MPFM")
