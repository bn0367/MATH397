import random
import numpy as np
from eps import Eps
from tqdm import tqdm  # progress bar
import os

# algorithm adapted from https://blbadger.github.io/3-body-problem.html
# changed to be 2d, extended to be n-bodies

iterations = 1000000
delta = 0.0001
G = 9.8

colors = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0), (1.0, 0.0, 1.0), (1.0, 0.9, 0.0)]

masses = [
    10,
    20,
    30,
    40,
    20
]

position_starts = [
    np.array([10., 10.]),
    np.array([0., 0.]),
    np.array([10., -10.]),
    np.array([-10., 10.]),
    np.array([-10., -10.]),
]

velocity_starts = [
    np.array([0., 0.]),
    np.array([0., 0.]),
    np.array([0., 0.]),
    np.array([0., 0.]),
    np.array([0., 0.])
]


# calculates derivatives (accelerations) of the 3 bodies
def accelerations(p, m):
    acc = []
    for i in range(len(p)):
        dv = sum(-G * m[x] * (p[i] - p[x])
                 / (np.sqrt((p[i][0] - p[x][0]) ** 2 + (p[i][1] - p[x][1]) ** 2) ** 2) for x in range(len(p)) if x != i)
        acc.append(dv)
    return acc


# create arrays for the positions and velocities
positions = [[np.array([0., 0.]) for _ in range(iterations)] for _ in range(len(masses))]
velocities = [[np.array([0., 0.]) for _ in range(iterations)] for _ in range(len(masses))]

# set initial values
for i in range(len(masses)):
    positions[i][0] = position_starts[i]
    velocities[i][0] = velocity_starts[i]

for i in tqdm(range(iterations - 1)):
    dvs = accelerations([x[i] for x in positions], masses)

    for m in range(len(masses)):
        velocities[m][i + 1] = velocities[m][i] + dvs[m] * delta

    for m in range(len(masses)):
        positions[m][i + 1] = positions[m][i] + velocities[m][i] * delta

    if (i - 500) % 1000 == 0 and i > 0:
        eps = Eps("nbodyproblem%d" % ((i - 500) / 1000), 500)
        eps.add("%f setlinewidth" % 0.05)
        # black background
        eps.add("0.0 0.0 0.0 setrgbcolor")
        eps.add("newpath 0 0 moveto 0 500 lineto 500 500 lineto 500 0 lineto closepath fill")

        # fix scaling to make the paths visible
        eps.add("%f %f translate" % (250, 250))
        eps.add("%f %f scale" % (5, 5))

        # use old points to make frame transition smoother
        for k in range(i - 500, i + 499):
            for j in range(len(masses)):
                if all(positions[j][k]) and all(positions[j][k + 1]):
                    eps.add("%f %f moveto" % (positions[j][k][0], positions[j][k][1]))
                    eps.add("%f %f lineto" % (positions[j][k + 1][0], positions[j][k + 1][1]))
                    eps.add("{} {} {} setrgbcolor".format(*colors[j]))
                    eps.add("stroke")

        eps.add("closepath")
        eps.add("showpage")
        eps.add("%EOF")
        eps.write()

        # .eps to png
        os.system(
            "gswin64c -g500x500 -q -dNOPAUSE -dBATCH -sDEVICE=png256 -sOutputFile=frame%03d.png nbodyproblem%d.eps" % (
                ((i - 500) / 1000), ((i - 500) / 1000)))
        os.system("del nbodyproblem%d.eps" % ((i - 500) / 1000))

# frames to gif
os.system("ffmpeg -f image2 -framerate 15 -i frame%03d.png -y output-5-bodies.gif")
os.system("del *.png")
