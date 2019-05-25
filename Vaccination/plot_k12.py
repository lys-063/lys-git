import matplotlib.pyplot as pyplot
from math import tanh

pyplot.figure()
font = {'family': 'Times New Roman',
        'weight': 'normal',
        'size': 15,
        }
# 1
k11 = 0.5
k22 = 0.5
k33 = 0.5
k23 = 0.5
k12 = [0.3, 0.32, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
k13 = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
r0 = 3
beta = 10
vcost = 1
icost = 5
x = []
line1 = []
for i in range(1, 100):
    x.append(i / 100)
for k in range(1, 100):
    k = k / 100
    line1.append(
        (1 - 1 / r0 * (1 + (k13[0] / k) * (tanh(0.5 * beta * vcost) / tanh(0.5 * beta * (icost - vcost))))) * 100)

scatter1 = [18.32, 18.9, 21.0, 25.36, 29.02, 31.52, 33.71, 35.15, 37.7, 38.37, 39.72, 41.56, 42.18, 43.02, 43.97]

pyplot.subplot(3, 1, 1)
p1 = pyplot.plot(x, line1)
pyplot.scatter(k12, scatter1)
pyplot.legend(['$r_0=3$'])
pyplot.text(0.37,49,'(a)')
pyplot.xlim([0.2,1])
pyplot.ylim([0,60])

# 2
k11 = 0.5
k22 = 0.5
k33 = 0.5
k23 = 0.5
k12 = [0.3, 0.32, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
k13 = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
r0 = 4
beta = 10
vcost = 1
icost = 5
x = []
line2 = []
for i in range(1, 100):
    x.append(i / 100)
for k in range(1, 100):
    k = k / 100
    line2.append(
        (1 - 1 / r0 * (1 + (k13[0] / k) * (tanh(0.5 * beta * vcost) / tanh(0.5 * beta * (icost - vcost))))) * 100)

scatter2 = [40.88, 42.08, 43.76, 46.3, 47.94, 49.76, 50.88, 52.36, 53.42, 54.07, 54.7, 55.56, 56.54, 57.9, 58.38]

pyplot.subplot(3, 1, 2)
p2 = pyplot.plot(x, line2)
pyplot.scatter(k12, scatter2)
pyplot.legend(['$r_0=4$'])
pyplot.text(0.37,62,'(b)')
pyplot.ylabel('Final Vaccination Level',font)
pyplot.xlim([0.2,1])
pyplot.ylim([0,80])

# 3
k11 = 0.5
k22 = 0.5
k33 = 0.5
k23 = 0.5
k12 = [0.3, 0.32, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
k13 = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
r0 = 5
beta = 10
vcost = 1
icost = 5
x = []
line3 = []
for i in range(1, 100):
    x.append(i / 100)
for k in range(1, 100):
    k = k / 100
    line3.append(
        (1 - 1 / r0 * (1 + (k13[0] / k) * (tanh(0.5 * beta * vcost) / tanh(0.5 * beta * (icost - vcost))))) * 100)

scatter3 = [52.42, 52.73, 54.96, 56.5, 58.44, 60.04, 61.43, 62.14, 62.64, 63.7, 64.46, 64.99, 65.48, 66.0, 66.2]

pyplot.subplot(3, 1, 3)
p3 = pyplot.plot(x, line3)
pyplot.scatter(k12, scatter3)
pyplot.legend(['$r_0=5$'])
pyplot.text(0.37,69,'(c)')
pyplot.xlabel('$k_{VH}$',font)
pyplot.xlim([0.2,1])
pyplot.ylim([20,80])
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
for i in range(1,100):
    x.append(i / 100)
for k in range(1,100):
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
