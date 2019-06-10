import numpy as np

delta = 5e-1

def size(par):
    m = 0
    i = 0
    j = 0
    for I in par:
        lm = I[1] - I[0]
        if m < lm:
            m = lm
            i = j
        j += 1
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

pi = [[0,np.pi],[0,np.pi], [0,np.pi],[0,np.pi],[-8,14],[-8,14]]
P = [pi]

print(size(pi))

while len(P) > 0:
    cpar = P.pop()
    # print("P = ", P)
    sz = size(cpar)
    if sz[0] < delta:
        print(cpar)
    else:
        P.extend(split(cpar, sz[1]))


