from turtle import *

IMG_SIZE = (30, 24)

nodes = [int(x) for x in
         open("output.sol", "r").read().replace(str(IMG_SIZE[0] * IMG_SIZE[1]), "").replace("\n", "").split(" ")[
         :-1]] + [0]
speed(0)
old = -1
penup()
goto(-300, -300)
pendown()
for i in nodes:
    goto(i % IMG_SIZE[1] * 10 - 300, i // IMG_SIZE[1] * 10 - 300)
    if old != -1:
        goto(old % IMG_SIZE[1] * 10 - 300, old // IMG_SIZE[1] * 10 - 300)
    old = i

while (True):
    pass
