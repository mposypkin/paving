import interval as ival
import plotbot as pb

OUT = 0
IN = 1
INDET = 2



def f(x):
    return x[0] * x[0] + x[1] * x[1] + x[2] * x[2] - 1

def fi(x):
    return x[0] * x[0] + x[1] * x[1] + x[2] * x[2] - ival.Interval([1, 1])

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


def checkBox(par):
    c = ival.Interval(par[2]).mid()
    ac = 1./(2. * c)
    ic = [ival.Interval(par[0]), ival.Interval(par[1]), ival.Interval([c, c])]
    igc = gi(ic, ac)
    ibox = [ival.Interval(par[0]), ival.Interval(par[1]), ival.Interval(par[2])]
    idg = dgi(ival.Interval(ibox), ac)
    xmc = ival.Interval([par[2][0] - c, par[2][1] - c])
    ix = igc + idg * xmc
    ix2 = ival.Interval(par[2])
    if ix.isIn(ix2):
        rv = IN
    elif ix.isNoIntersec(ix2):
        rv = OUT
    else:
        ix2.intersec(ix)
        par[2] = ix2.x
        rv = INDET
    return rv

def boxSize(par, coords):
    w = 0
    for i in coords:
        l = par[i][1] - par[i][0]
        if  l > w:
            w = l
    return w



def evalBox(par):
    delta = 1e-3
    snew = 0
    sold = boxSize(par, [2])
    while(True):
        cb = checkBox(par)
        if cb != INDET:
            return cb
        else:
            snew = boxSize(par, [2])
            if sold - snew < delta:
                return cb
            else:
                sold = snew

box = [[0.1, 0.3], [0.1, 0.3], [0, 1]]
print(evalBox(box))

inbox = []
outbox = []
indetbox = []
n = 100
h = 2. / n
for i in range(0,n):
    for j in range(1,n):
        bx = [[-1 + h * i, -1 + h * (i + 1)], [-1 + h * j, -1 + h * (j + 1)], [0, 1.1]]
        cb = evalBox(bx)
        print(cb)
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




