import numpy as np
import matplotlib.pyplot as plt
import prettyplotlib as ppl
from markov import *

T = TransitionMatrix()

idx = T.evals.argsort()[::-1]
evals = T.evals[idx]
evecs = T.evecs[:, idx]

evalstring = ['%1.1lf' % e for e in evals]

pevecs = []

for evec in evecs:
    e = np.abs(evec)/np.abs(evec).max()
    pevecs.append(e)

pevecs = np.array(pevecs)

fig, ax = ppl.subplots(1)
# p = ax.pcolormesh(pevecs)
ppl.pcolormesh(fig, ax, pevecs)
# fig.colorbar(p)
plt.yticks(9-np.arange(9)-0.5,
           ['$0$', '$h$', '$\hat{h}$', '$X$', '$X^+$', '$\hat{X}_1^+$', '$\hat{X}_2^+$', '$XX$', '$XX^+$'])
plt.xticks(0.5+np.arange(9), evalstring)

plt.savefig('output/evecs.png')

plt.close()

fig, ax = ppl.subplots(1)
# p = ax.pcolormesh(pevecs)

ppl.pcolormesh(fig, ax, T.matrix)
# fig.colorbar(p)
# plt.yticks(9-np.arange(9)-0.5,
           # ['$0$', '$h$', '$\hat{h}$', '$X$', '$X^+$', '$\hat{X}_1^+$', '$\hat{X}_2^+$', '$XX$', '$XX^+$'])
# plt.xticks(0.5+np.arange(9), evalstring)

plt.savefig('output/matrix.png')
