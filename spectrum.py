
import numpy as np
import matplotlib.pyplot as plt
import brewer2mpl

# global plot settings
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
# plt.tight_layout()

data = np.loadtxt('input/raw/A1208 RTD spectrum.dat')

wavelength = data[:, 0]
intensity = data[:, 1]
max_intensity = 1.2*intensity.max()
energy = (1000)*1239.84187/wavelength  # eV from wiki page on electronvolt

peak_positions = [
    1386.3,
    1386.85,
    1387.3,
    1390.58,
    1391.2,
    1391.89,
    1392.55,
]

# names = [
#     "$X_{T5/2}+$",
#     "$X$",
#     "$XX$",
#     "$X+$",
#     "$XX_{T1/2}+$",
#     "$XX_{T5/2}+$"
# ]

names = [
    "7",
    "6",
    "5",
    "4",
    "3",
    "2",
    "1"
]


heights = [0.3, 0.5, 0.7, 0.5, 0.9, 0.5, 0.7]

for i in xrange(len(peak_positions)):
    pos = peak_positions[i]
    plt.vlines(pos, 0, max_intensity*(heights[i]-0.02), color=set2[0], alpha=0.3)
    plt.text(pos-0.25, max_intensity*(heights[i]), "$%1.1lf$" % pos, alpha=1, size=12)
    plt.text(pos-0.25, max_intensity*(heights[i]+0.065), names[i], alpha=1, size=12)

plt.fill_between(energy, intensity, color=set2[4])


plt.xlim([1385.5, 1393])
plt.ylim([0, max_intensity])

plt.yticks([])

xlabel = plt.xlabel("Energy ($meV$)")
plt.ylabel("Intensity (a.u.)")

plt.savefig('output/spectrum.png', bbox_extra_artists=[xlabel], bbox_inches='tight')
