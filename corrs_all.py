import matplotlib.pyplot as plt
import os
try:
    import prettyplotlib as ppl
except ImportError:
    ppl = plt

import numpy as np
import scipy.optimize as optimize
import g2 as g2
from names import *
np.seterr(all="ignore")


def main():

    if not os.path.exists('output/all/'):
        os.makedirs('output/all/')

    with open('output/fit.md', "w") as file:
        file.write("")

    for i in range(len(names)):

        name = names[i]
        label = labels[i]

        data = np.loadtxt('input/rebinned/%s.txt' % name, delimiter=",")
        time = data[:, 0] - zeropoints[i]
        counts = data[:, 1]

        idx = (time > -20) & (time < 20)
        time = time[idx]
        counts = counts[idx]
        counts_n = counts/counts.mean()

        try:
            p0 = [4, 1, 0.4, 0]
            poptd, pcovd = optimize.curve_fit(g2.g2c_direct, time, counts_n, p0=p0)
            perrd = np.sqrt(np.diag(pcovd))
        except RuntimeError:
            poptd = np.array([0., 0., 0., 0.])
            perrd = np.zeros_like(poptd)

        try:
            p0 = [0.6, 1.1, 0.4, 0.5, 0]
            popti, pcovi = optimize.curve_fit(g2.g2c_indirect, time, counts_n, p0=p0)
            perri = np.sqrt(np.diag(pcovi))
        except RuntimeError:
            popti = np.array([0., 0., 0., 0., 0.])
            perri = np.zeros_like(popti)

        try:
            p0 = [0.5, 0.5, 0]
            popta, pcova = optimize.curve_fit(g2.g2c_antidirect, time, counts_n, p0=p0)
            perra = np.sqrt(np.diag(pcova))
        except RuntimeError:
            popta = np.array([0., 0., 0.])
            perra = np.zeros_like(popta)

        with open('output/fit.md', "a") as file:
            file.write("\n# %s\n" % label)
            file.write('![](all/corrs%s.png)\n' % name)

            file.write("## Direct\n")
            file.write("\tc1: %1.3lf +- %1.3lf\n" % (poptd[0], perrd[0]))
            file.write("\tl1: %1.3lf +- %1.3lf\n" % (poptd[1], perrd[1]))
            file.write("\tl2: %1.3lf +- %1.3lf\n" % (poptd[2], perrd[2]))

            file.write("## Indirect\n")
            file.write("\tc1: %1.3lf +- %1.3lf\n" % (popti[0], perri[0]))
            file.write("\tl1: %1.3lf +- %1.3lf\n" % (popti[1], perri[1]))
            file.write("\tl3: %1.3lf +- %1.3lf\n" % (popti[2], perri[2]))
            file.write("\tl2: %1.3lf +- %1.3lf\n" % (popti[3], perri[3]))

            file.write("## Antidirect\n")
            file.write("\tl1: %1.3lf +- %1.3lf\n" % (popta[0], perra[1]))
            file.write("\tl2: %1.3lf +- %1.3lf\n" % (popta[1], perra[0]))

        a = g2.g2c_direct(time, *poptd)
        b = g2.g2c_indirect(time, *popti)
        c = g2.g2c_antidirect(time, *popta)
        null = np.zeros_like(c)

        if name == "1_3":
            exports = np.vstack((time, counts_n, a, b, null)).T
        elif name == "1_6":
            exports = np.vstack((time, counts_n, a, b, null)).T
        elif name == "1_7":
            exports = np.vstack((time, counts_n, a, b, null)).T
        elif name == "2_3":
            exports = np.vstack((time, counts_n, a, b, null)).T
        elif name == "2_6":
            exports = np.vstack((time, counts_n, null, b, c)).T
        elif name == "2_7":
            exports = np.vstack((time, counts_n, a, b, null)).T
        elif name == "3_5":
            exports = np.vstack((time, counts_n, null, b, c)).T
        elif name == "3_7":
            exports = np.vstack((time, counts_n, null, b, c)).T
        elif name == "4_5":
            exports = np.vstack((time, counts_n, a, null, null)).T
        elif name == "5_7":
            exports = np.vstack((time, counts_n, null, b, c)).T
        elif name == "6_7":
            exports = np.vstack((time, counts_n, null, b, c)).T
        elif name == "7_5":
            exports = np.vstack((time, counts_n, null, b, c)).T

        print "%d: saving specific fits %s" % (i, name)
        np.savetxt('output/all/data/fit_%s.txt' % name, exports)

        # just plotting stuff now
        plt.close()
        ppl.plot(time, counts_n, linewidth=4, alpha=0.3)
        ppl.plot(time, g2.g2c_direct(time, *poptd), label="Direct", linewidth=5)
        ppl.plot(time, g2.g2c_indirect(time, *popti), label="Indirect", linewidth=2)
        ppl.plot(time, g2.g2c_antidirect(time, *popta), label="Antidirect", linewidth=2)

        plt.text(5, 0.1, label)
        plt.xlim([-15, 15])
        plt.ylim(ymin=0)

        ppl.legend()
        xlabel = plt.xlabel("$\\tau (ns)$")
        plt.ylabel("$g^{(2)}(\\tau)$")

        print "saving all fits %s" % name
        plt.savefig('output/all/corrs%s.png' % name, bbox_extra_artists=[xlabel], bbox_inches='tight')


if __name__ == "__main__":
    main()
