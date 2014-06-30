import numpy as np
from scipy.special import erfc


def g2(t, c1, l1, c2, l2, l3, d):
    return np.choose(t < 0, [
        1 + c1*np.exp(-l1*t) + c2*np.exp(-l2*t),
        1-np.exp(l3*t)
    ])


def g2c_direct(t, c1, l1, l2, d):
    sig = 0.3
    c2 = -1
    a = c1*0.5*np.exp(-l1*(t-d) +
        0.5*(sig**2.0)*(l1**2.0))*(erfc(-(t-d)/np.sqrt(2.0*sig**2.0) + l1*(sig)/np.sqrt(2.0)))

    b = c2*0.5*np.exp(l2*(t-d) +
        0.5*(sig**2.0)*(l2**2.0))*(erfc((t-d)/np.sqrt(2.0*sig**2.0) + l2*(sig)/np.sqrt(2.0)))

    y = 1 + a + b
    return y


def g2c_indirect(t, c1, l1, l3, l2, d):
    sig = 0.3
    c2 = -1
    c3 = - 1 - c1

    a1 = c1*0.5*np.exp(-l1*(t-d) +
         0.5*(sig**2.0)*(l1**2.0))*(erfc(-(t-d)/np.sqrt(2.0*sig**2.0) + l1*(sig)/np.sqrt(2.0)))

    a3 = c3*0.5*np.exp(-l3*(t-d) +
         0.5*(sig**2.0)*(l3**2.0))*(erfc(-(t-d)/np.sqrt(2.0*sig**2.0) + l3*(sig)/np.sqrt(2.0)))

    b = c2*0.5*np.exp(l2*(t-d) +
        0.5*(sig**2.0)*(l2**2.0))*(erfc((t-d)/np.sqrt(2.0*sig**2.0) + l2*(sig)/np.sqrt(2.0)))

    y = 1 + a1 + a3 + b
    return y


def g2c_antidirect(t, l1, l2, d):
    sig = 0.3
    c1 = -1
    c2 = -1
    a = c1*0.5*np.exp(-l1*(t-d) +
        0.5*(sig**2.0)*(l1**2.0))*(erfc(-(t-d)/np.sqrt(2.0*sig**2.0) + l1*(sig)/np.sqrt(2.0)))

    b = c2*0.5*np.exp(l2*(t-d) +
        0.5*(sig**2.0)*(l2**2.0))*(erfc( (t-d)/np.sqrt(2.0*sig**2.0) + l2*(sig)/np.sqrt(2.0)))

    y = 1 + a + b

    return y
