import matplotlib.pyplot as plt

try:
    import prettyplotlib as ppl
except ImportError:
    ppl = plt


import numpy as np
import scipy.optimize as optimize
import g2 as g2
np.seterr(all="ignore")


types = ['indirect', 'indirect', 'direct', 'direct',
         'indirect', 'direct', 'direct', 'indirect',
         'antidirect', 'antidirect', 'antidirect']

labels = ['1_3 A-I', '3_5 A-I', '2_3 A-D', '1_6 A-D',
          '2_6 A-A/I', '4_5 A-D', '1_7 A-D', '2_7 A-D',
          '3_7 A-A/I', '5_7 A-A', '6_7 A-A']


names = ['1_3', '3_5', '2_3', '1_6', '2_6', '4_5', '1_7', '2_7', '3_7', '5_7', '6_7']

zeropoints = [171.6, 171.0, 171.5, 170.5, 171.1, 171.2, 171.2, 171.2, 171.2, 171.2, 171.2]


p0s = [
    [0.6, 1.1, 0.4, 0.5, 0],
    [0.6, 1.1, 0.4, 0.5, 0],
    [4, 1, 0.4, 0],
    [4, 1, 0.4, 0],
    [0.6, 1.1, 0.4, 0.5, 0],
    [4, 1, 0.4, 0],
    [4, 1, 0.4, 0],
    [0.6, 1.1, 0.4, 0.5, 0],
    [0.5, 0.5, 0],
    [0.5, 0.5, 0],
    [0.5, 0.5, 0]
]


def main():

    with open('output/fit_specific.md', "w") as file:
        file.write("")

    # for i in [5]:
    for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:

        name = names[i]
        label = labels[i]
        type = types[i]

        data = np.loadtxt('input/rebinned/%s.txt' % name, delimiter=",")
        time = data[:, 0] - zeropoints[i]
        counts = data[:, 1]

        idx = (time > -20) & (time < 20)
        time = time[idx]
        counts = counts[idx]
        counts_n = counts/counts.mean()

        if type == "direct":
            try:
                poptd, pcovd = optimize.curve_fit(g2.g2c_direct, time, counts_n, p0=p0s[i])
                perrd = np.sqrt(np.diag(pcovd))
            except RuntimeError:
                poptd = np.array([0., 0., 0., 0.])
                perrd = np.zeros_like(poptd)

        elif type == "indirect":
            try:
                popti, pcovi = optimize.curve_fit(g2.g2c_indirect, time, counts_n, p0=p0s[i])
                perri = np.sqrt(np.diag(pcovi))
            except RuntimeError:
                popti = np.array([0., 0., 0., 0., 0.])
                perri = np.zeros_like(popti)

        elif type == "antidirect":
            try:
                popta, pcova = optimize.curve_fit(g2.g2c_antidirect, time, counts_n, p0=p0s[i])
                perra = np.sqrt(np.diag(pcova))
            except RuntimeError:
                popta = np.array([0., 0., 0.])
                perra = np.zeros_like(popta)

        with open('output/fit_specific.md', "a") as file:
            file.write("\n# %s\n" % label)
            file.write('![](specific/specific_corrs%s.png)\n' % name)

            if type == "direct":
                file.write("## Direct\n")
                file.write("\tc1: %1.3lf +- %1.3lf\n" % (poptd[0], perrd[0]))
                file.write("\tl1: %1.3lf +- %1.3lf\n" % (poptd[1], perrd[1]))
                file.write("\tl2: %1.3lf +- %1.3lf\n" % (poptd[2], perrd[2]))

            elif type == "indirect":
                file.write("## Indirect\n")
                file.write("\tc1: %1.3lf +- %1.3lf\n" % (popti[0], perri[0]))
                file.write("\tl1: %1.3lf +- %1.3lf\n" % (popti[1], perri[1]))
                file.write("\tl3: %1.3lf +- %1.3lf\n" % (popti[2], perri[2]))
                file.write("\tl2: %1.3lf +- %1.3lf\n" % (popti[3], perri[3]))

            elif type == "antidirect":
                file.write("## Antidirect\n")
                file.write("\tl1: %1.3lf +- %1.3lf\n" % (popta[0], perra[0]))
                file.write("\tl2: %1.3lf +- %1.3lf\n" % (popta[1], perra[1]))

        # just plotting stuff now
        plt.close()
        ppl.plot(time, counts_n, linewidth=4, alpha=0.3)
        if type == "direct":
            ppl.plot(time, g2.g2c_direct(time, *poptd), label="Direct", linewidth=2)
        elif type == "indirect":
            ppl.plot(time, g2.g2c_indirect(time, *popti), label="Indirect", linewidth=2)
        elif type == "antidirect":
            ppl.plot(time, g2.g2c_antidirect(time, *popta), label="Antidirect", linewidth=2)

        plt.text(5, 0.1, label)
        plt.xlim([-15, 15])
        plt.ylim(ymin=0)

        ppl.legend()
        xlabel = plt.xlabel("$\\tau (ns)$")
        plt.ylabel("$g^{(2)}(\\tau)$")

        print "saving specific fits %s" % name
        plt.savefig('output/specific/specific_corrs%s.png' % name, bbox_extra_artists=[xlabel],
                    bbox_inches='tight')


if __name__ == "__main__":
    main()