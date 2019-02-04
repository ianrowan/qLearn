from qLearn.Initialize import Initialize
from core.MultiOps import tensor_product, controlled_measure, enumerate_names
import math
import numpy as np


class Session(object):

    def __init__(self, limit_spin=False):
        self.system = []
        self.system_name = {}
        self.entangled_pairs = {}
        self._entangle_count = 0
        self.limit_spin = limit_spin

    def custom_states(self, rotate_angle, *args):
        """
        Applies custom rotation to list of indexed Qubits
        :param rotate_angle: Angle for Ry Op
        :param args: List of indexes
        :return:
        """
        for i in args:
            self.system[i].Ry(rotate_angle)
            if self.limit_spin:
                self.__check_spin_limit(i)

    def __single_var_liklihood(self, x):
        """
        Arbitrary Liklihood function for single varible data
        :param x: datapoint
        :return:
        """
        return 1 / math.exp(1 - x)

    def __switched_liklihood(self, x, c):
        """
        Arbitrary two way liklihood fucntion for single variable data
        :param x: datapoint
        :param c: boolean
        :return:
        """
        return self.__single_var_liklihood(x) - 1 + c

    def __check_spin_limit(self, q):
        """
        Checks if superposition of q is over Spin Limit
        Measures is so
        :param q: Qubit Type Object
        :return:
        """
        beta = 1 - self.system[q].superposition()[1]
        if beta <= 0 or beta >= 1:
            self.system[q].measure()

    def adjust_state_liklihood(self, num, x, c=None):
        """
        Adjusts the liklihood of a Qubit State based on data
        :param num: index of state
        :param x: datapoint
        :param c: boolean(optional)
        :return:
        """
        rotate = self.__single_var_liklihood(x) if not c else self.__switched_liklihood(x, c)
        self.custom_states(rotate, num)

    def measure_single(self, num, name=None):
        """
        Measures a single state in the system
        :param num: index of state
        :param name: name of state
        :return: state of Qubit[num, name]
        """
        if name:
            return controlled_measure(self.system_name[name], self.system)
        return controlled_measure(self.system[num], self.system)

    def system_state(self, include_names=False):
        """
        Visualization of the full system state
        :param include_names: enumerate names
        :return: [2^n x 1] system state vector
        """
        if not include_names:
            return tensor_product(self.system)

        return tensor_product(self.system), enumerate_names(self.system)

    def measure_system(self, include_names=False):
        """
        Measures all elements of the system
        :param include_names: enumerate names
        :return: [2^n x 1] system state vector
        """
        for q in self.system:
            controlled_measure(q, self.system)
        if not include_names:
            return tensor_product(self.system)
        return tensor_product(self.system), enumerate_names(self.system)

    def single_state_value(self, *args):
        """
        Finds the custom state probability of passed inidices
        :param args: indexes of Qubits in desired state
        :return: Single probability of the desired state
        """
        if type(args[0]) == list:
            args = args[0]
        args = list(args)
        key = np.zeros([len(self.system)])
        for i in args:
            key[i] += 1
        return tensor_product(self.system)[int("".join(key), 2)]
