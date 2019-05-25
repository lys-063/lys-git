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
k12 = 0.8
k13 = 0.8
r0 = 3

vcost = 1
icost = 5
line1 = []
for beta in range(50, 1000):
    beta = beta / 100
    line1.append(
        (1 - 1 / r0 * (1 + (k13 / k12) * (tanh(0.5 * beta * vcost) / tanh(0.5 * beta * (icost - vcost))))) * 100)

vcost = 3.5
icost = 5
line2 = []
for beta in range(50, 1000):
    beta = beta / 100
    line2.append(
        (1 - 1 / r0 * (1 + (k13 / k12) * (tanh(0.5 * beta * vcost) / tanh(0.5 * beta * (icost - vcost))))) * 100)

beta = [0.5, 1, 1.5, 2, 2.5, 3, 4, 6, 8, 10]
scatter1 = [54.75, 49.58, 44.45, 40.64, 36.13, 35.7, 31.86, 31.28, 30.32, 30.41]
scatter2 = [8.64, 11.36, 21.9, 26.483333333333334, 29.78, 31.16, 30.5, 31.8, 30.51, 31.22]

x = []
for i in range(50, 1000):
    x.append(i / 100)

pyplot.subplot(3, 1, 1)
p1 = pyplot.plot(x, line1)
p2 = pyplot.plot(x, line2)
pyplot.scatter(beta, scatter1)
pyplot.scatter(beta, scatter2)
pyplot.legend(['C=5,V=1', 'C=5,V=3.5'])
pyplot.text(9,50,'(a) $r_0=3$')

# 2
k11 = 0.5
k22 = 0.5
k33 = 0.5
k23 = 0.5
k12 = 0.8
k13 = 0.8
r0 = 4

vcost = 1
icost = 5
line1 = []
for beta in range(50, 1000):
    beta = beta / 100
    line1.append(
        (1 - 1 / r0 * (1 + (k13 / k12) * (tanh(0.5 * beta * vcost) / tanh(0.5 * beta * (icost - vcost))))) * 100)

vcost = 3.5
icost = 5
line2 = []
for beta in range(50, 1000):
    beta = beta / 100
    line2.append(
        (1 - 1 / r0 * (1 + (k13 / k12) * (tanh(0.5 * beta * vcost) / tanh(0.5 * beta * (icost - vcost))))) * 100)

beta = [0.5, 1, 1.5, 2, 2.5, 3, 4, 6, 8, 10]
scatter1 = [66.4, 62.31666666666667, 58.733333333333334, 55.03333333333333, 53.53333333333333, 52.03333333333333,
            50.333333333333336, 50.03333333333333, 50.166666666666664, 49.95]
scatter2 = [19.416666666666668, 37.53333333333333, 44.266666666666666, 47.233333333333334, 48.43333333333333,
            50.083333333333336, 49.7, 49.68333333333333, 49.766666666666666, 49.9]

x = []
for i in range(50, 1000):
    x.append(i / 100)

pyplot.subplot(3, 1, 2)
p1 = pyplot.plot(x, line1)
p2 = pyplot.plot(x, line2)
pyplot.scatter(beta, scatter1)
pyplot.scatter(beta, scatter2)
pyplot.legend(['C=5,V=1', 'C=5,V=3.5'])
pyplot.text(9,61,'(b) $r_0=4$')
pyplot.ylabel('Final Vaccination Level',font)

# 3
k11 = 0.5
k22 = 0.5
k33 = 0.5
k23 = 0.5
k12 = 0.8
k13 = 0.8
r0 = 5

vcost = 1
icost = 5
line1 = []
for beta in range(50, 1000):
    beta = beta / 100
    line1.append(
        (1 - 1 / r0 * (1 + (k13 / k12) * (tanh(0.5 * beta * vcost) / tanh(0.5 * beta * (icost - vcost))))) * 100)

vcost = 3.5
icost = 5
line2 = []
for beta in range(50, 1000):
    beta = beta / 100
    line2.append(
        (1 - 1 / r0 * (1 + (k13 / k12) * (tanh(0.5 * beta * vcost) / tanh(0.5 * beta * (icost - vcost))))) * 100)

beta = [0.5, 1, 1.5, 2, 2.5, 3, 4, 6, 8, 10]
scatter1 = [73.64, 70.4, 67.02, 64.36, 62.96, 61.82, 60.7, 59.75, 60.14, 60.21]
scatter2 = [37.26, 49.39, 54.65, 57.8, 58.76, 59.39, 59.44, 60.26, 59.28, 59.72]

x = []
for i in range(50, 1000):
    x.append(i / 100)

pyplot.subplot(3, 1, 3)
p1 = pyplot.plot(x, line1)
p2 = pyplot.plot(x, line2)
pyplot.scatter(beta, scatter1)
pyplot.scatter(beta, scatter2)
pyplot.legend(['C=5,V=1', 'C=5,V=3.5'])
pyplot.text(9,70,'(c) $r_0=4$')
pyplot.xlabel('Selection Intensity',font)
# pyplot.ylabel('Final Vaccination Level')
'''
# 4
k11 = 0.5
k22 = 0.5
k33 = 0.5
k23 = 0.5
k12 = 0.8
k13 = 0.5
r0 = 5

vcost = 1
icost = 5
line1 = []
for beta in range(50, 1000):
    beta = beta / 100
    line1.append(
        (1 - 1 / r0 * (1 + (k13 / k12) * (tanh(0.5 * beta * vcost) / tanh(0.5 * beta * (icost - vcost))))) * 100)

vcost = 3.5
icost = 5
line2 = []
for beta in range(50, 1000):
    beta = beta / 100
    line2.append(
        (1 - 1 / r0 * (1 + (k13 / k12) * (tanh(0.5 * beta * vcost) / tanh(0.5 * beta * (icost - vcost))))) * 100)

beta = [0.5, 1, 1.5, 2, 2.5, 3, 4, 6, 8, 10]
scatter1 = [78.03333333333333, 75.0, 72.9, 70.0, 69.5, 67.33333333333333, 66.46666666666667, 66.33333333333333,
            66.16666666666667, 65.96666666666667]
scatter2 = [49.266666666666666, 58.233333333333334, 62.233333333333334, 63.86666666666667, 64.93333333333334,
            66.36666666666666, 65.8, 66.03333333333333, 66.36666666666666, 66.3]

x = []
for i in range(50, 1000):
    x.append(i / 100)

pyplot.subplot(4, 1, 4)
p1 = pyplot.plot(x, line1)
p2 = pyplot.plot(x, line2)
pyplot.scatter(beta, scatter1)
pyplot.scatter(beta, scatter2)
pyplot.legend(['C=5,V=1', 'C=5,V=3.5'])
pyplot.xlabel('Selection Intensity')
pyplot.ylabel('Final Vaccination Level')
'''
pyplot.show()
