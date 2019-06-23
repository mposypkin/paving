import numpy as np
import interval as ival
import plotbot as pb
import rootfind as rf
import time
from r5 import *

discarded = 0
covered = 0
delta = 2
minsize = 0.1
maxrfit = 100
tol = 1e-4

paving = []
ipar = [[0, 2 * np.pi - 0.01], [0, 2 * np.pi - 0.02], [0, 2 * np.pi - 0.03], [0, 2 * np.pi - 0.04], [-14, 14], [-14, 14]]
P = [ipar]




def size(par):
    m = 0
    i = 0
    # r = range(0, len(par))
    r = range(4, len(par))
    for j in r:
        lm = par[j][1] - par[j][0]
        if m < lm:
            m = lm
            i = j
    return (m, i)

def split(par, i):
    p1 = []
    p2 = []
    j = 0
    for I in par:
        if j == i:
            m = 0.5 * (I[0] + I[1])
            p1.append([I[0], m])
            p2.append([m, I[1]])
        else:
            p1.append(I)
            p2.append(I)
        j += 1
    return [p1, p2]


def ifAlreadyCovered(par):
    rv = False
    for p in paving:
        if (p[4][0] <= par[4][0] and p[4][1] >= par[4][1]) and (p[5][0] <= par[5][0] and p[5][1] >= par[5][1]):
            rv = True
            break
    return rv


def check(par):
    rv = True
    makeint = lambda x: ival.Interval(x)
    ivec = list(map(makeint, par))
    # for i in range(0, len(ivec)):
    #     print(ivec[i])
    iv = IF(ivec)
    for I in iv:
        if I[0] > 0 or I[1] < 0:
            rv = False
            break
    return rv

def isIn(x, par):
    rv = True
    for i in range(0, len(x)):
        if x[i] < par[i][0] or x[i] > par[i][1]:
            rv = False
            break
    return rv

def getCenter(par):
    return list(map(lambda y: 0.5 * (y[0] + y[1]), par))

def containsRoot(par):
    # print(par)
    x = np.array(getCenter(par))
    xnv = x[0:4]
    Fn = lambda y : F(np.concatenate((y, np.array([x[4], x[5]]))))
    if not rf.solve(xnv, Fn, hessr, tol, maxrfit):
        # print("Fail to converge")
        return False
    # if not isIn(xnv, ipar):
    #     print("Out of box: ", xnv)
    #     return False
    else:
        print("Inside box of size ", size(par))
    return True

# def containsRoot(par):
#     x = np.array(getCenter(par))
#     if not rf.solve(x, F, hess, tol, maxrfit):
#         print("Fail to converge")
#         return False
#     if not isIn(x, par):
#         return False
#     else:
#         print("Inside box of size ", size(par))
#     return True

# def containsRoot(par):
#     x = np.array(getCenter(par))
#     if not rf.solve(x, F, hess, tol, maxrfit):
#         print("Fail to converge")
#         return False
#     if x[4] < par[4][0] or x[4] > par[4][1] or x[5] < par[5][0] or x[5] > par[5][1] :
#         return False
#     else:
#         print("Inside box of size ", size(par))
#     return True


print(size(ipar))

t = time.time()
while len(P) > 0:
    cpar = P.pop()
    if check(cpar) == False:
        discarded += 1
        continue
    if ifAlreadyCovered(cpar):
        covered += 1
        continue
    sz = size(cpar)
    if sz[0] <= minsize:
        continue

    if sz[0] <= delta and containsRoot(cpar):
            paving.append(cpar)
    else:
        P.extend(split(cpar, sz[1]))

t = time.time() - t
print("elapsed ", t, " sec")
print("paving consist of ", len(paving), " elements")
print("discarded = ", discarded)
print("covered = ", covered)
pb.plot(paving)