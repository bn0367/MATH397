fh = .5 * (sqrt(5) - 1);
fi = 1 - fh;
rr = 10 * cos(pi / 5);
tt = 10 * sin(pi / 5)

bug <- function(n, x, y, p, q, r, s)
    if (n > 1) {
        lines(c(x + p, x + fh * (p + r)), c(y + q, y + fh * (q + s)));
        lines(c(x + fh * p, x + fh * (p + r)), c(y + fh * q, y + fh * (q + s)));
        bug(n - 1, x + fh * (p + r), y + fh * (q + s), - fh * r, - fh * s, - fh * p, - fh * q);
        bug(n - 1, x + p + r, y + q + s, - fi * (p + r), - fi * (q + s), fi * p - fh * r, fi * q - fh * s);
        lil(n - 1, x + fh * (p + r), y + fh * (q + s), fi * p - fh * r, fi * q - fh * s, - fh * r, - fh * s);
    } else {
        polygon(c(x, x + p, x + p + r), c(y, y + q, y + q + s), col = 7, border = NA);
        lines(c(x, x + p, x + p + r), c(y, y + q, y + q + s))
    }

lil <- function(n, x, y, p, q, r, s)
    if (n > 1) {
        lines(c(x + p, x + fh * r), c(y + q, y + fh * s));
        lil(n - 1, x + p, y + q, r - p, s - q, fh * r - p, fh * s - q);
        bug(n - 1, x + p, y + q, fh * r - p, fh * s - q, - fh * r, - fh * s)
    } else {
        polygon(c(x, x + p, x + r), c(y, y + q, y + s), col = 2, border = NA);
        lines(c(x + r, x, x + p), c(y + s, y, y + q))
    }

plot(1, 1, xlim = c(5.2, 8.6), ylim = c(0.18, 3.58), type = "n", xaxt = "n", yaxt = "n", xlab = "", ylab = "")
lil(10, 0, 0, 10, 0, rr, tt)