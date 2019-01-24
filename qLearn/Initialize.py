from core import MultiOps as op
from core.Qubit import Qubit as q
from qLearn.Session import Session


class Initialize(Session):

    def __init__(self, num_vars, limit_spin=False):
        super(Initialize, self).__init__(limit_spin)
        self.system = [q() for i in range(num_vars)]

    def equalize(self):
        for i in self.system:
            i.H()

    def entangle(self, i1, i2):
        self.entangled_pairs[self._entangle_count] = (i1, i2)
        self._entangle_count += 1
        return op.CNOT(self.system[i1], self.system[i2])

    def state_flips(self, *args):
        for i in args:
            self.system[i].X()

    def state_name(self, *args):
        if type(args[0]) == list:
            args = args[0]
        if len(args) != len(self.system):
            raise ValueError("Must pass 1:1 state names to initialized states")

        args = list(args)
        self.system_name = {args[i]: self.system[i] for i in range(len(args))}
        [self.system[i].set_name(name) for i, name in enumerate(args)]



