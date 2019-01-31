import numpy as np
import math
import operator
from core.Qubit import Qubit
import time


def tensor_product_simple(q1, q2):
    try:
        return np.asarray([i*j for i in q1.superposition() for j in q2.superposition()])
    except AttributeError:
        raise(ValueError("Argument types for q1, q2 must be 'core.Qubit'"))


def tensor_product(*args):

    if type(args[0]) == list:
        args = args[0]
    args = list(args)

    def __product(x1, x2):
        return np.asarray([i*j for i in x1 for j in x2])

    t_product = np.zeros(shape=[int(math.pow(2, len(args))), 1])
    try:
        entangled = system_elements_entangled(args)
        if entangled[1] > 0:
            systems = [CNOT(entangled[0][n*2], entangled[0][n*2+1]) for n in range(int(entangled[1]))]
            for p in range(len(systems)):
                t_product[:int(math.pow(4, p+1))] = __product(t_product[:int(math.pow(4, p))], systems[p]) \
                    if p > 0 else systems[0]
            args = entangled[0]
            num = int(entangled[1] * 2)
        else:
            t_product[:4] = __product(args[0].superposition(), args[1].superposition())
            num = 2

        if len(args) > 2:
            for k in range(num, len(args)):
                t_product[:int(math.pow(2, k+1))] = __product(t_product[:int(math.pow(2, k))], args[k].superposition())
        return t_product
    except AttributeError:
        raise(ValueError("Argument types must be 'core.Qubit' or List('core.Qubit')"))


def CNOT(q1, q2):
    gate = np.asarray([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 0, 1],
                       [0, 0, 1, 0]])
    q_system = tensor_product_simple(q1, q2)

    q1.entangle(q2, 1)
    q2.entangle(q1, 2)

    return np.matmul(gate, q_system)


def are_entangled(q1, q2):
    return q1.is_entangled() == id(q2)


def system_elements_entangled(*args):
    if type(args[0]) == list:
        args = args[0]
    args = list(args)
    e = []
    try:
        for i in args:
            for j in args:
                if are_entangled(i, j):
                    e.append(i if i.entangled_position < j.entangled_position else j)
                    e.append(i if i.entangled_position > j.entangled_position else j)
                    args.pop(args.index(i))
                    args.pop(args.index(j))
        num_entangled = len(e)/2
        e.extend(args)
        return e, num_entangled
    except AttributeError:
        raise(ValueError("Argument types must be 'core.Qubit' or List('core.Qubit')"))


def controlled_measure(q1, *args):
    if type(args[0]) == list:
        args = args[0]
    args = list(args)
    try:
        q1.measure()
        for q in args:
            if are_entangled(q1, q) and (np.argmax(CNOT(q1, q)) > 1):
                q.X()
                q.entangled_with = 0
                q1.entangled_with = 0
                break
        return q1.measure()
    except AttributeError:
        raise(ValueError("Argument types must be 'core.Qubit' or List('core.Qubit')"))


def enumerate_names(*args):
    if type(args[0]) == list:
        args = args[0]
    args = list(args)
    product = []
    args = system_elements_entangled(args)[0]
    nums = [format(i, "0{}b".format(len(args))) for i in range(int(math.pow(2, len(args))))]
    for i, num in enumerate(nums):
        product.append([''.join([args[k].name for k in range(len(num)) if num[k] == "1"])])
    return product


def binary_tensor(*args):
    if type(args[0]) == list:
        args = args[0]
    args = list(args)
    enum = [format(i, "0{}b".format(len(args))) for i in range(int(math.pow(2, len(args))))]
    prod = np.zeros(shape=[int(math.pow(2,len(args))), 1])
    for i, b in enumerate(enum):
        prod[i] = np.prod([args[k].superposition()[int(bb)] for k, bb in enumerate(b)])
    return prod


def vector_tensor(*args):
    if type(args[0]) == list:
        args = args[0]
    args = list(args)
    identity = np.repeat([np.identity(2)], int(math.pow(2, len(args))), axis=0)

    def single_prod(l1, l2):
        s = identity[:len(l1)]
        delta = np.reshape(list(map(operator.mul, s, l1)), newshape=[int(len(l1))*2, 2])
        return np.matmul(delta, l2)
    prod = np.zeros(shape=[int(math.pow(2, len(args))), 1])
    for q in range(0, len(args)):
        prod[:int(math.pow(2, q+1))] = single_prod(prod[:int(math.pow(2, q))], args[q].superposition()) \
            if q > 0 else args[q].superposition()
    return prod


'''
Q1 = Qubit()
Q1.H()
Q1.Ry(.22)

#Q1.Ry(.22)
#print(q1.superposition())
Q2 = Qubit()
Q2.H()
Q2.Ry(-.3)
print(vector_tensor(Q1, Q2))
print(tensor_product(Q1, Q2))

Q3 = Qubit()
Q3.H()
print(Q1.superposition())
print(Q2.superposition())
print(vector_tensor(Q1, Q2))

print(binary_tensor(Q1, Q2))

print(tensor_product(Q1, Q2))

#Q2.X()

Q3 = Qubit()
Q4 = Qubit()
Q4.H()
Q5 = Qubit()
Q4.X()
#print(tensor_product_simple(q2, q3))
CNOT(Q3, Q4)
CNOT(Q1, Q2)
print(tensor_product(Q1, Q3, Q4, Q2, Q5))
#print(controlled_measure(Q1, [Q1, Q2, Q3, Q4]))
#print(Q2.measure())
print(tensor_product([Q4, Q2]))

x = []
for i in range(25):
    q = Qubit()
    if i%2 == 0:
        q.X()
    q.H()
    x.append(q)
print("Load complete")
start = time.time()
print(vector_tensor(x))
print(time.time() - start)
'''








