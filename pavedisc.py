import interval as ival
import plotbot as pb

OUT = 0
IN = 1
INDET = 2


def intervalize(par):
    return [ival.Interval(e) for e in par]

# Disc
# def f(x):
#     return x[0] ** 2 + x[1] ** 2 + x[2] ** 2 - 1
#
# def df(x):
#     return 2 * x[2]
#
# bigBox = [[-2, 2], [-2, 2], [0,1]]


# Ring
# def f(x):
#     return x[0] ** 2 + x[1] ** 2 - x[2] ** 2 - 1
#
# def df(x):
#     return -2 * x[2]
#
# bigBox = [[-2, 2], [-2, 2], [0,10]]


# Butterfly
def f(x):
    return x[0] ** 2 - x[1] ** 2 + x[2] ** 2 - 1

def df(x):
    return 2 * x[2]

bigBox = [[-2, 2], [-2, 2], [0,10]]




def g(x, a):
    return x[2] - a * f(x)

def dg(x, a):
    return 1. - a * df(x)


# def checkBoxNT(par):
#     c = ival.Interval(par[2]).mid()
#     boxc = [ival.Interval(par[0]), ival.Interval(par[1]), ival.Interval([c,c])]
#     intf = fi(boxc)
#     intdfr = ival.Interval([1./(2. * par[2][1]), 1./(2. * par[2][0])])
#     ix = ival.Interval([c,c]) - intf * intdfr
#     ix2 = ival.Interval(par[2])
#     print("ix = ", ix, "ix2 = ", ix2)
#     if ix.isIn(ix2):
#         rv = IN
#     elif ix.isNoIntersec(ix2):
#         rv = OUT
#     else:
#         # ix2.intersec(ix)
#         # par[2] = ix2.x
#         ix.intersec(ival.Interval([0.01,10]))
#         par[2] = ix.x
#         rv = INDET
#     return rv

def getCentralFormBounds(par, c, ac):
    ic = [par[0], par[1], c]
    igc = g(ic, ac)
    idg = dg(par, ac)
    ix = igc + idg * (par[2] - c)
    return ix

def getKRBounds(par):
    c = df(par).mid()
    ac = 1. / c if c != 0 else 0.1
    ix = getCentralFormBounds(par, par[2].mid(), ac)
    return ix

def getKRSBounds(par):
    c = df(par).mid()
    ac = 0.6 / c if c != 0 else 0.1
    # ac = 1/(2. * c) if c != 0 else 0.1
    idg = dg(par, ac)
    if idg[1] <= 0:
        cl = par[2][1]
        cu = par[2][0]
    elif idg[0] >= 0:
        cl = par[2][0]
        cu = par[2][1]
    else:
        cl = (idg[1] * par[2][0] - idg[0] * par[2][1]) / (idg[1] - idg[0])
        cu = (idg[1] * par[2][1] - idg[0] * par[2][0]) / (idg[1] - idg[0])
    ixl = getCentralFormBounds(par, cl, ac)
    ixu = getCentralFormBounds(par, cu, ac)
    ixl.intersec(ixu)
    return ixl



def checkBoxKR(par):
    # ix = getKRBounds(par)
    ix = getKRSBounds(par)
    if ix.isIn(par[2]):
        rv = IN
    elif ix.isNoIntersec(par[2]):
        rv = OUT
    else:
        par[2] = ix
        rv = INDET
    return rv



# def checkBox(par):
#     rv = checkBoxKR(par)
#     if rv == INDET:
#         return checkBoxNT(par)
#     else:
#         return rv
#
# def checkBox(par):
#     return checkBoxNT(par)

def checkBox(par):
    return checkBoxKR(par)

def boxSize(par, coords):
    w = 0
    for i in coords:
        l = par[i][1] - par[i][0]
        if l > w:
            w = l
    return w


def reduceBox(par):
    delta = 1e-8
    sold = boxSize(par, [2])
    i = 0
    while(True):
        cb = checkBox(par)
        if not cb == INDET:
            return cb
        else:
            snew = boxSize(par, [2])
            # print("snew = ", snew)
            if snew > maxBoxSize:
                return cb
            i = i + 1
            # print(i)
            if abs(sold - snew) < delta:
                return cb
            else:
                sold = snew
                par[2].scale(1.1)

def bndFixPointTest(par):
    # return False
    c = df(par).mid()
    a = 1 / c if c != 0 else 0.1
    i1 = g([par[0], par[1], ival.Interval([par[2][0], par[2][0]])], a)
    if i1.isIn(par[2]):
        i2 = g([par[0], par[1], ival.Interval([par[2][1], par[2][1]])], a)
        if i2.isIn(par[2]):
            return True
    return False

def evalBox(par):
    delta = 1e-1
    if bndFixPointTest(par):
        return IN
    snew = boxSize(par, [2])
    cb = reduceBox(par.copy())
    if not cb == INDET:
        return cb
    else:
        if snew < delta:
            return reduceBox(par)
        else:
            m = par[2].mid()
            vl = evalBox([par[0], par[1], ival.Interval([par[2][0], m])])
            if vl == IN:
                return IN
            else:
                vr = evalBox([par[0], par[1], ival.Interval([m, par[2][1]])])
                if vr == IN:
                    return IN
                elif vr == OUT:
                    if vl == OUT:
                        return OUT
                    else:
                        return INDET
                else:
                    return INDET

maxBoxSize = 16

# box = [[-0.8, -0.6], [0.8, 1], [0, 1]]
# box = [[-0.8, -0.6], [-1, -0.8], [0, 1]]
box = [[-0.7999999999999998, -0.5999999999999999], [-1, -0.7999999999999998], [0, 10]]
# box = [[0.0, 0.5], [0.0, 0.5], [0.6422613636363637, 1.1]]
# box = [[0.8, 0.9], [0.0, 0.1], [0.4,0.6]]
# box = [[-0.5, 0.0], [-0.5, 0.0], [0.6422613636363637, 1.1]]
# print(reduceBox(intervalize(box)))
print("eval: ", evalBox(intervalize(box)))
# print(checkBox(intervalize(box)))
# exit(0)

inbox = []
outbox = []
indetbox = []
n = 10
h = [(I[1] - I[0]) / n for I in bigBox]

for i in range(0,n):
    for j in range(0,n):
        bx = [[bigBox[0][0] + h[0] * i, bigBox[0][0] + h[0] * (i + 1)], [bigBox[1][0] + h[1] * j, bigBox[1][0] + h[1] * (j + 1)], bigBox[2]]
        cb = evalBox(intervalize(bx))
        if cb == IN:
            inbox.append(bx)
        elif cb == OUT:
            outbox.append(bx)
        else:
            indetbox.append(bx)


# print(inbox)
pb.plot(inbox, 'green', False)
pb.plot(outbox, 'grey', False)
pb.plot(indetbox, 'yellow', True)

print(h)
print(-2. + 0.2 * 6)


