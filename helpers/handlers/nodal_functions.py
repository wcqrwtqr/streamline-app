import numpy as np


# Productivity Index (darcy law)
# Productivity Index Taking into account Petrophysical and Fluid Properties
def j_darcy(ko, h, bo, uo, re, rw, s, flow_regime="seudocontinuo"):
    """
    Productivity Index (darcy law) Petrophysical and Fluid Properties
    J_darcy : Productivity Index (bpd/psi)
    Ko : Effective permeablity (md)
    h : Thickness (ft)
    Bo : Oil Formation Volume Factor (rb/stb)
    uo : Oil Viscosity (cp)
    re : Drainage radius (ft)
    rw : Well radius (ft)
    s : Skin
    """
    if flow_regime == "seudocontinuo":
        J_darcy = ko * h / (141.2 * bo * uo * (np.log(re / rw) - 0.75 + s))
    elif flow_regime == "continuo":
        J_darcy = ko * h / (141.2 * bo * uo * (np.log(re / rw) + s))
    return J_darcy


# Productivity Index
# Productivity Index with productivity test data
def j(q_test, pwf_test, pr, pb, ef=1, ef2=None):
    """
    J : Productivity index (bpd/psi).
    r_test : Test oil flow rate (bpd).
    Pr : Reservoir pressure (psia).
    Pb : Bubble point pressure (psia).
    pwf_test : Flowing bottom pressure of test (psia).
    EF : Flow efficiency.
    EF2 : Well flow efficiency measured after a period of time.
    """
    if ef == 1:
        if pwf_test >= pb:
            J = q_test / (pr - pwf_test)
        else:
            J = q_test / (
                (pr - pb)
                + (pb / 1.8) * (1 - 0.2 * (pwf_test / pb) - 0.8 * (pwf_test / pb) ** 2)
            )
    elif ef != 1 and ef2 is None:
        if pwf_test >= pb:
            J = q_test / (pr - pwf_test)
        else:
            J = q_test / (
                (pr - pb)
                + (pb / 1.8)
                * (1.8 * (1 - pwf_test / pb) - 0.8 * ef * (1 - pwf_test / pb) ** 2)
            )
    elif ef != 1 and ef2 is not None:
        if pwf_test >= pb:
            J = ((q_test / (pr - pwf_test)) / ef) * ef2
        else:
            J = (
                (
                    q_test
                    / (
                        (pr - pb)
                        + (pb / 1.8)
                        * (
                            1.8 * (1 - pwf_test / pb)
                            - 0.8 * ef * (1 - pwf_test / pb) ** 2
                        )
                    )
                )
                / ef
            ) * ef2
    return J


# Oil Flow Rate at Bubble Point
# Q(bpd) @ Pb
def Qb(q_test, pwf_test, pr, pb, ef=1, ef2=None):
    """
    Qb : Oil Flow Rate at Bubble Point (bpd)
    J : Productivity Index (bpd/psi) 𝑃𝑟
    Pr : Reservoir Pressure (psia)
    Pb : Bubble Point Pressue (psia)
    """
    qb = j(q_test, pwf_test, pr, pb, ef, ef2) * (pr - pb)
    return qb


