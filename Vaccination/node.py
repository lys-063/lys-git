class Node:
    def __init__(self, index, type):
        '''shorthand of notation
            vaccinated 1
            unvaccinated but healthy 2
            unvaccinated and infected 3'''
        self.index = index
        self.type = type
        self.link = []
