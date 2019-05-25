from network import Network
from random import random

window = 1000


def independent_run(index, generation, omega, N, deg, vaccination_level, k11, k22, k33, k12, k13, k23, beta, vcost,
                    icost, r0):
    print('RUN---' + str(index) + '---START')
    net = Network(N, deg, vaccination_level, k11, k22, k33, k12, k13, k23, beta, vcost, icost, r0)
    vlevel = []
    for i in range(generation):
        if random() < omega:
            net.restrategy()
            net.epidemic()
            if (i < generation - window) and (net.vaccination_level == 0 or net.vaccination_level == net.N):
                vlevel = [net.vaccination_level] * window
                break
        else:
            net.relink()
        if (i >= generation - window):
            vlevel.append(net.vaccination_level)
        else:
            pass
    print('RUN---' + str(index) + '---END' + '\t' + str(net.vaccination_level))

    v = 0
    if len(vlevel) != window:
        print('ERROR')
    else:
        for x in vlevel:
            v = v + x
    v = v / window

    return v
