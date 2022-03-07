import math
from tqdm import trange  # progress bar
import subprocess  # cmd calls
from subprocess import DEVNULL  # suppress ffmpeg
import sys  # arguments
import csv  # read input file

# algorithm adapted from https://blbadger.github.io/3-body-problem.html
# changed to be 2d, extended to be n-bodies

if len(sys.argv) != 6:
    print("Usage: nbodyproblem   <iterations> <timestep> <trail_length> <input_file> <output_file>")
    exit(1)

# (r, g, b), mass, [x, y], [vx, vy]
bodies = []

with open(sys.argv[4], 'r') as csvfile:
    reader = csv.reader(csvfile)
    data = list(reader)
    for i in range(1, len(data)):
        bodies.append([(float(data[i][0]), float(data[i][1]), float(data[i][2])), float(data[i][3]),
                       [float(data[i][4]), float(data[i][5])], [float(data[i][6]), float(data[i][7])]])

iterations = int(sys.argv[1])
delta = float(sys.argv[2])
G = 9.8
trail_length = int(sys.argv[3])
size = 1000


# calculates accelerations of the bodies
def accelerations(p, m):
    acc = []
    for i in range(len(p)):
        dv = [0., 0.]
        for j in range(len(p)):
            if i != j:
                top = [(p[i][0] - p[j][0]) * -G * m[j] * m[i], (p[i][1] - p[j][1]) * -G * m[j] * m[i]]
                bottom = math.sqrt(((p[i][0] - p[j][0]) ** 2) + ((p[i][1] - p[j][1]) ** 2)) ** 2
                dv[0] += top[0] / bottom
                dv[1] += top[1] / bottom
        acc.append(dv)
    return acc


# create arrays for the positions and velocities
print("Initializing positions... ", end="")
positions = [[[0., 0.] for _ in range(iterations)] for _ in range(len(bodies))]
print("Done")
print("Initializing velocities... ", end="")
velocities = [[[0., 0.] for _ in range(iterations)] for _ in range(len(bodies))]
print("Done")
# set initial values
for i in range(len(bodies)):
    positions[i][0] = bodies[i][2]
    velocities[i][0] = bodies[i][2]

print("Rendering frames... ", end="")

for i in trange(iterations - 1):
    dvs = accelerations([x[i] for x in positions], [x[1] for x in bodies])

    for m in range(len(bodies)):
        velocities[m][i + 1][0] = velocities[m][i][0] + dvs[m][0] * delta
        velocities[m][i + 1][1] = velocities[m][i][1] + dvs[m][1] * delta

    for m in range(len(bodies)):
        positions[m][i + 1][0] = positions[m][i][0] + velocities[m][i][0] * delta
        positions[m][i + 1][1] = positions[m][i][1] + velocities[m][i][1] * delta

    if (i - 500) % 1000 == 0 and i > 0:
        lines = [
            "%%!PS-Adobe-3.0 EPSF-3.0\n%%BoundingBox: 0 0 %d %d\n%d setlinejoin %d setlinewidth %d setlinecap 0.0 "
            "0.0 0.0 setrgbcolor newpath 0 0 moveto 0 %d lineto %d %d lineto %d 0 lineto closepath fill %d %d "
            "translate %d %d scale " % (
                size, size, 1, 1, 1, size, size, size, size, -positions[0][i][0] + size // 2,
                -positions[0][i][1] + size // 2, 1, 1)]

        # use old points to make frame transition smoother
        start = i - trail_length if i > trail_length else 1
        for j in range(len(bodies)):
            lines.append("%.1f %.1f %.1f setrgbcolor %.3f %.3f moveto\n" % (
                bodies[j][0][0], bodies[j][0][1], bodies[j][0][2], positions[j][start][0], positions[j][start][1]))
            for k in range(start + 1, i + 499, 25):
                width = ((k - start) / ((i + 499) - (start - 1))) * (bodies[j][1] / 30)
                if width > 1 and positions[j][k][0] != 0 and positions[j][k][1] != 0 and \
                        positions[j][k + 1][0] != 0 and positions[j][k + 1][1] != 0:
                    lines.append("newpath %.3f setlinewidth %.3f %.3f moveto %.3f %.3f lineto stroke " % (
                        width, positions[j][k][0], positions[j][k][1], positions[j][k + 1][0], positions[j][k + 1][1]))
            lines.append(
                " \n%.3f %.3f %.3f 0 360 arc fill " % (
                    positions[j][i][0], positions[j][i][1], bodies[j][1] / 30))

        lines.append("showpage\n%EOF")
        with open("frames/nbodyproblem%d.eps" % ((i - 500) / 1000), "w") as f:
            f.writelines(lines)

        # .eps to png
        subprocess.Popen(["gswin64c", "-g%dx%d" % (size, size), "-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=png16m",
                          "-sOutputFile=frame%03d.png" % ((i - 500) / 1000),
                          "nbodyproblem%d.eps" % ((i - 500) / 1000)], cwd="frames/")

# frames to gif
print("Rendering gif... ", end="")
subprocess.Popen(
    ["ffmpeg", "-f", "image2", "-framerate", "15", "-i", "frame%03d.png", "-y", "../%s" % sys.argv[5]], cwd="frames/",
    stdout=DEVNULL, stderr=DEVNULL).wait()
print("Done")

# cleanup
print("Cleaning up... ", end="")
subprocess.Popen("del *.eps", shell=True, cwd="frames/").wait()
subprocess.Popen("del *.png", shell=True, cwd="frames/").wait()
print("Done")
