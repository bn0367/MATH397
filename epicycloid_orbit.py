from eps import Eps
import math

eps = Eps("simple_orbit", 500)
eps.add("%f %f translate" % (250, 250))
eps.add("%f %f scale" % (1, 1))
eps.add("%f setlinewidth" % 1)
iterations = 2000
scale = 100
body_size = 1

# numbers from https://digitalcommons.kennesaw.edu/ojur/vol5/iss1/3
bodies = {
    "sun": (1210, 1, 50.4, 0, 0),
    "moon": (48, 5.125, 10.07, 0, 0),
    "mercury": (115, 43.13, 5.75, 0, 0),
    "venus": (622.5, 447.85, 12.95, 0, 0),
    "mars": (5040, 3318, 504.3, 0, 0),
    "jupiter": (11504, 2462, 527.2, 0, 0),
    "saturn": (17026, 1998, 971.2, 0, 0)
}

for i in range(iterations):
    for body, (radius, size, e, oX, oY) in bodies.items():
        k = radius
        x = (radius + size) * math.cos(math.radians(i)) - e * math.cos(((radius + size) / size) * math.radians(i))
        y = (radius + size) * math.sin(math.radians(i)) - e * math.sin(((radius + size) / size) * math.radians(i))
        if i == 0:
            eps.add("%f %f moveto" % (x / scale, y / scale))
        else:
            eps.add("%f %f moveto" % (oX / scale, oY / scale))
        eps.add("%f %f lineto" % (x / scale, y / scale))
        eps.add("stroke")
        bodies[body] = (radius, size, e, x, y)

eps.add("closepath")
eps.add("showpage")
eps.add("%EOF")
print("HELLO")
eps.write()
