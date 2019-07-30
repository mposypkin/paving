import matplotlib.pyplot as plt
import sys
# import re

def plot(parr, color = 'red', show = True):
    plt.axes()
    for p in parr:
        # a1 = p[4][0]
        # b1 = p[4][1]
        # a2 = p[5][0]
        # b2 = p[5][1]
        a1 = p[0][0]
        b1 = p[0][1]
        a2 = p[1][0]
        b2 = p[1][1]
        # rectangle = plt.Rectangle((a1, a2), b1 - a1, b2 - a2, fc=color, fill = True, color='black')
        rectangle = plt.Rectangle((a1, a2), b1 - a1, b2 - a2, fc=color, fill = True)
        plt.gca().add_patch(rectangle)
    plt.axis('scaled')
    if show:
        plt.show()

#circle = plt.Circle((0, 0), radius=3, fc='y', fill = False)
#plt.gca().add_patch(circle)
# circle = plt.Circle((-3, 0), radius=3, fc='y', fill = False)
# plt.gca().add_patch(circle)
# circle = plt.Circle((-3, 0), radius=7, fc='y', fill = False)
# plt.gca().add_patch(circle)

