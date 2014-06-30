import numpy as np
import matplotlib.pyplot as plt
import brewer2mpl
from scipy.optimize import curve_fit

set2 = brewer2mpl.get_map('Spectral', 'Diverging', 5).mpl_colors


fig, ax = plt.subplots(figsize=(8, 4), dpi=600)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

ax.yaxis.label.set_size(18)
ax.xaxis.label.set_size(18)
ax.ticklabel_format(useOffset=False)
plt.setp(ax.spines.values(), alpha=0.5)
plt.tick_params(axis='both', which='major', labelsize=16)

data = np.loadtxt("input/A1208_28_05_14/02/lifetimes_1_2.txt", delimiter=",")
data1 = np.loadtxt("input/A1208_28_05_14/02/lifetimes_1_3.txt", delimiter=",")


def func(t, tau, intensity):
    return intensity*np.exp(-t/tau)

t = data[:, 0] - 190
indices = (t > -3.4) & (t < 7.6)

t = t[indices]

xx = data[indices, 1]
x = data[indices, 2]
xn1 = data1[indices, 2]
xn2 = data1[indices, 4]

xn1 = np.append(xn1, xn1[t < 0])
xn2 = np.append(xn2, xn2[t < 0])

tneg = t[t < 0]
tmod = np.append(t, t.max() + np.abs(tneg[::-1]))

indices = (t > 0)
indicesmod = (tmod > 0)

x = x[indices]
xx = xx[indices]
xn1 = xn1[indicesmod]
xn2 = xn2[indicesmod]

t = t[t>0]
tmod = tmod[tmod>0]

poptx, pcovx = curve_fit(func, t[t > 1.5], x[t > 1.5], p0=[2, x.max()])
plt.plot(t, x, label="$X$")
plt.plot(t[t > 1.5], func(t[t > 1.5], *poptx))

poptxx, pcovxx = curve_fit(func, t[t > 1.5], xx[t > 1.5], p0=[1, xx.max()])
plt.plot(t, xx, label="$XX$")
plt.plot(t[t > 1.5], func(t[t > 1.5], *poptxx))

poptxn1, pcovxn1 = curve_fit(func, tmod[tmod > 1.5], xn1[tmod > 1.5], p0=[10, xn1.max()])
plt.plot(tmod, xn1, label="$X_1^-$")
plt.plot(tmod[tmod > 1.5], func(tmod[tmod > 1.5], *poptxn1))

poptxn2, pcovxn2 = curve_fit(func, tmod[tmod > 1.5], xn2[tmod > 1.5], p0=[10, xn2.max()])
plt.plot(tmod, xn2, label="$X_1^-$")
plt.plot(tmod[tmod > 1.5], func(tmod[tmod > 1.5], *poptxn2))


pcovx = np.sqrt(np.diag(pcovx))
pcovxx = np.sqrt(np.diag(pcovxx))
pcovxn1 = np.sqrt(np.diag(pcovxn1))
pcovxn2 = np.sqrt(np.diag(pcovxn2))

plt.xlim([0, 10])
plt.yticks([])
xlabel = plt.xlabel('Delay time  (ns)')
plt.ylabel('Intensity [a.u.]')

plt.legend([
    "$X$ - %1.2lf [%1.2lf] (ns)" % (poptx[0], pcovx[0]),
    "$XX$ - %1.2lf [%1.2lf] (ns)" % (poptxx[0], pcovxx[0]),
    "$X^-_2$ - %1.2lf [%1.2lf] (ns)" % (poptxn1[0], pcovxn1[0]),
    "$X^-_2$ - %1.2lf [%1.2lf] (ns)" % (poptxn2[0], pcovxn2[0]),
])

plt.savefig('temp/lifetimes.png', bbox_extra_artists=[xlabel], bbox_inches='tight')
