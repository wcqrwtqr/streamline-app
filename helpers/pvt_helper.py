import streamlit as st
import pandas as pd
import numpy as np
from handlers.pvt_correlation_functions import (
    oil_compressibility,
    oil_pbubble,
    oil_fvf,
    gasoilratio,
    oil_mu,
    gas_pseudoprops,
    gas_zfactor,
    gas_density,
    gas_fvf,
    gas_compressibility,
    gas_mu,
    water_compressibility,
    water_fvf,
    water_mu,
    water_pbubble,
)


def pvt_helper():
    with st.expander(label="OIL PVT"):
        with st.form(key="file_form"):
            col1, col2, col3, col4 = st.columns(4)
            sg_val = col1.number_input(label="SG", step=0.10, value=0.75)
            temp_val = col2.number_input(label="Temperature F", step=5, value=150)
            Rsb_val = col3.number_input(label="Solution GOR", step=10, value=300)
            API_val = 141.5 / (sg_val) - 131.5
            press_val = col4.number_input(label="Pressure psi", step=10, value=300)
            submit = st.form_submit_button(label="Submit")
            if submit:
                # calculate bubble-point pressure using Vasquez and Beggs (1980)
                pbubble = oil_pbubble(Rsb_val, sg_val, API_val, temp_val)
                # calculate isothermal compressibility using Vazquez and Beggs (1980); McCain et al (1988)
                coil = oil_compressibility(
                    press_val, pbubble, temp_val, API_val, Rsb_val, sg_val
                )
                # calculate FVF using Vazquez and Beggs (1980); Levitan and Murtha (1999)
                Bo = oil_fvf(pbubble, API_val, Rsb_val, sg_val, temp_val, press_val)
                # calculate gas-oil ratio using Vazquez and Beggs (1980)
                Rs = gasoilratio(press_val, pbubble, sg_val, API_val, temp_val, Rsb_val)
                # calculate gas-oil ratio using Vazquez and Beggs (1980); Beggs and Robinson (1975)
                viscooil = oil_mu(press_val, pbubble, sg_val, API_val, temp_val, Rs)
                # col1, col2 = st.columns(2)
                columns = [
                    "Pressure (psi)",
                    "Temperature (°F)",
                    "Specific Gravity",
                    "Gas-oil ratio (scf/STB)",
                    "API",
                    "Bubble point (psi)",
                    "GOR (scf/STB)",
                    "FVF RB/STB",
                    "Isothermal Compressibility (microcip)",
                    "Viscosity (cp)",
                ]
                df = pd.DataFrame(columns=columns)
                df[columns[0]] = np.array([0])
                df[columns[0]] = press_val
                df[columns[1]] = temp_val
                df[columns[2]] = sg_val
                df[columns[3]] = Rsb_val
                df[columns[4]] = API_val
                df[columns[5]] = pbubble
                df[columns[6]] = Rs
                df[columns[7]] = Bo
                df[columns[8]] = coil * 1_000_000
                df[columns[9]] = viscooil
                st.dataframe(df)
                st.markdown(
                    """
                * calculate bubble-point pressure using Vasquez and Beggs (1980)
                * calculate isothermal compressibility using Vazquez and Beggs (1980); McCain et al (1988)
                * calculate FVF using Vazquez and Beggs (1980); Levitan and Murtha (1999)
                * calculate gas-oil ratio using Vazquez and Beggs (1980); Beggs and Robinson (1975)
                """
                )

    with st.expander(label="Gas PVT"):
        with st.form(key="file_form_gas"):
            col1, col2, col3, col4, col5 = st.columns(5)
            press_val = col1.number_input(label="Pressure psi", step=10, value=2000)
            temp_val = col2.number_input(label="Temperature F", step=5, value=110)
            sg_val = col3.number_input(label="SG", step=0.10, value=0.7)
            h2s_val = col4.number_input(label="HS %", step=0.01, value=0.07)
            co2_val = col5.number_input(label="Co2 %", step=0.01, value=0.07)
            submit = st.form_submit_button(label="Submit")
            if submit:
                # calculate pseudoproperties using Sutton (1985), Wichert and Aziz (1972)
                P_pc, T_pc, P_pr, T_pr = gas_pseudoprops(
                    temp_val, press_val, sg_val, h2s_val, co2_val
                )
                # calculate z-factor using Dranchuk-Aboukassem (1975)
                pseudo_rho, z_factor = gas_zfactor(T_pr, P_pr)
                # calculate density
                rhogas = gas_density(temp_val, press_val, sg_val, z_factor)
                # calculate gas FVF
                Bg = gas_fvf(z_factor, temp_val, press_val)
                # calculate isothermal compressibility using Trube (1957) and Mattar (1975)
                cgas = gas_compressibility(T_pr, P_pr, pseudo_rho, z_factor, P_pc)
                # calculate viscosity using Lee et al (1966)
                viscogas = gas_mu(temp_val, rhogas, sg_val)
                columns = [
                    "Pressure (psi)",
                    "Temperature (°F)",
                    "Specific Gravity",
                    "z-factor",
                    "Density (lb/ft3)",
                    "FVF ft3/scf",
                    "Isothermal Compressibility (microcip)",
                    "Viscosity (cp)",
                ]
                df = pd.DataFrame(columns=columns)
                df[columns[0]] = np.array([0])
                df[columns[0]] = press_val
                df[columns[1]] = temp_val
                df[columns[2]] = sg_val
                df[columns[3]] = z_factor
                df[columns[4]] = rhogas
                df[columns[5]] = Bg
                df[columns[6]] = cgas * 1_000_000
                df[columns[7]] = viscogas
                st.dataframe(df)
                st.markdown(
                    """
                * calculate pseudoproperties using Sutton (1985), Wichert and Aziz (1972)
                * calculate z-factor using Dranchuk-Aboukassem (1975)
                * calculate isothermal compressibility using Trube (1957) and Mattar (1975)
                * calculate viscosity using Lee et al (1966)
                """
                )

    with st.expander(label="Water PVT"):
        with st.form(key="file_form_water"):
            col1, col2, col3, col4, col5 = st.columns(5)
            press_val = col1.number_input(label="Pressure psi", step=10, value=2000)
            temp_val = col2.number_input(label="Temperature F", step=5, value=110)
            s_val = col3.number_input(label="Salinity, wt%", step=1, value=5)
            submit = st.form_submit_button(label="Submit")
            if submit:
                # calculate water FVF using McCain et al (1989)
                Bw = water_fvf(temp_val, press_val)
                # calculate vapor (bubble-point) press_val using the classic Antoine (1888)
                pbubble = water_pbubble(temp_val)
                # calculate isothermal water compressibility using Osif (1988) and McCain (1989)
                cw = water_compressibility(temp_val, press_val, s_val, Bw)
                # calculate water viscosity using McCain (1989)
                mu_w = water_mu(temp_val, press_val, s_val)
                columns = [
                    "Pressure (psi)",
                    "Temperature (°F)",
                    "Salinity",
                    "FVF (RB/STB)",
                    "Bubble-Point (psia)",
                    "Isothermal Compressibility (microcip)",
                    "Viscosity (cp)",
                ]
                df = pd.DataFrame(columns=columns)
                df[columns[0]] = np.array([0])
                df[columns[0]] = press_val
                df[columns[1]] = temp_val
                df[columns[2]] = s_val
                df[columns[3]] = Bw
                df[columns[4]] = pbubble
                df[columns[5]] = cw * 1_000_000
                df[columns[6]] = mu_w
                st.dataframe(df)
                st.markdown(
                    """
                * calculate water FVF using McCain et al (1989)
                * calculate vapor (bubble-point) press_val using the classic Antoine (1888)
                * calculate isothermal water compressibility using Osif (1988) and McCain (1989)
                * calculate water viscosity using McCain (1989)
                """
                )
