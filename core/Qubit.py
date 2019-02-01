import numpy as np


class Qubit:

    def __init__(self):
        self.position = np.asarray([[1.0],
                                    [0.0]])
        self.name = ""
        self.entangled_with = 0
        self.entangled_position = 0

    def set_name(self, name):
        """
        Sets name of Qubit
        :param name: string type for name of Qubit
        :return:
        """
        self.name = name

    def measure(self):
        """
        Measures the current particle state of the Qubit
        sets position to determinant state
        :return: state
        """

        for i in self.position:
            i[0] = int(i[0] == max(self.position))

        return self.position

    def is_entangled(self):
        """
        returns reference of entangled Qubit
        :return: id of entangled qubit or ""
        """
        return self.entangled_with

    def superposition(self):
        """
        visualizes the current state of the Qubit
        :return: superposition vector
        """
        return self.position

    def entangle(self, q, pos):
        """
        Entangles Qubit Object with another Qubit Object q
        :param q: Qubit Type Object
        :param pos: 1 || 2 for first or second of the pair
        :return:
        """
        self.entangled_with = id(q)
        self.entangled_position = pos

    def X(self):
        """
        Quantum X Gate operation
        :return:
        """
        gate = np.asarray([[0, 1],
                           [1, 0]])
        self.position = np.matmul(gate, self.position)

    def H(self):
        """
        Quantum H Gate operation
        :return:
        """
        gate = 1 / np.sqrt(2) * np.asarray([[1, 1],
                                            [1, -1]])
        self.position = np.matmul(gate, self.position)

    def Z(self):
        """
        Quantum Z Gate operation
        :return:
        """
        gate = np.asarray([[1, 0],
                           [0, -1]])
        self.position = np.matmul(gate, self.position)

    def Ry(self, theta):
        """
        Ry type Quantum rotation gate
        :param theta: angle of rotation
        :return:
        """
        gate = np.asarray([[np.cos(theta/2), -np.sin(theta/2)],
                           [np.sin(theta/2), np.cos(theta/2)]])
        self.position = np.matmul(gate, self.position)
