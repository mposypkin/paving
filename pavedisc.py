import interval as ival
import plotbot as pb

OUT = 0
IN = 1
INDET = 2



def f(x):
    return x[0] ** 2 + x[1] ** 2 + x[2] ** 2 - 1

def fi(x):
    return x[0] ** 2 + x[1] ** 2 + x[2] ** 2 - ival.Interval([1, 1])

def g(x, a):
    return x[2] - a * f(x)

def gi(x, a):
    return x[2] - ival.Interval([a,a]) * fi(x)

def dg(x, a):
    return 1. - 2. * a * x[2]

def dgi(x, a):
    return ival.Interval([1.,1.]) - ival.Interval([2., 2.]) * ival.Interval([a,a]) * x[2]

def getCenter(par):
    return list(map(lambda y: 0.5 * (y[0] + y[1]), par))


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
    c = ival.Interval(par[2]).mid()
    ac = 1./(2. * c)
    ic = [ival.Interval(par[0]), ival.Interval(par[1]), ival.Interval([c, c])]
    igc = gi(ic, ac)
    ibox = [ival.Interval(par[0]), ival.Interval(par[1]), ival.Interval(par[2])]
    idg = dgi(ival.Interval(ibox), ac)
    xmc = ival.Interval([par[2][0] - c, par[2][1] - c])
    ix = igc + idg * xmc
    ix2 = ival.Interval(par[2])
    # print("ix = ", ix, "ix2 = ", ix2)
    if ix.isIn(ix2):
        rv = IN
    elif ix.isNoIntersec(ix2):
        rv = OUT
    else:
        ix.intersec(ival.Interval([0, 100]))
        par[2] = ix.x
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

    cb = reduceBox([[par[0][0],par[0][1]], [par[1][0], par[1][1]], [par[2][0],par[2][1]]])
    # return cb
    if not cb == INDET:
        return cb
    else:
        if snew < delta:
            # print(par, snew)
            return reduceBox(par)
            # return cb
        else:
            m = 0.5 * (par[2][0] + par[2][1]);
            vl = evalBox([par[0], par[1], [par[2][0], m]])
            if vl == IN:
                return IN
            else:
                vr = evalBox([par[0], par[1], [m, par[2][1]]])
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
# print(reduceBox(box))
# print(evalBox(box))
# exit(0)

inbox = []
outbox = []
indetbox = []
n = 100
h = 2. / n
A = -1
B = -1
for i in range(0,n):
    for j in range(0,n):
        bx = [[A + h * i, A + h * (i + 1)], [B + h * j, B + h * (j + 1)], [0.0, 1]]
        cb = evalBox(bx)
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




