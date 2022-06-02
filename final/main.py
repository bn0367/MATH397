"""
Code from:
P. Mora, G. Morra, D. A. Yuen, 2019, A concise Python implementation of the Lattice Boltzmann Method on HPC for
    geo-fluid flow Geophysical Journal International, Volume 220, Issue 1, Pages 682–702
    https://doi.org/10.1093/gji/ggz423
"""

import numpy as np
import tqdm
from PIL import Image

im = Image.open("monster.jpg")
im = im.convert('L').resize((int(im.size[0] / 7), int(im.size[1] / 7)))

na = 9
c = np.array([[0, 0], [1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]])  # Right to left
ai = np.array([0, 2, 1, 4, 3, 6, 5, 8, 7])
D = 2

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

nt = 100  # Number of time steps
nx = 201  # X-axis size
nz = 201  # Z-axis size

# new indexes for the vectorized streaming calculations
indexes = np.zeros((na, nx * nz), dtype=int)
xInds, zInds = [], []
if stream_opt == 1:
    for a in range(na):
        xArr = (np.arange(nx) - c[a][0] + nx) % nx
        zArr = (np.arange(nz) - c[a][1] + nz) % nz
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
rho_0 = 1.0  # Density
rho *= rho_0
rho2 = np.zeros((nz, nx))
np.random.seed(0)
rho = np.random.rand(nz, nx)

# Initialize the density, velocity and solid boolean
# f[0:na] = 1
u2 = np.einsum('ijk,ijk->jk', u, u)
for a in np.arange(na):
    f[a] = rho * w[a]
    cu = np.einsum('i,ijk->jk', c[a], u)
    for d in np.arange(D):
        f[a] += w[a] * (c2 * c[a][d] * u[d] + c3 * cu ** 2 + c4 * u2)

frames[0] = rho


def tick(t):
    global f, f_stream, f_eq, Delta_f, solid, rho, u, Pi, cu, u2
    # periodic BC for f
    f[0:na, 0:nz, 0] = f[0:na, 0:nz, -2]
    f[0:na, 0:nz, -1] = f[0:na, 0:nz, 1]

    #   Streaming step with bounce back boundary conditions from solid surfaces
    if stream_opt == 0:
        for a in range(na):
            for x in range(1, nx - 1):
                x_xa = (x - c[a][0] + nx) % nx
                for z in range(nz):
                    z_za = (z - c[a][1] + nz) % nz
                    if solid[z_za][x_xa]:
                        f_stream[a][z][x] = f[ai[a]][z][x]  # Bounce-back BC
                    else:
                        f_stream[a][z][x] = f[a][z_za][x_xa]  # Streaming step

    # correct but without BC (not anymore!)
    elif stream_opt == 1:
        for a in np.arange(na):
            f_new = f[a].reshape(nx * nz)[indexes[a]]
            f_new[solid[zInds[a], xInds[a]]] = f[ai[a]][zInds[a], xInds[a]][solid[zInds[a], xInds[a]]]
            f_stream[a] = f_new.reshape(nz, nx)

    f = f_stream.copy()

    #   Macroscopic properties
    rho = np.sum(f, axis=0)
    Pi = np.einsum('azx,ad->dzx', f, c)
    u[0:D] = Pi[0:D] / rho

    #   Equilibrium distribution
    u2 = u[0] * u[0] + u[1] * u[1]
    for a in np.arange(na):
        cu = c[a][0] * u[0] + c[a][1] * u[1]
        f_eq[a] = rho * w[a] * (c1 + c2 * cu + c3 * cu ** 2 + c4 * u2)

    #   Collision term
    Delta_f = (f_eq - f) / tau_f
    f += Delta_f

    frames[t + 1] = u2.copy()


for i in tqdm.tqdm(range(nt)):
    tick(i)


# from https://stackoverflow.com/a/50784012/7809935

def color_fader(col1, col2, mix=0.):  # fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    return (1 - mix) * col1 + mix * col2


blue = np.array((0.17, 0.65, 0.89))
white = np.array((1, 1, 1))

for i in tqdm.tqdm(range(nt)):
    frame = frames[i]
    fixed = np.array(frame, dtype=np.float32)
    fixed[fixed < 0] = 0
    fixed[fixed > 1] = 1
    try:
        fixed = np.abs(np.log(fixed)) * 10
        fixed = np.array(fixed, dtype=np.uint8)
    except Warning:
        print("frame:", i)
    image = Image.fromarray(fixed, 'L')
    image.save('frames/frame_%03d.png' % i)
