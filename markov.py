"""
    markov.py

    Containes the TransitionMatrix class and the MarkovExpansionState class.
"""


import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt
import brewer2mpl
from names import *
import os

set2 = brewer2mpl.get_map('Spectral', 'Diverging', 5).mpl_colors
np.seterr(all='ignore')


def gauss(t):
    """Generates gaussian for convolution"""
    c = 0.3
    a = 1.0/np.sqrt(2*np.pi*(c**2))
    b = 0
    return a*np.exp(-((t-b)**2)/(2*c**2))


# States
empty = 0
groundhole = 1
excitedhole = 2
exciton = 3
groundtrion = 4
hottrion1 = 5  # state that emits #6 and #7 and spin flips.
hottrion2 = 6  # state that relaxes quickly to groundtrion.
biexciton = 7
chargedbiexciton = 8


class TransitionMatrix():

    def __init__(self, th=1.48, tpe=1.0, gsf=2.0, geh=10.0, t001=0.001):
        # electron hole capture times.
        self.th = th
        # electron hole capture times in positive QD.
        self.tpe = tpe
        # spin flip time
        self.gsf = gsf
        # time for ground hole to be excited.
        self.geh = geh

        # lifetimes.

        self.t001 = t001  # excited hole relaxation time.
        self.t110 = 1.66  # exciton lifetime (emission #5).
        self.t120 = 1.86  # ground trion lifetime (emission #3).
        self.t1116 = 1.33  # hot trion 1 relax to ground hole (emission #6).
        self.t1117 = 1.33  # hot trion 1 relax to excited hole (emission #7).
        self.t220 = 0.97  # biexciton lifetime (emission #4).
        self.t2211 = 1.03  # charged biexciton to hot trion 1 (emision #1).
        self.t2212 = 1.18  # charged biexciton to hot trion 2 (emision #2).

        s = self
        self.T = np.matrix([
            [-1.0/s.th, 0, 0, 1.0/s.t110, 0, 0, 0, 0, 0],
            [1.0/s.th, -1.0/s.tpe, 1.0/s.t001, 0, 1.0/s.t120, 1.0/s.t1116, 0, 0, 0],
            [0, 0, -1.0/s.t001, 0, 0, 1.0/s.t1117, 0, 0, 0],
            [0, 1.0/s.tpe, 0, -1.0/s.th-1.0/s.t110, 0, 0, 0, 1.0/s.t220, 0],
            [0, 0, 0, 1.0/s.th, -1.0/s.t120-1.0/s.geh-1.0/s.tpe, 1.0/s.gsf, 1.0/s.t001, 0, 0],
            [0, 0, 0, 0, 1.0/s.geh, -1.0/s.t1116-1.0/s.t1117-1.0/s.gsf, 0, 0, (2.0/3)*(1.0/s.t2211)],
            [0, 0, 0, 0, 0, 0, -1.0/s.t001, 0, (1.0/3)*(1.0/s.t2212)],
            [0, 0, 0, 0, 1.0/s.tpe, 0, 0, -1.0/s.th-1.0/s.t220, 0],
            [0, 0, 0, 0, 0, 0, 0, 1.0/s.th, -(2.0/3)*(1.0/s.t2211)-(1.0/3)*(1.0/s.t2212)]
        ])

        self.matrix = self.T

        e = linalg.eig(self.matrix)
        self.evals = e[0]
        self.evecs = e[1]

    def __getitem__(self, key, val):
        return getattr(self, key)


class MarkovExpansionState(TransitionMatrix):

    def __init__(self, statei, statef):
        TransitionMatrix.__init__(self)

        self.statei = statei
        self.statef = statef

        evecs = self.evecs
        evals = self.evals

        a = self.matrix
        b = np.zeros(self.matrix.shape[0])
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

        # we need to set the small eigenvalues to zero
        # in order to find the stationary eigenvalue
        self.l.real[np.abs(self.l.real) < 1e-5] = 0
        self.l.imag[np.abs(self.l.imag) < 1e-5] = 0

        self.asteady = self.a[self.l == 0][0].real

        def foo(t):
            s = [self.a[i]*np.exp(self.l[i]*t) for i in xrange(self.a.size)]
            return np.sum(s)/self.asteady

        self._foo = np.vectorize(foo)

    def __str__(self):
        a = self.a
        l = self.l

        asteady = a[l == 0][0].real

        s = []
        for j in xrange(a.size):
            ar = a[j].real/asteady
            ai = a[j].imag/asteady
            lr = l[j].real
            li = l[j].imag

            if self.filter(ar, ai, lr, li):
                a_s = '\t{:3d} | a: {:8.3f} + {:8.3f}i \t l: {:8.3f} + {:8.3f}i' .format(1+j, ar, ai, lr, li)
                s.append(a_s)

        return '\n'.join(s)

    def filter(self, ar, ai, lr, li):
        if np.abs(ar) < 0.1 and np.abs(ai) < 0.1:
            return False
        if np.abs(lr) > 5.0 and np.abs(li) > 5.0:
            return False
        return True

    def __call__(self, t):
        return self._foo(t)


if __name__ == '__main__':

    if not os.path.exists('output/spectral/'):
        os.makedirs('output/spectral/')

    with open('output/markov.md', 'w') as file:
        file.write('')

    TM = TransitionMatrix()

    for i in range(9):
        s = TM.matrix[:, i].sum()
        assert np.abs(s) < 1e-6, 'Column %s does not sum to zero, actually: %1.5lf.' % (i, s)
    print 'All columns sum to 0.0'

    t = np.linspace(0, 20, 400)
    tau = np.concatenate((-t[::-1], t[1:-1]), axis=0)
    gaussed = gauss(tau)

    pairs = [
        [chargedbiexciton, hottrion1],  # 1
        [chargedbiexciton, hottrion2],  # 2
        [groundtrion, groundhole],  # 3
        [biexciton, exciton],  # 4
        [exciton, empty],  # 5
        [hottrion1, groundhole],  # 6
        [hottrion1, excitedhole],  # 7
    ]

    for i in range(len(peaks)):
        ppair = pairs[peaks[i][0]-1]
        npair = pairs[peaks[i][1]-1]

        stateip = ppair[0]
        statefp = ppair[1]

        statein = npair[0]
        statefn = npair[1]

        pspec = MarkovExpansionState(statefp, statein)
        nspec = MarkovExpansionState(statefn, stateip)

        name = '%s_%s' % (peaks[i][0], peaks[i][1])
        with open('output/markov.md', 'a') as file:
            file.write('\n# %s\n' % name)
            file.write('![](spectral/%s.png)' % name)
            file.write('\n\n## tau > 0\n')
            file.write(str(pspec))
            file.write('\n## tau < 0\n')
            file.write(str(nspec))
            file.write('\n')

        plt.close()
        g2 = np.concatenate((nspec(t)[::-1], pspec(t)[1:-1]), axis=0)
        g2c = np.convolve(gaussed/gaussed.sum(), g2, 'same')
        plt.plot(tau, g2)
        plt.plot(tau, g2c)
        plt.text(3, 0.3, '%s' % name)
        plt.ylim(ymin=0)
        plt.xlim([-15, 15])

        print 'saving output/spectral/%s.png' % name
        plt.savefig('output/spectral/%s.png' % name, bbox_inches='tight')
