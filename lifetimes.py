import matplotlib.pyplot as plt
try:
    import prettyplotlib as ppl
except ImportError:
    ppl = plt

import numpy as np
import scipy.optimize as optimize
import os
from names import *
np.seterr(all="ignore")

import brewer2mpl
set2 = brewer2mpl.get_map('Spectral', 'Diverging', 5).mpl_colors


def func(t, tau, intensity, delay):
    return intensity*np.exp(-(t-delay)/tau)


def main():

    if not os.path.exists('output/lifetimes/'):
        os.makedirs('output/lifetimes/')

    names = [1, 2, 3, 4, 5, 6, 7]
    zeropoints = [4, 4, 5.5, 4, 5, 5, 4]

    for i in names:
        data = np.loadtxt("input/raw/lifetimes%s.txt" % i, delimiter=",")

        time = data[:, 0] - 180 - zeropoints[int(i)-1]
        counts = data[:, 1]

        plt.close()
        plt.plot(time, counts, label="%d" % i, color=set2[0], linewidth=4, alpha=0.5)

        idx = (time > 0) & (time < 10)
        time = time[idx]
        counts = counts[idx]

        popt, pcov = optimize.curve_fit(func, time, counts, p0=[1.0, 350, 0.0])
        err = np.sqrt(np.diag(pcov))

        plt.plot(time, counts, label="%d" % i, color=set2[0], linewidth=4, alpha=0.5)
        plt.plot(time, func(time, *popt), label="fit %1.3lf [%1.3lf]" % (popt[0], err[0]),
                 color=set2[4], linewidth=2)
        plt.legend()
        plt.xlim([-5, 10])
        plt.yticks([])
        plt.ylabel('Intensity [a.u.]')
        plt.xlabel('$\\tau$ [ns]')

        print 'saving output/lifetimes/%s.png' % i
        print '\t%1.3lf %1.3lf %1.3lf' % (popt[0], popt[1], popt[2])
        plt.savefig('output/lifetimes/%s.png' % i)

if __name__ == "__main__":
    main()
