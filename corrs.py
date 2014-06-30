import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimize
import brewer2mpl
import g2 as g2

set2 = brewer2mpl.get_map('Spectral', 'Diverging', 5).mpl_colors
np.seterr(all="ignore")

with open('output/fit.md', "w") as file:
    file.write("")

names = ['1_3', '3_5', '2_3', '1_6', '2_6', '4_5']
states = ["XXT5", "XXT1", "XP", "XX", "X", "XT5"]
labels = ["XXT5_XP", "XP_X", "XXT1_XP", "XXT5_XT5", "XXT1_XT5", "XX_X"]

fmaxs = [1.4, 1.1]

def gauss(t):
    """Generates gaussian for convolutionz"""
    c = 0.3
    a = 1.0/np.sqrt(2*np.pi*(c**2))
    b = 0
    return a*np.exp(-((t-b)**2)/(2*c**2))

foos = [
    g2.g2c_complicated,
    g2.g2c_complicated,
    g2.g2c,
    g2.g2c,
    g2.g2c_auto,
    g2.g2c]

p0s = [
    [0.6, 1.1, 0.4, 0.5, 0],
    [0.6, 1.1, 0.4, 0.5, 0],
    [4, 1, 0.4, 0],
    [4, 1, 0.4, 0],
    [1, 0.4, 0],
    [4, 1, 0.4, 0]
]

zeropoints = [171.6, 171.0, 171.5, 170.5, 171.1, 171.2]

for i in [0, 1, 2, 3, 4, 5]:

    name = names[i]
    foo = foos[i]
    p0 = p0s[i]
    label = labels[i]

    data = np.loadtxt('input/%s.txt' % name, delimiter=",")
    time = data[:, 0] - zeropoints[i]
    counts = data[:, 1]

    idx = (time > -20) & (time < 20)
    time = time[idx]
    counts = counts[idx]
    counts_n = counts/counts.mean()

    if name == "2_6":
        popt2, pcov2 = optimize.curve_fit(g2.g2c_complicated, time, counts_n, p0=[0.6, 1.1, 0.4, 0.5, 0])
        popt3, pcov3 = optimize.curve_fit(g2.g2c, time, counts_n, p0=[4, 1, 0.4, 0],)

    popt, pcov = optimize.curve_fit(foo, time, counts_n, p0=p0)
    std_err = np.sqrt(np.diag(pcov))

    with open('output/fit.md', "a") as file:
        file.write("\n" + name + "\n")

        for j in xrange(len(popt)):
            param = popt[j]
            std_err = np.sqrt(np.diag(pcov))
            err = std_err[j]
            file.write("\t%1.3lf +- %1.3lf\n" % (param, err))

        if name == "2_6":

            file.write("\n # Indirect")
            for j in xrange(len(popt2)):
                param = popt2[j]
                std_err = np.sqrt(np.diag(pcov2))
                err = std_err[j]
                file.write("\t%1.3lf +- %1.3lf\n" % (param, err))

            file.write("\n # Direct")
            for j in xrange(len(popt3)):
                param = popt3[j]
                std_err = np.sqrt(np.diag(pcov3))
                err = std_err[j]
                file.write("\t%1.3lf +- %1.3lf\n" % (param, err))

    # just plotting stuff now
    plt.close()
    plt.grid()
    plt.plot(time, counts_n, linewidth=3, color=set2[0])
    plt.text(5, 0.1, label)
    plt.text(5, 0.6, name)

    if name == "2_6":
        plt.plot(time, g2.g2c_complicated(time, *popt2), label="fit", linewidth=3, color='g')
        plt.plot(time, g2.g2c(time, *popt3), label="fit", linewidth=3, color='k')

    plt.plot(time, foo(time, *popt), label="fit", linewidth=3, color=set2[4])
    plt.xlim([-15, 15])
    plt.ylim(ymin=0)

    xlabel = plt.xlabel("$\\tau (ns)$")
    ylabel = plt.ylabel("$g^{(2)}(\\tau)$")

    print "saving output/corrs%s.png" % label
    plt.savefig('output/corrs%s.png' % label, bbox_extra_artists=[xlabel], bbox_inches='tight')
