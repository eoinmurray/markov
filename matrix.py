import numpy as np

# ansatz values
ce = 1.2
ch = 0.01
te = 1.
th = 0.4
lt5 = 0.44

t001 = 0.000040
t110 = 1.661768
t210 = 1.897675
t111t5 = 1.057866
t220 = 0.909169
t221t1 = 1.052696
t221t5 = 1.100000

A = 0.3
B = 1.0-A

empty = 0
groundhole = 1
twohole = 2
groundelectron = 3
excitedhole = 4
exciton = 5
posexciton = 6
biexciton = 7
chargedbiexciton = 8
excitedtrion = 9

T = np.matrix([
    [-1/th-1/te, 0, 0, 0, 0, 1/t110, 0, 0, 0, 0],  # empty
    [1/th, -ce/te-ch/th, 0, 0, 1/t001, 0, 1/t210, 0, 0, 0],  # ground hole
    [0, ch/th, -ce/te, 0, 0, 0, 0, 0, 0, 0],  # two hole
    [1/te, 0, 0, -1/th, 0, 0, 0, 0, 0, 0],  # ground electron
    [0, 0, 0, 0, -1/t001, 0, 0, 0, 0, 1/t111t5],  # excited hole
    [0, ce/te, 0, 1/th, 0, -1/t110-1/th, 0, 1/t220, 0, 0],  # exciton
    [0, 0, ce/te, 0, 0, 0.5/th, -ce/te-1/t210, 0, A/t221t1, 1/lt5],  # pos exc
    [0, 0, 0, 0, 0, 0, ce/te, -1/th-1/t220, 0, 0],  # biexc
    [0, 0, 0, 0, 0, 0, 0, 1/th, -A/t221t1-B/t221t5, 0],  # charged biex
    [0, 0, 0, 0, 0, 0.5/th, 0, 0, B/t221t5, -1/lt5-1/t111t5]  # l=5/2
])
