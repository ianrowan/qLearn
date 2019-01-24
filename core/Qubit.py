import numpy as np


class Qubit:

    def __init__(self):
        self.position = np.asarray([[1.0],
                                    [0.0]])
        self.name = ""
        self.entangled_with = 0
        self.entangled_position = 0

    def set_name(self, name):
        self.name = name

    def measure(self):

        for i in self.position:
            i[0] = int(i[0] == max(self.position))

        return self.position

    def is_entangled(self):
        return self.entangled_with

    def superposition(self):
        return self.position

    def entangle(self, q, pos):
        self.entangled_with = id(q)
        self.entangled_position = pos

    def X(self):
        gate = np.asarray([[0, 1],
                           [1, 0]])
        self.position = np.matmul(gate, self.position)

    def H(self):
        gate = 1 / np.sqrt(2) * np.asarray([[1, 1],
                                            [1, -1]])
        self.position = np.matmul(gate, self.position)

    def Z(self):
        gate = np.asarray([[1, 0],
                           [0, -1]])
        self.position = np.matmul(gate, self.position)

    def Ry(self, theta):
        gate = np.asarray([[np.cos(theta/2), -np.sin(theta/2)],
                           [np.sin(theta/2), np.cos(theta/2)]])
        self.position = np.matmul(gate, self.position)
