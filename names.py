
names = ['1_3', '3_5', '2_3', '1_6', '2_6', '4_5', '1_7', '2_7', '3_7', '5_7', '6_7', '7_5']

types = ['indirect', 'indirect', 'direct', 'direct',
         'indirect', 'direct', 'direct', 'indirect',
         'antidirect', 'antidirect', 'antidirect', 'indirect']

zeropoints = [171.6, 171.0, 171.5, 170.5, 171.1, 171.2, 171.2, 171.2, 171.2, 171.2, 171.2, 171.2]


peaks = []
for name in names:
    a = int(name.split('_')[0])
    b = int(name.split('_')[1])
    peaks.append([a, b])

labels = []
for i in range(len(names)):
    l = names[i]
    t = types[i]
    if t == "direct":
        l = l + ' A-D'
    if t == "indirect":
        l = l + ' A-I'
    if t == "antidirect":
        l = l + ' A-A'
    labels.append(l)
