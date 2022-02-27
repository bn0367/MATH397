class Eps:
    def __init__(self, name, size, linejoin=1, linecap=1, linewidth=1):
        self.SIZE = size
        self.name = name
        self.linejoin = linejoin
        self.linecap = linecap
        self.linewidth = linewidth
        self.file = open("%s.eps" % name, "w")
        self.lines = ["%!PS-Adobe-3.0 EPSF-3.0", "%%BoundingBox: 0 0 %d %d" % (size, size),
                      "%d setlinejoin" % self.linejoin,
                      "%d setlinecap" % self.linecap,
                      "%d setlinewidth" % self.linewidth]

    def add(self, line):
        self.lines.append(line)

    def write(self):
        for line in self.lines:
            self.file.write(line + "\n")
        self.file.close()
