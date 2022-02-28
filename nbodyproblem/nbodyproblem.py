import random
import numpy as np
from eps import Eps
from tqdm import tqdm  # progress bar
import os

# algorithm adapted from https://blbadger.github.io/3-body-problem.html
# changed to be 2d

iterations = 200000
delta = 0.0005
G = 9.8

# masses
m1, m2, m3 = 10, 20, 30

# start positions
p1_start, p2_start, p3_start = np.array(
    [10., 10.]), np.array(
    [0., 0.]), np.array(
    [10., -10.])

# start velocities
v1_start, v2_start, v3_start = np.array(
    [0., 0.]), np.array(
    [0., 0.]), np.array(
    [0., 0.])


# calculates derivatives (accelerations) of the 3 bodies
def accelerations(p1, p2, p3, m1, m2, m3):
    planet_1_dv = -G * m2 * (p1 - p2) / (
            np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 2) - \
                  G * m3 * (p1 - p3) / (
                          np.sqrt((p1[0] - p3[0]) ** 2 + (p1[1] - p3[1]) ** 2) ** 2)

    planet_2_dv = -G * m3 * (p2 - p3) / (
            np.sqrt((p2[0] - p3[0]) ** 2 + (p2[1] - p3[1]) ** 2) ** 2) - \
                  G * m1 * (p2 - p1) / (
                          np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 2)

    planet_3_dv = -G * m1 * (p3 - p1) / (
            np.sqrt((p3[0] - p1[0]) ** 2 + (p3[1] - p1[1]) ** 2) ** 2) - \
                  G * m2 * (p3 - p2) / (
                          np.sqrt((p3[0] - p2[0]) ** 2 + (p3[1] - p2[1]) ** 2) ** 2)

    return planet_1_dv, planet_2_dv, planet_3_dv


# create arrays for the positions and velocities
p1, p2, p3 = [[[0., 0.] for _ in range(iterations)] for _ in range(3)]
v1, v2, v3 = [[[0., 0.] for _ in range(iterations)] for _ in range(3)]

# set initial values
p1[0], p2[0], p3[0] = p1_start, p2_start, p3_start
v1[0], v2[0], v3[0] = v1_start, v2_start, v3_start

for i in tqdm(range(iterations - 1)):
    dv1, dv2, dv3 = accelerations(p1[i], p2[i], p3[i], m1, m2, m3)

    v1[i + 1] = v1[i] + dv1 * delta
    v2[i + 1] = v2[i] + dv2 * delta
    v3[i + 1] = v3[i] + dv3 * delta

    p1[i + 1] = p1[i] + v1[i] * delta
    p2[i + 1] = p2[i] + v2[i] * delta
    p3[i + 1] = p3[i] + v3[i] * delta

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
            if all(p1[k]) and all(p1[k + 1]):
                eps.add("%f %f moveto" % (p1[k][0], p1[k][1]))
                eps.add("%f %f lineto" % (p1[k + 1][0], p1[k + 1][1]))
                eps.add("%f %f %f setrgbcolor" % (1, 0, 0))
                eps.add("stroke")

            if all(p2[k]) and all(p2[k + 1]):
                eps.add("%f %f moveto" % (p2[k][0], p2[k][1]))
                eps.add("%f %f lineto" % (p2[k + 1][0], p2[k + 1][1]))
                eps.add("%f %f %f setrgbcolor" % (0, 1, 0))
                eps.add("stroke")

            if all(p3[k]) and all(p3[k + 1]):
                eps.add("%f %f moveto" % (p3[k][0], p3[k][1]))
                eps.add("%f %f lineto" % (p3[k + 1][0], p3[k + 1][1]))
                eps.add("%f %f %f setrgbcolor" % (0, 0, 1))
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
os.system("ffmpeg -f image2 -framerate 15 -i frame%03d.png -y output.gif")
os.system("del *.png")
