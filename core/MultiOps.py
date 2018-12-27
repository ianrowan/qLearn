import numpy as np
import math
from Qubit import Qubit

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


q1 = Qubit()
q1.H()
print(q1.superposition())
q2 = Qubit()
q2.H()
q3 = Qubit()
q3.H()

print(tensor_product(q1, q2, q3))
x = []
for i in range(25):
    q = Qubit()
    if i%2 == 0:
        q.X()
    q.H()
    x.append(q)
print(tensor_product(x))



