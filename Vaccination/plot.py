import matplotlib.pyplot as pyplot
from math import tanh


def plot(xaxis, yaxis, xlabel, ylabel, path, name):
    pyplot.figure()
    pyplot.plot(xaxis, yaxis)
    pyplot.xlabel(xlabel)
    pyplot.ylabel(ylabel)
    # pyplot.xlim(left=0, right=10)
    # pyplot.ylim(bottom=0, top=100)
    pyplot.savefig(path + name + '.png')
    pyplot.savefig(path + name + '.eps')
    pyplot.show()


