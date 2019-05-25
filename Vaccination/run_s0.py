from network import Network
from random import random


def independent_run(index, generation, omega, N, deg, vaccination_level, k11, k22, k33, k12, k13, k23, beta, vcost,
                    icost, r0):
    print('RUN---' + str(index) + '---START')
    net = Network(N, deg, vaccination_level, k11, k22, k33, k12, k13, k23, beta, vcost, icost, r0)
    vlevel = [0] * (net.N + 1)
    for i in range(generation):
        if random() < omega:
            net.restrategy()
            net.epidemic()
            vlevel[net.vaccination_level] = vlevel[net.vaccination_level] + 1
            if net.vaccination_level == 0 or net.vaccination_level == net.N:
                break
        else:
            net.relink()
    print('RUN---' + str(index) + '---END' + '\t' + str(net.vaccination_level))

    mode = []
    m = max(vlevel)
    for j in range(net.N + 1):
        if vlevel[j] == m:
            mode.append(j)

    if len(mode) > 1:
        print("EXCEPTION: exist more than one mode")
        print(mode)

    average_mode = 0
    for x in mode:
        average_mode = average_mode + x
    average_mode = average_mode / len(mode)

    return average_mode
