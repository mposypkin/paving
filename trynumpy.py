import numpy as np

def F(x):
    return np.array([np.inner(x,x), x[2] - 1])

def hess(x):
    return np.array([[2 * x[0], 2 * x[1], 2 * x[2]], [0, 0, 1]])

def penrose(a):
    at = np.transpose(a)
    c = a @ at
    cinv = np.linalg.inv(c)
    r = at @ cinv
    return r

def solve(x):
    while True:
        a = 1
        h = hess(x)
        p = penrose(h)
        print(h @ p)
        z = p @ F(x)
        print("------------")
        print(z)
        print(np.inner(z, z))
        con = input("continue (n/y)?")
        if con == "n":
            break
        else:
            x = x - a * z

# a = np.array([[0.5, 0.7, 0.9],[1, 2, 3]])
# a = np.array([1, 1, 2])
# b = np.transpose(a)
# c = a @ b
# print(a)
# print(b)
# print(c)
# a = hess(np.array([1,1,0]))
# print(penrose(a))

solve(np.array([0.5,0.5,0.9]))