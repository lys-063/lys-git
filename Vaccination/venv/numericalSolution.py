
    R0 = 3;
    k = 0.8 / 0.45;
    C = 5;
    V = 1;
    beta=[]
    for xbeta in range(100):
        #xbeta=0:0.1:10
        beta.append((xbeta + 1) / 10)
    equilibrium = []
    for xbeta in beta:
        equilibrium.append((1 - 1 / R0 * (1 + k * tanh(0.5 * xbeta * V) / tanh(0.5 * xbeta * (C - V)))) * 100)

    R0 = 3;
    beta = 10;
    C = 5;
    V = 1;
    kRatio = []
    for xkRatio in range(200):
        #xkRatio=0:0.01:2
        kRatio.append((xkRatio + 1) / 100)
    equilibrium = []
    for xkRatio in kRatio:
        equilibrium.append((1 - 1 / R0 * (1 + xkRatio * tanh(0.5 * beta * V) / tanh(0.5 * beta * (C - V)))) * 100)
