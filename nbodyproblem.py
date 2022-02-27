import random
import numpy as np
from eps import Eps
from tqdm import tqdm


eps = Eps("nbodyproblem", 500)
eps.add("%f %f translate" % (250, 250))
eps.add("%f %f scale" % (5, 5))
eps.add("%f setlinewidth" % 0.01)

G = 9.8

# algorithm and start points from https://blbadger.github.io/3-body-problem.html

iterations = 200000
delta = 0.001

m1, m2, m3 = 10, 20, 30
p1_start, p2_start, p3_start = np.array(
    [10., 10., -11.]), np.array(
    [0., 0., 0.]), np.array(
    [10., 10., 12.])
v1_start, v2_start, v3_start = np.array(
    [-3., 0., 0.]), np.array(
    [0., 0., 0.]), np.array(
    [3., 0., 0.])


def accelerations(p1, p2, p3, m1, m2, m3):
    planet_1_dv = -9.8 * m2 * (p1 - p2) / (
            np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2) ** 3) - \
                  9.8 * m3 * (p1 - p3) / (
                          np.sqrt((p1[0] - p3[0]) ** 2 + (p1[1] - p3[1]) ** 2 + (p1[2] - p3[2]) ** 2) ** 3)

    planet_2_dv = -9.8 * m3 * (p2 - p3) / (
            np.sqrt((p2[0] - p3[0]) ** 2 + (p2[1] - p3[1]) ** 2 + (p2[2] - p3[2]) ** 2) ** 3) - \
                  9.8 * m1 * (p2 - p1) / (
                          np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2 + (p2[2] - p1[2]) ** 2) ** 3)

    planet_3_dv = -9.8 * m1 * (p3 - p1) / (
            np.sqrt((p3[0] - p1[0]) ** 2 + (p3[1] - p1[1]) ** 2 + (p3[2] - p1[2]) ** 2) ** 3) - \
                  9.8 * m2 * (p3 - p2) / (
                          np.sqrt((p3[0] - p2[0]) ** 2 + (p3[1] - p2[1]) ** 2 + (p3[2] - p2[2]) ** 2) ** 3)

    return planet_1_dv, planet_2_dv, planet_3_dv


p1, p2, p3 = [[[0., 0., 0.] for _ in range(iterations)] for _ in range(3)]
v1, v2, v3 = [[[0., 0., 0.] for _ in range(iterations)] for _ in range(3)]

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

    eps.add("%f %f moveto" % (p1[i][0], p1[i][1]))
    eps.add("%f %f lineto" % (p1[i + 1][0], p1[i + 1][1]))
    eps.add("%f %f %f setrgbcolor" % (1, 0, 0))
    eps.add("stroke")

    eps.add("%f %f moveto" % (p2[i][0], p2[i][1]))
    eps.add("%f %f lineto" % (p2[i + 1][0], p2[i + 1][1]))
    eps.add("%f %f %f setrgbcolor" % (0, 1, 0))
    eps.add("stroke")

    eps.add("%f %f moveto" % (p3[i][0], p3[i][1]))
    eps.add("%f %f lineto" % (p3[i + 1][0], p3[i + 1][1]))
    eps.add("%f %f %f setrgbcolor" % (0, 0, 1))
    eps.add("stroke")

eps.add("closepath")
eps.add("showpage")
eps.add("%EOF")
eps.write()
