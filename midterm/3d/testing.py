import math
from re import L
import matplotlib.pyplot as plt

def icosphere(subdivisions):
	vertices = []
	faces = []
	def middlePoint(p1, p2):
		x = (p1[0] + p2[0]) / 2
		y = (p1[1] + p2[1]) / 2
		z = (p1[2] + p2[2]) / 2
		return (x, y, z)
	def fixPosition(point):
		x, y, z = point
		length = math.sqrt(x**2 + y**2 + z**2)
		return (x/length, y/length, z/length)

	t = (1 + math.sqrt(5)) / 2

	vertices.append(fixPosition((-1, t, 0)))
	vertices.append(fixPosition(((1, t, 0))))
	vertices.append(fixPosition((-1, -t, 0)))
	vertices.append(fixPosition((1, -t, 0)))

	vertices.append(fixPosition((0, -1, t)))
	vertices.append(fixPosition((0, 1, t)))
	vertices.append(fixPosition((0, -1, -t)))
	vertices.append(fixPosition((0, 1, -t)))

	vertices.append(fixPosition((t, 0, -1)))
	vertices.append(fixPosition((t, 0, 1)))
	vertices.append(fixPosition((-t, 0, -1)))
	vertices.append(fixPosition((-t, 0, 1)))

	faces.append([vertices[0], vertices[11], vertices[5]])
	faces.append([vertices[0], vertices[5], vertices[1]])
	faces.append([vertices[0], vertices[1], vertices[7]])
	faces.append([vertices[0], vertices[7], vertices[10]])
	faces.append([vertices[0], vertices[10], vertices[11]])

	faces.append([vertices[1], vertices[5], vertices[9]])
	faces.append([vertices[5], vertices[11], vertices[4]])
	faces.append([vertices[11], vertices[10], vertices[2]])
	faces.append([vertices[10], vertices[7], vertices[6]])
	faces.append([vertices[7], vertices[1], vertices[8]])

	faces.append([vertices[3], vertices[9], vertices[4]])
	faces.append([vertices[3], vertices[4], vertices[2]])
	faces.append([vertices[3], vertices[2], vertices[6]])
	faces.append([vertices[3], vertices[6], vertices[8]])
	faces.append([vertices[3], vertices[8], vertices[9]])

	faces.append([vertices[4], vertices[9], vertices[5]])
	faces.append([vertices[2], vertices[4], vertices[11]])
	faces.append([vertices[6], vertices[2], vertices[10]])
	faces.append([vertices[8], vertices[6], vertices[7]])
	faces.append([vertices[9], vertices[8], vertices[1]])

	for i in range(subdivisions):
		newFaces = []
		for face in faces:
			a = face[0]
			b = face[1]
			c = face[2]
			m1 = middlePoint(a, b)
			m2 = middlePoint(b, c)
			m3 = middlePoint(c, a)
			print(m1, m2, m3, sep="\n")
			newFaces.append([a, m1, m3])
			newFaces.append([b, m2, m1])
			newFaces.append([c, m3, m2])
			newFaces.append([m1, m2, m3])
			print(newFaces)
			input()
		faces = newFaces
	
	print(faces[-1])
	print(len(faces))
	return vertices, faces

icosphere(3)

# ps: [[0.7288059 0.318994045 -0.0657163858] [0.7288059 0.318994045 0.0657163858] [0.769420862 0.212662697 0.0]]
# py: [(0.7288059222647001, 0.318994053132015, -0.0657163890148917), (0.7288059222647001, 0.318994053132015, 0.0657163890148917), (0.7694208842938134, 0.21266270208801, 0.0)]

l1 = [[[-0.525731087, 0.850650787, 0.0], [-0.809017, 0.5, 0.309016973], [-0.309016973, 0.809017, 0.5]], [[-0.850650787, 0.0, 0.525731087], [-0.5, 0.309016973, 0.809017], [-0.809017, 0.5, 0.309016973]], [[0.0, 0.525731087, 0.850650787], [-0.309016973, 0.809017, 0.5], [-0.5, 0.309016973, 0.809017]], [[-0.809017, 0.5, 0.309016973], [-0.5, 0.309016973, 0.809017], [-0.309016973, 0.809017, 0.5]]]
l2 = [[(-0.5257311121191336, 0.85065080835204, 0.0), (-0.6881909602355868, 0.42532540417602, 0.2628655560595668), (-0.2628655560595668, 0.6881909602355868, 0.42532540417602)], [(-0.85065080835204, 0.0, 0.5257311121191336), (-0.42532540417602, 0.2628655560595668, 0.6881909602355868), (-0.6881909602355868, 0.42532540417602, 0.2628655560595668)], [(0.0, 0.5257311121191336, 0.85065080835204), (-0.2628655560595668, 0.6881909602355868, 0.42532540417602), (-0.42532540417602, 0.2628655560595668, 0.6881909602355868)], [(-0.6881909602355868, 0.42532540417602, 0.2628655560595668), (-0.42532540417602, 0.2628655560595668, 0.6881909602355868), (-0.2628655560595668, 0.6881909602355868, 0.42532540417602)]]