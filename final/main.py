"""
Code from:
P. Mora, G. Morra, D. A. Yuen, 2019, A concise Python implementation of the Lattice Boltzmann Method on HPC for
    geo-fluid flow Geophysical Journal International, Volume 220, Issue 1, Pages 682–702
    https://doi.org/10.1093/gji/ggz423
"""
import math

import numpy as np
import tqdm
from PIL import Image, ImageSequence
import os

img = Image.open('square.gif')

is_animated = 'loop' in img.info

if is_animated:
    wall_frames = []
    for frame in ImageSequence.Iterator(img):
        wall_frames.append(np.array(frame))
else:
    walls = np.array(img)

na = 9
D = 2

e = np.array([[0, 0], [1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]])  # Right to left
ai = np.array([0, 2, 1, 4, 3, 6, 5, 8, 7])

c = 1
c_s = c / math.sqrt(3)

w0 = 4.0 / 9.0
w1 = 1.0 / 9.0
w2 = 1.0 / 36.0

w = np.array([w0, w1, w1, w1, w1, w2, w2, w2, w2])

dt = 1
dx = 1
S = dx / dt
c1 = 1.0
c2 = 3.0 / (S ** 2)
c3 = 9.0 / (2.0 * S ** 4)
c4 = -3.0 / (2.0 * S ** 2)

# Initialize the relaxation times
nu_f = 0.1  # Viscosity
tau_f = nu_f * 3. / (S * dt) + 0.5

stream_opt = 1  # vectorized
periodic_bc = False  # whether to use a periodic boundary condition

if not periodic_bc:
    if is_animated:
        for fr in range(0, len(wall_frames)):
            wall_frames[fr] = np.pad(wall_frames[fr], ((1, 1), (1, 1)), 'constant')
    else:
        walls = np.pad(walls, ((1, 1), (1, 1)), 'constant')

if is_animated:
    nt = len(wall_frames) * 10  # Number of time steps
else:
    nt = 1000
nx = img.width + (not periodic_bc) * 2  # X-axis size
nz = img.height + (not periodic_bc) * 2  # Z-axis size

# new indexes for the vectorized streaming calculations
indexes = np.zeros((na, nx * nz), dtype=int)
xInds, zInds = [], []
if stream_opt == 1:
    for a in range(na):
        xArr = (np.arange(nx) - e[a][0] + nx) % nx
        zArr = (np.arange(nz) - e[a][1] + nz) % nz
        xInd, zInd = np.meshgrid(xArr, zArr)
        xInds.append(xInd.flatten())
        zInds.append(zInd.flatten())
        indTotal = zInd * nx + xInd
        indexes[a] = indTotal.reshape(nx * nz)
# Initialize arrays

f = np.zeros((na, nz, nx))
f_stream = np.zeros((na, nz, nx))
f_eq = np.zeros((na, nz, nx))
Delta_f = np.zeros((na, nz, nx))
solid = np.zeros((nz, nx), dtype=bool)
rho = np.ones((nz, nx))
u = np.zeros((D, nz, nx))
Pi = np.zeros((D, nz, nx))
cu = np.zeros((nz, nx))

frames = np.zeros((nt + 1, nz, nx))

# Initialize the density and the number densities
rho_0 = 0.0  # Density
rho *= rho_0
np.random.seed(0)
rho = np.random.rand(nx, nz)

# Initialize the density, velocity and solid boolean
u2 = np.einsum('ijk,ijk->jk', u, u)
for a in np.arange(na):
    f[a] = rho * w[a]
    cu = np.einsum('i,ijk->jk', e[a], u)
    for d in np.arange(D):
        f[a] += w[a] * (c2 * e[a][d] * u[d] + c3 * cu ** 2 + c4 * u2)

frames[0] = rho
if is_animated:
    solid[wall_frames[0] == 0] = True
else:
    solid[walls == 0] = True

if not periodic_bc:
    solid[0, :] = True
    solid[-1, :] = True
    solid[:, 0] = True
    solid[:, -1] = True


def tick(t):
    global f, f_stream, f_eq, Delta_f, solid, rho, u, Pi, cu, u2, g, tau_g, g_eq

    if is_animated:
        solid[wall_frames[t % len(wall_frames) - 1] == 0] = False
        solid[wall_frames[t % len(wall_frames)] == 0] = True

    # streaming step
    for a in np.arange(na):
        f_new = f[a].reshape(nx * nz)[indexes[a]]
        f_new[solid[zInds[a], xInds[a]]] = f[ai[a]][zInds[a], xInds[a]][solid[zInds[a], xInds[a]]]
        f_stream[a] = f_new.reshape(nz, nx)

    f = f_stream.copy()

    #   Macroscopic properties
    rho = np.sum(f, axis=0)
    Pi = np.einsum('azx,ad->dzx', f, e)
    u[0:D] = Pi[0:D] / rho

    #   Equilibrium distribution
    u2 = u[0] * u[0] + u[1] * u[1]
    for a in np.arange(na):
        cu = e[a][0] * u[0] + e[a][1] * u[1]
        f_eq[a] = rho * w[a] * (c1 + c2 * cu + c3 * cu ** 2 + c4 * u2)

    #   Collision term
    Delta_f = (f_eq - f) / tau_f
    f += Delta_f

    frames[t + 1] = u2.copy()


for i in tqdm.tqdm(range(nt)):
    tick(i)

for i in tqdm.tqdm(range(nt)):
    frame = frames[i]
    fixed = np.array(frame, dtype=np.float32)
    if is_animated:
        fixed[wall_frames[i % len(wall_frames)] == 0] = 0
    if not periodic_bc:
        fixed = fixed[1:-1, 1:-1]
    fixed[fixed < 0] = 0
    fixed[fixed > 1] = 1

    try:
        fixed = np.abs(np.log(fixed)) * 10
        fixed = np.array(fixed, dtype=np.uint8)
    except Warning:
        print("frame:", i)
    image = Image.fromarray(fixed, 'L')
    image.save('frames/frame_%03d.png' % i)

os.system(".\\gif.bat %s" % input())