# AOF at different conditions
# AOF(bpd)
def aof(q_test, pwf_test, pr, pb, ef=1, ef2=None):
    """
    AOF : Maximum flow rate (bpd).
    Qb : Bubble point flow rate(bpd).
    J: Productivity index (bpd/psi).
    Pr : Reservoir pressure (psia). 𝑃𝑏
    Pb : Bubble point pressure (psia). 𝑃𝑤𝑓
    Pwf : Flowing bottom pressure (psia). 𝑃𝑤𝑓𝑡𝑒𝑠𝑡
    Pwftest : Flowing bottom pressure of test (psia).
    Qotest : Test oil flow rate (bpd). 𝐸𝐹
    EF : Flow efficiency. 𝐸𝐹2
    EF2 : Well flow efficiency measured after a period of time.
    """
    if ef == 1 and ef2 is None:
        if pr > pb:  # Yac. subsaturado
            if pwf_test >= pb:
                AOF = j(q_test, pwf_test, pr, pb) * pr
            elif pwf_test < pb:
                AOF = Qb(q_test, pwf_test, pr, pb, ef=1) + (
                    (j(q_test, pwf_test, pr, pb) * pb) / 1.8
                )
        else:  # Yac. Saturado
            AOF = q_test / (1 - 0.2 * (pwf_test / pr) - 0.8 * (pwf_test / pr) ** 2)

    elif ef < 1 and ef2 is None:
        if pr > pb:
            if pwf_test >= pb:
                AOF = j(q_test, pwf_test, pr, pb, ef) * pr
            elif pwf_test < pb:
                AOF = Qb(q_test, pwf_test, pr, pb, ef) + (
                    (j(q_test, pwf_test, pr, pb, ef) * pb) / 1.8
                ) * (1.8 - 0.8 * ef)
        else:
            AOF = (
                q_test
                / (
                    1.8 * ef * (1 - pwf_test / pr)
                    - 0.8 * ef**2 * (1 - pwf_test / pr) ** 2
                )
            ) * (1.8 * ef - 0.8 * ef**2)

    elif ef > 1 and ef2 is None:
        if pr > pb:
            if pwf_test >= pb:
                AOF = j(q_test, pwf_test, pr, pb, ef) * pr
            elif pwf_test < pb:
                AOF = Qb(q_test, pwf_test, pr, pb, ef) + (
                    (j(q_test, pwf_test, pr, pb, ef) * pb) / 1.8
                ) * (0.624 + 0.376 * ef)
        else:
            AOF = (
                q_test
                / (
                    1.8 * ef * (1 - pwf_test / pr)
                    - 0.8 * ef**2 * (1 - pwf_test / pr) ** 2
                )
            ) * (0.624 + 0.376 * ef)

    elif ef < 1 and ef2 >= 1:
        if pr > pb:
            if pwf_test >= pb:
                AOF = j(q_test, pwf_test, pr, pb, ef, ef2) * pr
            elif pwf_test < pb:
                AOF = Qb(q_test, pwf_test, pr, pb, ef, ef2) + (
                    j(q_test, pwf_test, pr, pb, ef, ef2) * pb / 1.8
                ) * (0.624 + 0.376 * ef2)
        else:
            AOF = (
                q_test
                / (
                    1.8 * ef * (1 - pwf_test / pr)
                    - 0.8 * ef**2 * (1 - pwf_test / pr) ** 2
                )
            ) * (0.624 + 0.376 * ef2)

    elif ef > 1 and ef2 <= 1:
        if pr > pb:
            if pwf_test >= pb:
                AOF = j(q_test, pwf_test, pr, pb, ef, ef2) * pr
            elif pwf_test < pb:
                AOF = Qb(q_test, pwf_test, pr, pb, ef, ef2) + (
                    j(q_test, pwf_test, pr, pb, ef, ef2) * pb / 1.8
                ) * (1.8 - 0.8 * ef2)
        else:
            AOF = (
                q_test
                / (
                    1.8 * ef * (1 - pwf_test / pr)
                    - 0.8 * ef**2 * (1 - pwf_test / pr) ** 2
                )
            ) * (1.8 * ef - 0.8 * ef2**2)
    return AOF


# Qo using Darcy's equation (linear method)
# Qo (bpd) @ Darcy Conditions
def qo_darcy(q_test, pwf_test, pr, pwf, pb, ef=1, ef2=None):
    """
    Qo : Oil flow rate (bpd) 𝐽
    J: Productivity index (bpd/psi)
    Pr : Reservoir pressure (psia) 𝑃𝑏
    Pb : Bubble point pressure (psia)
    """
    qo = j(q_test, pwf_test, pr, pb) * (pr - pwf)
    return qo


# Qo using Vogel's method.
# Qo(bpd) @ vogel conditions
def qo_vogel(q_test, pwf_test, pr, pwf, pb, ef=1, ef2=None):
    """
    Qo : Oil flow rate (bpd) 𝐴𝑂𝐹
    AOF : Maximum flow rate (bpd)
    Pr : Reservoir pressure (psia)
    Pb : Pressure at bubble point (psia) 𝑃𝑤𝑓
    Pwf : Flowing bottom pressure (psia)
    EF : Flowing efficiency
    """
    qo = aof(q_test, pwf_test, pr, pb) * (1 - 0.2 * (pwf / pr) - 0.8 * (pwf / pr) ** 2)
    return qo


# Qo to generate composite IPR curve
# Qo(bpd) @ vogel conditions
def qo_ipr_compuesto(q_test, pwf_test, pr, pwf, pb):
    """
    This method combines the Darcy equation and the Vogel equation, because the IPR curve is linear up to
    the bubble point, and subsequently has a parabolic form, by using the Vogel equation for values below
    the bubble point.

    Qo : Oil flow rate (bpd) 𝐴𝑂𝐹
    AOF : Maximun oil flow rate (bpd)
    J: Productivity index (bpd/psi) 𝑃𝑟
    Pr : Reservoir pressure (psia) 𝑃𝑏
    Pb : Pressure at bubble point 𝑃𝑤𝑓
    Pwf : Flowing bottom pressure (psia)
    """
    if pr > pb:  # Yac. subsaturado
        if pwf >= pb:
            qo = qo_darcy(q_test, pwf_test, pr, pwf, pb)
        elif pwf < pb:
            qo = Qb(q_test, pwf_test, pr, pb) + (
                (j(q_test, pwf_test, pr, pb) * pb) / 1.8
            ) * (1 - 0.2 * (pwf / pb) - 0.8 * (pwf / pb) ** 2)

    elif pr <= pb:  # Yac. Saturado
        qo = aof(q_test, pwf_test, pr, pb) * (
            1 - 0.2 * (pwf / pr) - 0.8 * (pwf / pr) ** 2
        )
    return qo


# Qo(bpd) @Standing Conditions
def qo_standing(q_test, pwf_test, pr, pwf, pb, ef=1, ef2=None):
    qo = aof(q_test, pwf_test, pr, pb, ef=1) * (
        1.8 * ef * (1 - pwf / pr) - 0.8 * ef**2 * (1 - pwf / pr) ** 2
    )
    return qo


