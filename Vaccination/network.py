from node import Node
from edge import Edge
from random import random, choice, sample
from math import exp


class Network:
    '''shorthand of notation
        vaccinated 1
        unvaccinated but healthy 2
        unvaccinated and infected 3'''

    def __init__(self, N, deg, vaccination_level, k11, k22, k33, k12, k13, k23, beta, vcost, icost, r0):
        self.N = N
        self.deg = deg
        self.vaccination_level = vaccination_level
        self.k11 = k11
        self.k22 = k22
        self.k33 = k33
        self.k12 = k12
        self.k13 = k13
        self.k23 = k23
        self.k = [[self.k11, self.k12, self.k13],
                  [self.k12, self.k22, self.k23],
                  [self.k13, self.k23, self.k33]]
        self.beta = beta
        self.vcost = vcost
        self.icost = icost
        self.payoff_list = [-self.vcost, 0, -self.icost]
        self.r0 = r0

        self.node_list = []
        self.edge_list = []

        if (self.vaccination_level / self.N) < (1 - 1 / self.r0):
            self.infection_rate = 1 - 1 / (self.r0 * (1 - self.vaccination_level / self.N))
        else:
            self.infection_rate = 0
        self.vaccination_list = sample(range(self.N), self.vaccination_level)
        self.unvaccination_list = list(set(range(self.N)) - set(self.vaccination_list))
        infection_list = sample(self.unvaccination_list, int(self.infection_rate * (self.N - self.vaccination_level)))

        # create node
        for i in range(self.N):
            if i in self.vaccination_list:
                self.node_list.append(Node(index=i, type=1))
            elif i in infection_list:
                self.node_list.append(Node(index=i, type=3))
            else:
                self.node_list.append(Node(index=i, type=2))
        # build link
        cnt = 0
        for i in range(self.N):
            node1 = self.node_list[i]
            for j in range(int(self.deg / 2)):
                node2 = self.node_list[(i + j + 1) % self.N]
                self.edge_list.append(Edge(index=cnt, node1=node1, node2=node2))
                node1.link.append(node2)
                node2.link.append(node1)
                cnt = cnt + 1

    def relink(self):
        while True:
            edge = choice(self.edge_list)
            (node1, node2) = sample((edge.node1, edge.node2), 2)
            brk = self.k[node1.type - 1][node2.type - 1]
            if random() < brk:
                if len(node2.link) > 1:
                    link1 = node1.link
                    link2 = node2.link

                    link1.remove(node2)
                    link2.remove(node1)

                    set_of_choice = set(self.node_list) - set(link1) - {node1}
                    node3 = choice(list(set_of_choice))
                    link3 = node3.link

                    link1.append(node3)
                    link3.append(node1)

                    index = edge.index
                    self.edge_list[index] = Edge(index, node1, node3)
                    break
                else:
                    continue
            else:
                break

    def restrategy(self):
        self.edge_list = self.edge_list
        edge = choice(self.edge_list)
        (node1, node2) = sample((edge.node1, edge.node2), 2)

        payoff1 = self.payoff_list[node1.type - 1]
        payoff2 = self.payoff_list[node2.type - 1]

        imitation_rate = 1.0 / (1.0 + exp(self.beta * (payoff1 - payoff2)))

        if random() < imitation_rate:
            if (node1.type == 2 or node1.type == 3) and node2.type == 1:
                node1.type = node2.type
                self.vaccination_level = self.vaccination_level + 1
                self.vaccination_list.append(node1.index)
                self.unvaccination_list.remove(node1.index)
            elif node1.type == 1 and (node2.type == 2 or node2.type == 3):
                node1.type = node2.type
                self.vaccination_level = self.vaccination_level - 1
                self.unvaccination_list.append(node1.index)
                self.vaccination_list.remove(node1.index)
            else:
                node1.type = node2.type
        else:
            pass

    def epidemic(self):
        if (self.vaccination_level / self.N) < (1 - 1 / self.r0):
            self.infection_rate = 1 - 1 / (self.r0 * (1 - self.vaccination_level / self.N))
        else:
            self.infection_rate = 0

        infection_list = sample(self.unvaccination_list, int(self.infection_rate * (self.N - self.vaccination_level)))
        for i in self.unvaccination_list:
            node = self.node_list[i]
            if i in infection_list:
                node.type = 3
            else:
                node.type = 2
