import numpy as np


class Qubit:

    def __init__(self):
        self.position = np.asarray([[1.0],
                                    [0.0]])

    def measure(self):

        for i in self.position:
            i[0] = int(i[0] == max(self.position))

        return self.position

    def superposition(self):
        return self.position

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



CNOT = np.asarray([[1,0,0,0], [0,1,0,0], [0,0,0,1], [0,0,1,0]])

q1 = Qubit()
q1.H()
q1.Ry(1.0)
q1 = q1.superposition()
q2 = Qubit().superposition()

tensor = [j[0]*i[0] for j in q1 for i in q2]
entangle = np.matmul(CNOT, np.asarray(tensor).transpose())
print(tensor)
print(entangle)