import matplotlib.pyplot as pyplot
from math import tanh
font = {'family': 'Times New Roman',
        'weight': 'normal',
        'size': 15,
        }
pyplot.figure()
# 1
k11 = 0.5
k22 = 0.5
k33 = 0.5
k23 = 0.5
k12 = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
k13 = [0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85]
r0 = 3
beta = 10
vcost = 1
icost = 5
x = []
line1 = []
for i in range(0, 100):
    x.append(i / 100)
for k in range(0, 100):
    k = k / 100
    line1.append(
        (1 - 1 / r0 * (1 + (k / k12[0]) * (tanh(0.5 * beta * vcost) / tanh(0.5 * beta * (icost - vcost))))) * 100)

scatter1 = [46.76, 44.78, 42.2, 40.3, 38.12, 36.32, 33.42, 31.58, 29.52, 25.99, 22.89, 21.02, 17.1, 14.63, 11.82]

pyplot.subplot(3, 1, 1)
p1 = pyplot.plot(x, line1)
pyplot.scatter(k13, scatter1)
pyplot.legend(['$r_0=3$'])
pyplot.text(0.78,52,'(a)')

# 2
k11 = 0.5
k22 = 0.5
k33 = 0.5
k23 = 0.5
k12 = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
k13 = [0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85]
r0 = 4
beta = 10
vcost = 1
icost = 5
x = []
line2 = []
for i in range(0, 100):
    x.append(i / 100)
for k in range(0, 100):
    k = k / 100
    line2.append(
        (1 - 1 / r0 * (1 + (k / k12[0]) * (tanh(0.5 * beta * vcost) / tanh(0.5 * beta * (icost - vcost))))) * 100)

scatter2 = [60.5, 58.9, 57.44, 55.67, 53.91, 52.2, 50.74, 50.26, 48.32, 46.98, 44.92, 42.74, 41.04, 39.86, 37.28]

pyplot.subplot(3, 1, 2)
p2 = pyplot.plot(x, line2)
pyplot.scatter(k13, scatter2)
pyplot.legend(['$r_0=4$'])
pyplot.text(0.78,64,'(b)')
pyplot.ylabel('Final Vaccination Level',font)

# 3
k11 = 0.5
k22 = 0.5
k33 = 0.5
k23 = 0.5
k12 = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
k13 = [0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85]
r0 = 5
beta = 10
vcost = 1
icost = 5
x = []
line3 = []
for i in range(0, 100):
    x.append(i / 100)
for k in range(0, 100):
    k = k / 100
    line3.append(
        (1 - 1 / r0 * (1 + (k / k12[0]) * (tanh(0.5 * beta * vcost) / tanh(0.5 * beta * (icost - vcost))))) * 100)

scatter3 = [68.04, 66.62, 65.44, 64.43, 63.72, 62.3, 61.46, 60.18, 59.04, 57.18, 55.48, 53.98, 52.32, 51.46, 50.76]

pyplot.subplot(3, 1, 3)
p3 = pyplot.plot(x, line3)
pyplot.scatter(k13, scatter3)
pyplot.legend(['$r_0=5$'])
pyplot.text(0.78,73,'(c)')
pyplot.xlabel('$k_{VI}$',font)
pyplot.show()
'''
# 4
k11 = 0.5
k22 = 0.5
k33 = 0.5
k23 = 0.5
k12 = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
k13 = [0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85]
r0 = 6
beta = 10
vcost = 1
icost = 5
x = []
line4 = []
for i in range(0, 100):
    x.append(i / 100)
for k in range(0, 100):
    k = k / 100
    line4.append(
        (1 - 1 / r0 * (1 + (k / k12[0]) * (tanh(0.5 * beta * vcost) / tanh(0.5 * beta * (icost - vcost))))) * 100)

scatter4 = [73.34, 72.12, 71.28, 70.02, 69.28, 67.94, 66.78, 65.76, 64.96, 63.9, 63.34, 62.42, 61.24, 60.07, 59.2]

pyplot.subplot(2, 2, 1)
p4 = pyplot.plot(x, line4)
pyplot.scatter(k13, scatter4)
pyplot.legend(['$r_0=6$'])
pyplot.xlabel('$k_13$')
pyplot.ylabel('Final Vaccination Level')
'''
