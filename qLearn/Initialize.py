from core import MultiOps as op
from core.Qubit import Qubit as q


class Initialize:

    def __init__(self, num_vars):
        self.system = [q() for i in range(num_vars)]
        self.system_name = {}
        self.entangled_pairs = {}
        self._entangle_count = 0

    def equalize(self):
        for i in self.system:
            i.H()

    def entangle(self, i1, i2):
        self.entangled_pairs[self._entangle_count] = (i1, i2)
        self._entangle_count += 1
        return op.CNOT(self.system[i1], self.system[i2])

    def system_state(self):
        return op.tensor_product(self.system)

    def state_flips(self, *args):
        for i in args:
            self.system[i].X()

    def custom_states(self, rotate_angle, *args):
        for i in args:
            self.system[i].Ry(rotate_angle)

    def state_name(self, *args):
        if len(args) != len(self.system):
            raise ValueError("Must pass 1:1 state names to initialized states")
        elif type(args[0]) == list:
            args = args[0]

        args = list(args)
        self.system_name = {args[i]: self.system[i] for i in range(len(args))}

