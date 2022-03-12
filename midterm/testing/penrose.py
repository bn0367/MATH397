import math
import turtle

fh = .5 * (math.sqrt(5) - 1)
fi = 1 - fh
rr = 10 * math.cos(math.pi / 5)
tt = 10 * math.sin(math.pi / 5)

tur = turtle.Turtle()

offset = 250

scale = lambda n: n * 100


def bug(n, x, y, p, q, r, s):
    if n > 1:

        bug(n - 1, x + fh * (p + r), y + fh * (q + s), - fh * r, - fh * s, - fh * p, - fh * q)
        bug(n - 1, x + p + r, y + q + s, - fi * (p + r), - fi * (q + s), fi * p - fh * r, fi * q - fh * s)
        lil(n - 1, x + fh * (p + r), y + fh * (q + s), fi * p - fh * r, fi * q - fh * s, - fh * r, - fh * s)
    else:
        # polygon(c(x, x + p, x + p + r), c(y, y + q, y + q + s), col=7, border=NA);
        tur.penup()
        tur.goto(x * scale(n) - offset, y * scale(n) - offset)
        tur.pendown()
        tur.goto((x + p) * scale(n) - offset, (y + q) * scale(n) - offset)
        tur.goto((x + p + r) * scale(n) - offset, (y + q + s) * scale(n) - offset)


def lil(n, x, y, p, q, r, s):
    if n > 1:
        lil(n - 1, x + p, y + q, r - p, s - q, fh * r - p, fh * s - q)
        bug(n - 1, x + p, y + q, fh * r - p, fh * s - q, - fh * r, - fh * s)
    else:
        # polygon(c(x, x + p, x + r), c(y, y + q, y + s), col=2, border=NA);
        tur.penup()
        tur.goto((x + r) * scale(n) - offset, (y + s) * scale(n) - offset)
        tur.pendown()
        tur.goto(x * scale(n) - offset, y * scale(n) - offset)
        tur.goto((x + p) * scale(n) - offset, (y + q) * scale(n) - offset)


tur.hideturtle()
tur.speed(0)

lil(7, 0, 0, 10, 0, rr, tt)

tur.penup()
while True:
    tur.goto(0, 0)
