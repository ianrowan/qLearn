import numpy as np
import math
from core.Qubit import Qubit

def tensor_product_simple(q1, q2):
    try:
        return np.asarray([i*j for i in q1.superposition() for j in q2.superposition()])
    except:
        Exception("must pass type Qubit")

def tensor_product(*args):

    if type(args[0]) == list:
        args = args[0]

    def __product(x1, x2):
        return np.asarray([i*j for i in x1 for j in x2])

    t_product = np.zeros(shape=[int(math.pow(2,len(args))), 1])
    t_product[:4] = __product(args[0].superposition(), args[1].superposition())
    if len(args) > 2:
        for k in range(2, len(args)):
            t_product[:int(math.pow(2, k+1))] = __product(t_product[:int(math.pow(2, k))], args[k].superposition())
    return t_product

def CNOT(q1, q2):
    gate = np.asarray([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 0, 1],
                       [0, 0, 1, 0]])
    q_system = tensor_product_simple(q1, q2)
    #Todo: log/track entangelment
    q1.entangled_with = id(q2)
    q2.entangled_With = id(q1)

    return np.matmul(gate, q_system)

def are_entangled(q1, q2):
    return q1.is_entangled() == id(q2)

def system_elements_entangled(*args):
    if type(args[0]) == list:
        args = args[0]
    e = []
    for i in args:
        for j in args:
            if are_entangled(i, j):
                e.append(i)
                e.append(j)
                del i, j
    num_entangled = len(e)/2
    e.append(args)
    return e, num_entangled


q1 = Qubit()
q1.H()
print(q1.superposition())
q2 = Qubit()
q2.H()
q3 = Qubit()
print(q3.is_entangled())
print(CNOT(q2, q3))
print(are_entangled(q1, q3))

print(system_elements_entangled(q1, q2, q3))
#print(tensor_product(q1, q2, q3))
x = []
for i in range(25):
    q = Qubit()
    if i%2 == 0:
        q.X()
    q.H()
    x.append(q)
#print(tensor_product(x))



