import interval as ival
import plotbot as pb

OUT = 0
IN = 1
INDET = 2


def intervalize(par):
    return [ival.Interval(e) for e in par]

def f(x):
    return x[0] ** 2 + x[1] ** 2 + x[2] ** 2 - 1


def g(x, a):
    return x[2] - a * f(x)

def dg(x, a):
    return 1. - 2. * a * x[2]


def inflate(x):
    m = 0.5 * (x[0] + x[1])
    w = x[1] - x[0]
    x[0] = m - 0.51 * w
    x[1] = m + 0.51 * w


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


def checkBoxKR(par):
    c = par[2].mid()
    ac = 1./(2. * c)
    ic = [par[0], par[1], c]
    igc = g(ic, ac)
    idg = dg(par, ac)
    ix = igc + idg * (par[2] - c)
    ix2 = par[2]
    # print("ix = ", ix, "ix2 = ", ix2)
    if ix.isIn(ix2):
        rv = IN
    elif ix.isNoIntersec(ix2):
        rv = OUT
    else:
        ix.intersec(ival.Interval([0, 100]))
        par[2] = ix
        inflate(par[2])
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
        if  l > w:
            w = l
    return w


def reduceBox(par):
    delta = 1e-8
    snew = 10
    sold = boxSize(par, [2])
    i = 0
    # print("Reduce entry")
    while(True):
        cb = checkBox(par)
        if not cb == INDET:
            return cb
        else:
            snew = boxSize(par, [2])
            i = i + 1
            if abs(sold - snew) < delta:
                return cb
            else:
                sold = snew


def evalBox(par):
    delta = 1e-1
    snew = boxSize(par, [2])
    print("snew = ", snew)
    # cb = checkBox(par)

    cb = reduceBox(par.copy())
    # return cb
    if not cb == INDET:
        return cb
    else:
        if snew < delta:
            # print(par, snew)
            return reduceBox(par)
            # return cb
        else:
            m = par[2].mid();
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

# def reduceBox(par):
#     delta = 1e-3
#     snew = 0
#     sold = boxSize(par, [2])
#     while(True):
#         print(par, sold)
#         cb = checkBox(par)
#         if cb != INDET:
#             return cb
#         else:
#             snew = boxSize(par, [2])
#             if sold - snew < delta:
#                 return cb
#             else:
#                 sold = snew

# box = [[0.1, 0.3], [0.1, 0.3], [0.01, 1]]
# box = [[0.0, 0.5], [0.0, 0.5], [0.6422613636363637, 1.1]]
box = [[0.8, 0.9], [0.0, 0.1], [0.4,0.6]]
# box = [[-0.5, 0.0], [-0.5, 0.0], [0.6422613636363637, 1.1]]
# print(reduceBox(intervalize(box)))
# print(evalBox(intervalize(box)))
# print(checkBox(intervalize(box)))
# exit(0)

inbox = []
outbox = []
indetbox = []
n = 10
h = 2. / n
A = -1
B = -1
for i in range(0,n):
    for j in range(0,n):
        bx = [[A + h * i, A + h * (i + 1)], [B + h * j, B + h * (j + 1)], [0.0, 1]]
        cb = evalBox(intervalize(bx))
        # print(cb)
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




