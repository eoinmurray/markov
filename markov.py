import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt
import brewer2mpl
from matrix import *

set2 = brewer2mpl.get_map('Spectral', 'Diverging', 5).mpl_colors
np.seterr(all="ignore")


def gauss(t):
    """Generates gaussian for convolutionz"""
    c = 0.3
    a = 1.0/np.sqrt(2*np.pi*(c**2))
    b = 0
    return a*np.exp(-((t-b)**2)/(2*c**2))

class MarkovExpansionState():

    def __init__(self, statei, statef):
        self.statei = statei
        self.statef = statef

        evecs = linalg.eig(T)[1]
        evals = linalg.eig(T)[0]

        a = T
        b = np.zeros(T.shape[0])
        b[statei] = 1
        b = np.asmatrix(b).T
        c = linalg.solve(evecs, b)

        intensities = []
        eigenvalues = []

        for i in xrange(c.size):
            a = evecs[:, i][statef]*c[i]
            intensities.append(a)
            eigenvalues.append(evals[i])

        self.a = np.array(intensities).flatten()
        self.l = np.array(eigenvalues).flatten()

        self.a.real[np.abs(self.a.real) < 1e-3] = 0
        self.a.imag[np.abs(self.a.imag) < 1e-3] = 0
        self.l.real[np.abs(self.l.real) < 1e-3] = 0
        self.l.imag[np.abs(self.l.imag) < 1e-3] = 0

        self.asteady = self.a[self.l == 0][0].real

        def foo(t):
            s = [self.a[i]*np.exp(self.l[i]*t) for i in xrange(self.a.size)]
            return np.sum(s)/self.asteady

        self._foo = np.vectorize(foo)

    def __str__(self):
        a = self.a
        l = self.l

        a.real[np.abs(a.real) < 1e-3] = 0
        a.imag[np.abs(a.imag) < 1e-3] = 0
        l.real[np.abs(l.real) < 1e-3] = 0
        l.imag[np.abs(l.imag) < 1e-3] = 0

        asteady = a[l == 0][0].real

        s = []
        for j in xrange(a.size):
            a_s = "a: %1.3lf + %1.3lfi" % (a[j].real/asteady, a[j].imag/asteady)
            l_s = "l: %1.3lf + %1.3lfi \t%d" % (l[j].real, l[j].imag, 1+j)
            s.append(a_s + "\t" + l_s)

        return "\n".join(s)

    def __call__(self, t):
        return self._foo(t)


if __name__ == "__main__":

    labels = ["XXT5 -> X+", "XXT1 -> X+", "XXT5 -> XT5", "XXT1 -> XT5", "X+ -> X", "XX -> X"]
    t = np.linspace(0, 20, 400)
    tau = np.concatenate((-t[::-1], t[1:-1]), axis=0)

    # XXT5 -> X+
    state_pos = MarkovExpansionState(excitedtrion, posexciton)
    state_neg = MarkovExpansionState(groundhole, chargedbiexciton)
    gxxt5_xp = np.concatenate((state_neg(t)[::-1], state_pos(t)[1:-1]), axis=0)

    # XX -> X
    state_pos = MarkovExpansionState(exciton, exciton)
    state_neg = MarkovExpansionState(empty, biexciton)
    gxx_x = np.concatenate((state_neg(t)[::-1], state_pos(t)[1:-1]), axis=0)

    # XXT5 -> XT5
    state_pos = MarkovExpansionState(excitedtrion, excitedtrion)
    state_neg = MarkovExpansionState(excitedhole, chargedbiexciton)
    gxxt5_xt5 = np.concatenate((state_neg(t)[::-1], state_pos(t)[1:-1]), axis=0)

    # XXT1 -> XT5
    state_pos = MarkovExpansionState(posexciton, excitedtrion)
    state_neg = MarkovExpansionState(excitedhole, chargedbiexciton)
    gxxt1_xt5 = np.concatenate((state_neg(t)[::-1], state_pos(t)[1:-1]), axis=0)

    # XXT1 -> XP
    state_pos = MarkovExpansionState(posexciton, posexciton)
    state_neg = MarkovExpansionState(groundhole, chargedbiexciton)
    gxxt1_xp = np.concatenate((state_neg(t)[::-1], state_pos(t)[1:-1]), axis=0)

    # XP -> X
    state_pos = MarkovExpansionState(groundhole, exciton)
    state_neg = MarkovExpansionState(empty, posexciton)
    gxp_x = np.concatenate((state_neg(t)[::-1], state_pos(t)[1:-1]), axis=0)


    # lets convolute all our g's.
    gaussed = gauss(tau)
    gxxt5_xp = np.convolve(gaussed/gaussed.sum(), gxxt5_xp, 'same')
    gxx_x = np.convolve(gaussed/gaussed.sum(), gxx_x, 'same')
    gxxt5_xt5 = np.convolve(gaussed/gaussed.sum(), gxxt5_xt5, 'same')
    gxxt1_xt5 = np.convolve(gaussed/gaussed.sum(), gxxt1_xt5, 'same')
    gxxt1_xp = np.convolve(gaussed/gaussed.sum(), gxxt1_xp, 'same')
    gxp_x = np.convolve(gaussed/gaussed.sum(), gxp_x, 'same')

    # make the plots
    def makePlot(x, y, l):
        plt.plot(x,y)
        plt.text(3, 0.3, l)
        plt.ylim(ymin=0)
        plt.xlim([-15, 15])

    plt.subplot(321)
    makePlot(tau, gxxt5_xp, "$XXT5 \\rightarrow XP$")

    plt.subplot(322)
    makePlot(tau, gxx_x, "$XX \\rightarrow X$")

    plt.subplot(323)
    makePlot(tau, gxxt5_xt5, "$XXT5 \\rightarrow XT5$")

    plt.subplot(324)
    makePlot(tau, gxxt1_xt5, "$XXT1 \\rightarrow XT5$")

    plt.subplot(325)
    makePlot(tau, gxxt1_xp, "$XXT1 \\rightarrow XP$")

    plt.subplot(326)
    makePlot(tau, gxp_x, "$XP \\rightarrow X$")

    plt.savefig('output/markov.png', bbox_inches='tight')
