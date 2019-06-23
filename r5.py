import numpy as np
import interval as ival

l = 8.
L = 6.
d = 6.

def F(x):
    return np.array([l * np.cos(x[0]) + L * np.cos(x[2]) - x[4],
                     l * np.cos(x[1]) + L * np.cos(x[3]) - x[4] + d,
                     l * np.sin(x[0]) + L * np.sin(x[2]) - x[5],
                     l * np.sin(x[1]) + L * np.sin(x[3]) - x[5]])

def hess(x):
    return np.array([[-l * np.sin(x[0]), 0, -L * np.sin(x[2]), 0, -1, 0],
                     [0, -l * np.sin(x[1]), 0, -L * np.sin(x[3]), -1, 0],
                     [l * np.cos(x[0]), 0, L * np.cos(x[2]), 0, 0, -1],
                     [0, l * np.cos(x[1]), 0, L * np.cos(x[3]), 0, -1]])

def hessr(x):
    return np.array([[-l * np.sin(x[0]), 0, -L * np.sin(x[2]), 0],
                     [0, -l * np.sin(x[1]), 0, -L * np.sin(x[3])],
                     [l * np.cos(x[0]), 0, L * np.cos(x[2]), 0],
                     [0, l * np.cos(x[1]), 0, L * np.cos(x[3])]])


def mkconst(val):
    return ival.Interval([val, val])

def IF(x):
    return np.array([mkconst(l) * ival.cos(x[0]) + mkconst(L) * ival.cos(x[2]) - x[4],
                     mkconst(l) * ival.cos(x[1]) + mkconst(L) * ival.cos(x[3]) - x[4] + mkconst(d),
                     mkconst(l) * ival.sin(x[0]) + mkconst(L) * ival.sin(x[2]) - x[5],
                     mkconst(l) * ival.sin(x[1]) + mkconst(L) * ival.sin(x[3]) - x[5]])
