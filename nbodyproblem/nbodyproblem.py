import math
import numpy as np
from eps import Eps
from tqdm import trange  # progress bar
import subprocess  # cmd calls
import os  # for deleting files

# algorithm adapted from https://blbadger.github.io/3-body-problem.html
# changed to be 2d, extended to be n-bodies

iterations = 2000000
delta = 0.0001
G = 9.8
trail_length = 10000

# (r, g, b), mass, [x, y], [vx, vy]
bodies = [
    ((1.0, 0.0, 0.0), 22, np.array([10.0, 10.0]), np.array([0., 0.])),
    ((0.0, 1.0, 0.0), 21, np.array([0.00, 0.00]), np.array([0., 0.])),
    ((0.0, 0.0, 1.0), 20, np.array([10.0, -10.]), np.array([0., 0.])),
    ((1.0, 0.0, 1.0), 21, np.array([-10., 10.0]), np.array([0., 0.])),
    ((1.0, 1.0, 0.0), 22, np.array([-10., -10.]), np.array([0., 0.])),
]


# calculates derivatives (accelerations) of the bodies
def accelerations(p, m):
    acc = []
    for i in range(len(p)):
        dv = 0
        for j in range(len(p)):
            if i != j:
                dv += -G * m[j] * (p[i] - p[j]) / (math.sqrt((p[i][0] - p[j][0]) ** 2 + (p[i][1] - p[j][1]) ** 2) ** 2)
        acc.append(dv)
    return acc


# create arrays for the positions and velocities
positions = [[np.array([0., 0.]) for _ in range(iterations)] for _ in range(len(bodies))]
velocities = [[np.array([0., 0.]) for _ in range(iterations)] for _ in range(len(bodies))]

# set initial values
for i in range(len(bodies)):
    positions[i][0] = bodies[i][2]
    velocities[i][0] = bodies[i][2]

for i in trange(iterations - 1):
    dvs = accelerations([x[i] for x in positions], [x[1] for x in bodies])

    for m in range(len(bodies)):
        velocities[m][i + 1] = velocities[m][i] + dvs[m] * delta

    for m in range(len(bodies)):
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
        start = i - trail_length if i > trail_length else 1
        for j in range(len(bodies)):
            for k in range(start, i + 499):
                if all(positions[j][k]) and all(positions[j][k + 1]):
                    eps.add("%f %f moveto" % (positions[j][k][0], positions[j][k][1]))
                    eps.add("%f %f lineto" % (positions[j][k + 1][0], positions[j][k + 1][1]))
                    eps.add("{} {} {} setrgbcolor".format(*bodies[j][0]))
                    eps.add("stroke")
            eps.add("%f %f 0.25 0 360 arc fill" % (positions[j][i][0], positions[j][i][1]))

        eps.add("closepath")
        eps.add("showpage")
        eps.add("%EOF")
        eps.write()

        # .eps to png
        subprocess.Popen(["gswin64c", "-g500x500", "-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=png16m",
                          "-sOutputFile=frame%03d.png" % ((i - 500) / 1000),
                          "nbodyproblem%d.eps" % ((i - 500) / 1000)])

# frames to gif
subprocess.Popen(
    ["ffmpeg", "-f", "image2", "-framerate", "15", "-i", "frame%03d.png", "-y", "output-5-bodies.gif"]).wait()

# cleanup
os.system("del *.eps")
os.system("del *.png")
