import math
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
			newFaces.append([a, m1, m3])
			newFaces.append([b, m2, m1])
			newFaces.append([c, m3, m2])
			newFaces.append([m1, m2, m3])
		faces = newFaces
	
	print(faces[-10])
	print(len(faces))
	return vertices, faces

icosphere(3)