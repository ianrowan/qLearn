from core import MultiOps as op
from core.Qubit import Qubit as q
from qLearn.Session import Session


class Initialize(Session):

    def __init__(self, num_vars, limit_spin=False):
        """
        Creates session for Quantum Learning
        :param num_vars: number of Qubits to init
        :param limit_spin: boolean; limit spin of states to range [0,1]
        """
        super(Initialize, self).__init__(limit_spin)
        self.system = [q() for i in range(num_vars)]

    def equalize(self):
        """
        Apply H gate to all system Qubits
        Allows for equal initial probability
        :return:
        """
        for i in self.system:
            i.H()

    def entangle(self, i1, i2):
        """
        Entangles two Qubits in the session
        :param i1: index of Qubit
        :param i2: index of Qubit
        :return: new state of entangled pair
        """
        self.entangled_pairs[self._entangle_count] = (i1, i2)
        self._entangle_count += 1
        return op.CNOT(self.system[i1], self.system[i2])

    def state_flips(self, *args):
        """
        Flips the superposition or state of any Qubit.
        :param args: list of indexes to flip
        :return:
        """
        for i in args:
            self.system[i].X()

    def state_name(self, *args):
        """
        Applies a list of str like names to system Qubits
        :param args: List of strings of equal length of system
        :return:
        """
        if type(args[0]) == list:
            args = args[0]
        if len(args) != len(self.system):
            raise ValueError("Must pass 1:1 state names to initialized states")

        args = list(args)
        self.system_name = {args[i]: self.system[i] for i in range(len(args))}
        [self.system[i].set_name(name) for i, name in enumerate(args)]



