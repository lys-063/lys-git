import matplotlib.pyplot as pyplot
from math import tanh

font = {'family': 'Times New Roman',
        'weight': 'normal',
        'size': 15,
        }
k11 = 0.5
k22 = 0.5
k33 = 0.5
k23 = 0.5
k12 = 0.8
k13 = 0.8
r0 = 3
beta = 10
vcost = 1
icost = 5
x = []
line = []
for i in range(1000):
    x.append(i / 1000)
for i in range(1000):
    line.append(
        (1 - 1 / r0 * (1 + (k13 / k12) * (tanh(0.5 * beta * vcost) / tanh(0.5 * beta * (icost - vcost))))) * 100)
omega = [0.001, 0.003, 0.005, 0.007, 0.009, 0.01, 0.03, 0.05, 0.07, 0.09, 0.1, 0.3, 0.5, 0.7, 0.9]
omega_reverse = []
for o in omega:
    omega_reverse.append(1 - o)
f = [30.8469, 33.35533333333333, 31.720633333333335, 30.520300000000006, 30.135666666666676, 31.472033333333336,
     28.102666666666664, 32.23296666666666, 31.62883333333333, 30.996766666666666, 28.965866666666674,
     30.43416666666667, 22.12363333333333, 25.693566666666666, 24.126633333333338]
f_reverse = [24.126633333333338, 25.693566666666666, 22.12363333333333, 30.43416666666667, 28.965866666666674,
             30.996766666666666, 31.62883333333333, 32.23296666666666, 28.102666666666664, 31.472033333333336,
             30.135666666666676, 30.520300000000006, 31.720633333333335, 33.35533333333333, 30.8469]
pyplot.figure()
pyplot.semilogx(x, line, 'r')
pyplot.scatter(omega, f)
pyplot.xlabel('$1-\omega$', font)
pyplot.ylabel('Final Vaccination Level', font)
pyplot.ylim([20, 40])
pyplot.show()
print()
