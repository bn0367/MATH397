strings = """........................O
......................O.O
............OO......OO............OO
...........O...O....OO............OO
OO........O.....O...OO
OO........O...O.OO....O.O
..........O.....O.......O
...........O...O
............OO""".split("\n")
for i in range(len(strings)):
	strings[i] = strings[i].ljust(37, '.')
	for j in range(len(strings[i])):
		if strings[i][j] == "O":
			print("%d %d pack 1 def" % (i, j))

