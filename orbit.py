from eps import Eps
import math

eps = Eps("orbit", 500)
eps.add("%f %f translate" % (250, 250))

# algorithm steps from https://ntrs.nasa.gov/citations/19680004301

iterations = 10000
timescale = 1
tolerance = 1e-5

# gauss's constant
k = 0.8346268416740731

# intial conditions: q, e, T which are the periapsis distance, eccentricity, and time to periapsis
# units: km, ??, days
# numbers all from wolfram alpha
planets = {
    "mercury": (4.6001272e7, 0.20563069, 87.97),
    "venus": (1.07476e8, 0.00677323, 224.7008),
    "earth": (1.47098074e8, 0.01671022, 365.25636),
    "mars": (2.06644545e8, 0.09341233, 686.97959),
    "jupiter": (7.407426e8, 0.04839266, 4332.8201),
    "saturn": (1.349467e9, 0.0541506, 10755.699),
    "uranus": (2.73555503e9, 0.04716771, 30687.153),
    "neptune": (4.4596315e9, 0.00858587, 60190.03),
}


# meant to be an infinite series, but i can't really do that
def z(i, B):
    return planet[1] * B ** i * sum(((-B ** 2 * (1 - planet[1])) ** n / math.factorial(2 * n + i)) for n in range(10))


def phi(B, r):
    return B + z(3, B) - r


def correction(B, r):
    return (-2 * phi(B, r)) / ((1 + z(2, B)) + math.sqrt((1 + z(2, B)) ** 2 - 2 * z(1, B) * phi(B, r)))


for i in range(iterations):
    for planet_str in planets:
        planet = planets[planet_str]
        r = (k * ((i * timescale) - planet[2])) / (planet[0] ** 1.5)
        A = math.sqrt((8 + (9 * r ** 2) * planet[1]) / planet[1])
        B0 = ((3 * r + A) / planet[1]) ** (1. / 3) + -(-(((3 * r) - A) / planet[1])) ** (1. / 3)
        B = B0
        if planet[1] == 1:
            # true anomaly
            v = 2 * math.atan(B0 / math.sqrt(2))
        else:
            while correction(B, r) > tolerance:
                B = B + correction(B0, r)
            print(B)
