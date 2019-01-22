from qLearn.Initialize import Initialize
from core.MultiOps import tensor_product, controlled_measure
import math


class Session:

    def __init__(self, limit_spin=False):
        self.system = []
        self.system_name = {}
        self.entangled_pairs = {}
        self._entangle_count = 0
        self.limit_spin = limit_spin

    def custom_states(self, rotate_angle, *args):
        for i in args:
            self.system[i].Ry(rotate_angle)
            if self.limit_spin:
                self.__check_spin_limit(i)

    def __single_var_liklihood(self, x):
        return 1 / math.exp(1 - x)

    def __switched_liklihood(self, x, c):
        return self.__single_var_liklihood(x) - 1 + c

    def __check_spin_limit(self, q):
        beta = 1 - self.system[q].superposition()[1]
        if beta <= 0 or beta >= 1:
            self.system[q].measure()

    def adjust_state_liklihood(self, num, x, c=None):
        rotate = self.__single_var_liklihood(x) if not c else self.__switched_liklihood(x, c)
        self.custom_states(rotate, num)

    def measure_single(self, num, name=None):
        if name:
            return controlled_measure(self.system_name[name], self.system)
        return controlled_measure(self.system[num], self.system)

    def system_state(self):
        return tensor_product(self.system)

    def measure_system(self):
        for q in self.system:
            controlled_measure(q, self.system)
        return tensor_product(self.system)


