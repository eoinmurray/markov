import matplotlib.pyplot as plt
try:
    import prettyplotlib as ppl
except ImportError:
    ppl = plt

import brewer2mpl
set2 = brewer2mpl.get_map('Spectral', 'Diverging', 5).mpl_colors

import numpy as np
from names import *
np.seterr(all="ignore")


def all():
    for i in range(len(names)):
        name = names[i]
        label = labels[i]
        type = types[i]

        data = np.loadtxt('output/specific/data/fit_%s.txt' % name)

        time = data[:, 0]
        counts = data[:, 1]
        fit = data[:, 2]

        # just plotting stuff now
        plt.close()
        ppl.plot(time, counts, linewidth=4, alpha=0.3)
        ppl.plot(time, fit, label=type, linewidth=2)

        plt.text(5, 0.1, label)
        plt.xlim([-15, 15])
        plt.ylim(ymin=0)

        plt.legend(fontsize=8)
        xlabel = plt.xlabel("$\\tau (ns)$")
        plt.ylabel("$g^{(2)}(\\tau)$")

        plt.savefig('output/specific/plots/%s.png' % name,
                    bbox_extra_artists=[xlabel], bbox_inches='tight')


def subplots():
    data13 = np.loadtxt('output/specific/data/fit_1_3.txt')
    data16 = np.loadtxt('output/specific/data/fit_1_6.txt')
    data17 = np.loadtxt('output/specific/data/fit_1_7.txt')
    data23 = np.loadtxt('output/specific/data/fit_2_3.txt')
    data26 = np.loadtxt('output/specific/data/fit_2_6.txt')
    data27 = np.loadtxt('output/specific/data/fit_2_7.txt')
    data35 = np.loadtxt('output/specific/data/fit_3_5.txt')
    data37 = np.loadtxt('output/specific/data/fit_3_7.txt')
    data45 = np.loadtxt('output/specific/data/fit_4_5.txt')
    data67 = np.loadtxt('output/specific/data/fit_6_7.txt')
    data75 = np.loadtxt('output/specific/data/fit_7_5.txt')

    make_1_plot(data45, '45')
    print 'saving 45'

    make_2_plot(data17, data27, '17_27')
    print 'saving 17_27'

    make_4_plot(data16, data13, data26, data23, '16_13_26_23')
    print 'saving 16_13_26_23'

    make_4_plot(data35, data75, data37, data67, '35_75_37_67')
    print 'saving 35_75_37_67'


def make_4_plot(data1, data2, data3, data4, name):
    plt.close()
    plt.figure(figsize=(6, 4))

    ax1 = plt.subplot(221)
    ax1.plot(data1[:, 0], data1[:, 1], color=set2[4], linewidth=2, alpha=0.5)
    ax1.plot(data1[:, 0], data1[:, 2], color=set2[0], linewidth=2)
    plt.xticks([-15, -10, -5, 0, 5, 10, 15], fontsize=10)
    a = np.array(plt.yticks()[0])
    plt.yticks(a[1:-1], fontsize=10)

    ax2 = plt.subplot(222, sharey=ax1)
    ax2.plot(data2[:, 0], data2[:, 1], color=set2[4], linewidth=2, alpha=0.5)
    ax2.plot(data2[:, 0], data2[:, 2], color=set2[0], linewidth=2)
    plt.xticks([-15, -10, -5, 0, 5, 10, 15], fontsize=10)

    ax3 = plt.subplot(223, sharex=ax1)
    ax3.plot(data3[:, 0], data3[:, 1], color=set2[4], linewidth=2, alpha=0.5)
    ax3.plot(data3[:, 0], data3[:, 2], color=set2[0], linewidth=2)
    plt.xticks([-15, -10, -5, 0, 5, 10, 15], fontsize=10)
    a = np.array(plt.yticks()[0])
    plt.yticks(a[1:-1], fontsize=10)

    ax4 = plt.subplot(224, sharey=ax3, sharex=ax1)
    ax4.plot(data4[:, 0], data4[:, 1], color=set2[4], linewidth=2, alpha=0.5)
    ax4.plot(data4[:, 0], data4[:, 2], color=set2[0], linewidth=2)
    plt.xticks([-15, -10, -5, 0, 5, 10, 15], fontsize=10)

    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.setp(ax2.get_xticklabels(), visible=False)
    plt.setp(ax2.get_yticklabels(), visible=False)
    plt.setp(ax4.get_yticklabels(), visible=False)
    plt.subplots_adjust(None, None, None, None, 0, 0)

    ax1.set_ylabel('$g^{(2)}(\\tau)$', fontsize=14)
    ax4.set_xlabel('$\\tau$(ns)', fontsize=14)
    ax1.yaxis.set_label_coords(-0.2, -0.1)
    ax4.xaxis.set_label_coords(0, -0.1)

    a = name.split('_')
    ax1.text(0.18, 0.8, a[0][0] + '_' + a[0][1], fontsize=16,
             horizontalalignment='center', verticalalignment='center', transform=ax1.transAxes)
    ax2.text(0.18, 0.8, a[1][0] + '_' + a[1][1], fontsize=16,
             horizontalalignment='center', verticalalignment='center', transform=ax2.transAxes)
    ax3.text(0.18, 0.8, a[2][0] + '_' + a[2][1], fontsize=16,
             horizontalalignment='center', verticalalignment='center', transform=ax3.transAxes)
    ax4.text(0.18, 0.8, a[3][0] + '_' + a[3][1], fontsize=16,
             horizontalalignment='center', verticalalignment='center', transform=ax4.transAxes)

    plt.savefig('output/specific/plots/grouped_%s.png' % name, bbox_inches='tight', dpi=600)