# Qo(bpd) @ vogel conditions
# Qo(bpd) @ all conditions
def qo_t(q_test, pwf_test, pr, pwf, pb, ef=1, ef2=None):
    if ef == 1 and ef2 is None:
        if pr > pb:  # Yac. subsaturado
            if pwf >= pb:
                qo = qo_darcy(q_test, pwf_test, pr, pwf, pb)
            elif pwf < pb:
                qo = Qb(q_test, pwf_test, pr, pb) + (
                    (j(q_test, pwf_test, pr, pb) * pb) / 1.8
                ) * (1 - 0.2 * (pwf / pb) - 0.8 * (pwf / pb) ** 2)
        else:  # Yac. Saturado
            qo = qo_vogel(q_test, pwf_test, pr, pwf, pb)

    elif ef != 1 and ef2 is None:
        if pr > pb:  # Yac. subsaturado
            if pwf >= pb:
                qo = qo_darcy(q_test, pwf_test, pr, pwf, pb, ef, ef2)
            elif pwf < pb:
                qo = Qb(q_test, pwf_test, pr, pb, ef) + (
                    (j(q_test, pwf_test, pr, pb, ef) * pb) / 1.8
                ) * (1.8 * (1 - pwf / pb) - 0.8 * ef * (1 - pwf / pb) ** 2)
        else:  # Yac.saturado
            qo = qo_standing(q_test, pwf_test, pr, pwf, pb, ef)

    elif ef != 1 and ef2 is not None:
        if pr > pb:  # Yac. subsaturado
            if pwf >= pb:
                qo = qo_darcy(q_test, pwf_test, pr, pwf, pb, ef, ef2)
            elif pwf < pb:
                qo = Qb(q_test, pwf_test, pr, pb, ef, ef2) + (
                    (j(q_test, pwf_test, pr, pb, ef, ef2) * pb) / 1.8
                ) * (1.8 * (1 - pwf / pb) - 0.8 * ef * (1 - pwf / pb) ** 2)
            else:  # Yac. saturado
                qo = qo_standing(q_test, pwf_test, pr, pwf, pb, ef, ef2)
    return qo


# Pwf @ vogel conditions
def pwf_vogel(q_test, pwf_test, pr, qo, pb):
    """
    Pwf at Different Conditions
    Qo: Oil Flow Rate of productivity test (bpd)
    AOF = Qomax : Absolute Open Flow (bpd)
    Qb: Oil Flow Rate at Bubble Point (bpd) J:Productivity Index (bpd/psi)
    Pr: Reservoir Pressure (psia) 𝑃𝑏
    Pb: Bubble Point Pressue 𝑃𝑤𝑓
    Pwf : Pressure Well Flowing (psia) 𝑃𝑤𝑓𝑡𝑒𝑠𝑡
    Pwf test : Pressure Well Flowing of productity test (psia) 𝑄𝑜𝑡𝑒𝑠𝑡
    Qotest : Oil Flow Rate of productivity test (bpd)
    """
    if pr > pb:
        if qo <= Qb(q_test, pwf_test, pr, pb):
            pwf = pr - qo / j(q_test, pwf_test, pr, pb)
        elif qo > Qb(q_test, pwf_test, pr, pb):
            Qmax = Qb(q_test, pwf_test, pr, pb) + (
                (j(q_test, pwf_test, pr, pb) * pb) / (1.8)
            )
            pwf = 0.125 * pr * (-1 + np.sqrt(81 - 80 * qo / Qmax))
    elif pr <= pb:
        Qmax = q_test / (1 - 0.2 * (pwf_test / pr) - 0.8 * (pwf_test / pr) ** 2)
        pwf = 0.125 * pr * (-1 + np.sqrt(81 - 80 * qo / Qmax))
    return pwf


def pwf_darcy(q_test, pwf_test, q, pr, pb):
    pwf = pr - (q / j(q_test, pwf_test, pr, pb))
    return pwf


# Friction factor (f) from darcy-weishbach equation
def f_darcy(Q, ID, C=120):
    """
    Friction factor (f) from darcy-weishbach equation
    """
    f = (2.083 * (((100 * Q) / (34.3 * C)) ** 1.85 * (1 / ID) ** 4.8655)) / 1000
    return f


# SGOil using API
def sg_oil(API):
    """
    SGOil using API
    """
    SG_oil = 141.5 / (131.5 + API)
    return SG_oil


# SG average of fluids
def sg_avg(API, wc, sg_h2o):
    """
    SG average of fluids
    wc water cut
    sg_h20 water sg
    """
    sg_avg = wc * sg_h2o + (1 - wc) * sg_oil(API)
    return sg_avg


# Average Gradient using fresh water gradient (0.433 psi/ft)
def gradient_avg(API, wc, sg_h2o):
    """
    Average Gradient using fresh water gradient (0.433 psi/ft)
    """
    g_avg = sg_avg(API, wc, sg_h2o) * 0.433
    return g_avg
