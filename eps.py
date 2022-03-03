class Eps:
    def __init__(self, name, size, linejoin=1, linecap=1, linewidth=1):
        self.SIZE = size
        self.name = name
        self.linejoin = linejoin
        self.linecap = linecap
        self.linewidth = linewidth
        self.file = open("%s.eps" % name, "w")
        self.lines = [
            "%!PS-Adobe-3.0 EPSF-3.0\n",
            "%%BoundingBox: 0 0 %d %d\n" % (size, size),
            "%d setlinejoin %d setlinewidth %d setlinecap " % (self.linejoin, self.linewidth, self.linecap),
        ]

    def add(self, line):
        self.lines.append(line + "\n")

    def write(self):
        self.file.writelines(self.lines)
        self.file.close()
