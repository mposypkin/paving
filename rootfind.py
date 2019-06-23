import numpy as np
from r5 import *


l = 8
L = 6
d = 6
tol = 1e-6





def penrose(a):
    at = np.transpose(a)
    c = a @ at
    cinv = np.linalg.inv(c)
    r = at @ cinv
    return r

def solve(x, f, df, tol, maxit):
    i = 0
    rv = True
    while True:
        h = df(x)
        p = penrose(h)
        # p = np.linalg.inv(h)
        fv = f(x)
        z = p @ fv
        fvnorm = np.inner(fv, fv)
        a = min(1, 1/fvnorm)
        a = 1
        if fvnorm <= tol:
            break
        else:
            x -= a * z
        i += 1
        if i > maxit:
            rv = False
            break
    return rv
            # x = x - a * z

if (__name__ == '__main__'):
    xv = np.array([0.5,0.5,0.9,0.9,3.9,2.4])
    xnv = xv[0:4]
    Fn = lambda y : F(np.concatenate((y, np.array([xv[4], xv[5]]))))
    solve(xnv, Fn, hessr, 1e-4, 1000)
    print("x = ", xnv)
    print("F(x) = ", Fn(xnv))

    # solve(xv, F, hess, 1e-4, 1000)
    # print("x = ", xv)
