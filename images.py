import math
from PIL import Image
import random

from eps import Eps


def convert(x, y, old_width, old_height, new_width, new_height):
    x = x * new_width / old_width
    y = y * new_height / old_height
    return x, y


img = Image.open("image.jpg")

SIZE = 500

eps = Eps("image", SIZE)
eps.add("%d %d translate\n" % (SIZE // 2, SIZE // 2))
eps.add("150 rotate\n")

a, b = 0.2, 0.3
x, y = 0, 0
oX, oY = 0, 0
i = 0
eps.add("newpath\n")
while SIZE // 2 > x > -SIZE // 2:
    oX, oY = x, y
    x = (a + (b * i)) * math.cos(i)
    y = (a + (b * i)) * math.sin(i)
    eps.add("%f %f moveto" % (oX, oY))
    eps.add("%f %f lineto" % (x, y))
    nX, nY = math.floor(500 - (oX + SIZE // 2 + 1)), math.floor(
        oY + SIZE // 2 + 1)  # convert(, SIZE, SIZE, img.width, img.height)
    noX, noY = math.floor(500 - (oX + SIZE // 2 + 1)), math.floor(oY + SIZE // 2 + 1)
    # get the midpoint of the line for more accurate (?) colors
    rX, rY = (nX + noX) // 2, (nY + noY) // 2
    try:
        pixel = img.getpixel((rX, rY))
        brightness = math.sqrt(0.299 * pixel[0] ** 2 + 0.587 * pixel[1] ** 2 + 0.114 * pixel[2] ** 2)
        # eps.add("%f %f %f setrgbcolor" % (pixel[0] / 255, pixel[1] / 255, pixel[2] / 255))
        eps.add("%f setgray" % (brightness / 255))
        eps.add("%f setlinewidth" % ((255 - brightness) / 63))
    except IndexError:
        pass
    eps.add("stroke")
    i += 1

print(i)
eps.add("fill\nclosepath\nshowpage\n%EOF")
eps.write()
