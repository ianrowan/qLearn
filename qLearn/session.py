from qLearn.Initialize import Initialize
from core.MultiOps import tensor_product, controlled_measure
import math


def single_var_liklihood(x):
    return 1/math.exp(1-x)


def switched_liklihood(x, c):
    return single_var_liklihood(x) - 1 + c


def adjust_state_liklihood(session, num, x, c=None):
    rotate = single_var_liklihood(x) if not c else switched_liklihood(x,c)
    print(rotate)
    session.custom_states(rotate, num)


def measure_single(session, num, name=None):
    if name:
        return controlled_measure(session.system_name[name], session.system)
    return controlled_measure(session.system[num], session.system)


def system_state(session):
    return tensor_product(session.system)


def measure_system(session):
    for q in session.system:
        controlled_measure(q, session.system)
    return tensor_product(session.system)

