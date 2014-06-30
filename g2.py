import numpy as np
from scipy.special import erfc


def g2(t, c1, l1, c2, l2, l3, d):
    return np.choose(t < 0, [
        1 + c1*np.exp(-l1*t) + c2*np.exp(-l2*t),
        1-np.exp(l3*t)
    ])


def g2c(t, c1, l1, l2, d):
    """Continious convoluted g2.
       Parameters
       ----------
       t: array
       args: parameters
       Returns
       -------
       array: 1D array g2(t)
    """
    sig = 0.3
    c2 = -1
    a = c1*0.5*np.exp(-l1*(t-d) +
        0.5*(sig**2.0)*(l1**2.0))*(erfc(-(t-d)/np.sqrt(2.0*sig**2.0) + l1*(sig)/np.sqrt(2.0)))

    b = c2*0.5*np.exp(l2*(t-d) +
        0.5*(sig**2.0)*(l2**2.0))*(erfc((t-d)/np.sqrt(2.0*sig**2.0) + l2*(sig)/np.sqrt(2.0)))

    y = 1 + a + b
    return y


def complicated_max(c1, l1, l2):
    A = (l1 + l2*c1)/(l1*c1)
    k1 = -l1/(l2-l1)
    k2 = -l2/(l2-l1)

    return 1 + c1*(A**k1) - (1+c1)*(A**k2)


def inverse_foo_for_c(target, l1, l2):
    cs = np.linspace(0.0, 10.0, 1000)
    fmaxes = np.zeros_like(cs)

    for i in xrange(cs.size):
        c = cs[i]
        fmaxes[i] = complicated_max(c, l1, l2)

    deltas = target - fmaxes
    return cs[np.abs(deltas).argmin()]


def g2c_complicated_fitter(fmax):

    def foo(t, l1, l2, l3, d):
        """Continious convoluted g2.
          Parameters
          ----------
             t: array
             args: parameters
          Returns
          -------
             array: 1D array g2(t)
        """
        sig = 0.3
        c3 = -1

        c1 = inverse_foo_for_c(fmax, l1, l2)

        if l1 > 1.0:
            return 1e6
        if l2 < 1.0:
            return 1e6
        if np.abs(fmax - complicated_max(c1, l1, l2)) > 0.01:
            return 1e6

        c2 = - 1 - c1

        a1 = c1*0.5*np.exp(-l1*(t-d) +
             0.5*(sig**2.0)*(l1**2.0))*(erfc(-(t-d)/np.sqrt(2.0*sig**2.0) + l1*(sig)/np.sqrt(2.0)))

        a2 = c2*0.5*np.exp(-l2*(t-d) +
             0.5*(sig**2.0)*(l2**2.0))*(erfc(-(t-d)/np.sqrt(2.0*sig**2.0) + l2*(sig)/np.sqrt(2.0)))

        b = c3*0.5*np.exp(l3*(t-d) +
            0.5*(sig**2.0)*(l3**2.0))*(erfc((t-d)/np.sqrt(2.0*sig**2.0) + l3*(sig)/np.sqrt(2.0)))

        y = 1 + a1 + a2 + b

        # print "fmax: %1.2lf fgen: %1.2lf" % (fmax, complicated_max(c1, l1, l2))
        # print "c: %1.2lf l1: %1.2lf l2: %1.2lf\n" % (c1, l1, l2)

        return y

    return foo


def g2c_complicated(t, c1, l1, l3, l2, d):
    """Continious convoluted g2.
      Parameters
      ----------
         t: array
         args: parameters
      Returns
      -------
         array: 1D array g2(t)
    """
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


def g2c_auto(t, l1, l2, d):
    """Continious convoluted g2.
        Parameters
        ----------
            t: array
            args: parameters
        Returns
        -------
            array: 1D array g2(t)
    """
    sig = 0.3
    c1 = -1
    c2 = -1
    a = c1*0.5*np.exp(-l1*(t-d) +
        0.5*(sig**2.0)*(l1**2.0))*(erfc(-(t-d)/np.sqrt(2.0*sig**2.0) + l1*(sig)/np.sqrt(2.0)))

    b = c2*0.5*np.exp(l2*(t-d) +
        0.5*(sig**2.0)*(l2**2.0))*(erfc( (t-d)/np.sqrt(2.0*sig**2.0) + l2*(sig)/np.sqrt(2.0)))

    y = 1 + a + b

    return y