def make_2_plot(data1, data2, name):
    plt.close()
    plt.figure(figsize=(6, 3))

    ax1 = plt.subplot(121)
    ax1.plot(data1[:, 0], data1[:, 1], color=set2[4], linewidth=2, alpha=0.5)
    ax1.plot(data1[:, 0], data1[:, 2], color=set2[0], linewidth=2)
    plt.xticks([-15, -10, -5, 0, 5, 10, 15], fontsize=10)
    plt.yticks(fontsize=10)

    ax2 = plt.subplot(122, sharey=ax1)
    ax2.plot(data2[:, 0], data2[:, 1], color=set2[4], linewidth=2, alpha=0.5)
    ax2.plot(data2[:, 0], data2[:, 2], color=set2[0], linewidth=2)
    plt.xticks([-15, -10, -5, 0, 5, 10, 15], fontsize=10)

    plt.setp(ax2.get_yticklabels(), visible=False)
    plt.subplots_adjust(None, None, None, None, 0, None)

    ax1.set_ylabel('$g^{(2)}(\\tau)$', fontsize=14)
    ax2.set_xlabel('$\\tau$(ns)', fontsize=14)
    ax2.xaxis.set_label_coords(0, -0.1)

    a = name.split('_')
    ax1.text(0.18, 0.9, a[0][0] + '_' + a[0][1], fontsize=16,
             horizontalalignment='center', verticalalignment='center', transform=ax1.transAxes)
    ax2.text(0.18, 0.9, a[1][0] + '_' + a[1][1], fontsize=16,
             horizontalalignment='center', verticalalignment='center', transform=ax2.transAxes)

    plt.savefig('output/specific/plots/grouped_%s.png' % name, bbox_inches='tight', dpi=600)


def make_1_plot(data1, name):
    plt.close()
    plt.figure(figsize=(6, 3))

    ax1 = plt.subplot(111)
    ax1.plot(data1[:, 0], data1[:, 1], color=set2[4], linewidth=2, alpha=0.5)
    ax1.plot(data1[:, 0], data1[:, 2], color=set2[0], linewidth=2)
    plt.xticks([-15, -10, -5, 0, 5, 10, 15], fontsize=10)
    plt.yticks(fontsize=10)

    ax1.set_ylabel('$g^{(2)}(\\tau)$', fontsize=14)
    ax1.set_xlabel('$\\tau$(ns)', fontsize=14)

    a = name
    ax1.text(0.18, 0.9, a[0] + '_' + a[1], fontsize=16,
             horizontalalignment='center', verticalalignment='center', transform=ax1.transAxes)
    plt.savefig('output/specific/plots/grouped_%s.png' % name, bbox_inches='tight', dpi=600)


if __name__ == "__main__":
    # all()
    subplots()
