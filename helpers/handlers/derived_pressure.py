import numpy as np


def calc_derivative_np(time, pressure, factor_L):
    # inicializacao do fator_L e variaveis secundarias

    n_points = len(time)
    deriv_pressure = []
    deriv_time = []
    i = 0
    while i < n_points:
        t1 = time[i]
        p1 = pressure[i]
        # encontrar o ti-1
        j = i
        while j > 0:
            if time[j] < t1 / np.exp(factor_L):
                break
            j -= 1
        # encontrar o ti+1
        k = i
        while k < n_points - 1:
            if time[k] > t1 * np.exp(factor_L):
                break
            k += 1

        p0, p2 = pressure[j], pressure[k]
        t0, t2 = time[j], time[k]
        log_t0 = np.log(t0) if t0 != 0 else 0
        log_t1 = np.log(t1) if t1 != 0 else 0
        log_t2 = np.log(t2) if t2 != 0 else 0
        w1 = log_t1 - log_t0
        w2 = log_t2 - log_t1
        m1 = (p1 - p0) / w1 if w1 > 0 else 0
        m2 = (p2 - p1) / w2 if w2 > 0 else 0
        tdpdt = m1 * w2 / (w1 + w2) + m2 * w1 / (w1 + w2)
        # calculo da derivada
        deriv_pressure.append(tdpdt)
        i += 1
        # retorna ambos os arrays (t e dpdt) como arrays numpy
    return np.array(deriv_pressure)
