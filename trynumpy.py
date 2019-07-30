import numpy as np

# def F(x):
#     return np.array([np.inner(x,x), x[2] - 1])
#
# def hess(x):
#     return np.array([[2 * x[0], 2 * x[1], 2 * x[2]], [0, 0, 1]])

l = 8
L = 6
d = 6
tol = 1e-6

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
        fv = F(x)
        z = p @ fv
        print("fv = ", fv)
        fvnorm = np.inner(fv, fv)
        print("fvnorm = ", fvnorm)
        print("------------")
        print(z)
        print(np.inner(z, z))
        con = input("continue (n/y)?")
        if con == "n":
            break
        else:
            x -= a * z
            # x = x - a * z

# a = np.array([[0.5, 0.7, 0.9],[1, 2, 3]])
# a = np.array([1, 1, 2])
# b = np.transpose(a)
# c = a @ b
# print(a)
# print(b)
# print(c)
# a = hess(np.array([1,1,0]))
# print(penrose(a))

# solve(np.array([0.5,0.5,0.9]))
# xv = np.array([0.5,0.5,0.9,0.9, 0.9,0.9])
# solve(xv)
#
# print("x = ", xv)
# print("F(x) = ", F(xv))

s1 = "aaa"
s2 = s1
print(s1, s2)
s1.swapcase()
print(s1, s2)


