import cv2
import math

IMG_SIZE = (30, 24)

img = cv2.imread('monster.jpg', 0)
img = cv2.resize(img, IMG_SIZE)

coords = lambda idx: (idx // IMG_SIZE[1], idx % IMG_SIZE[1])

# full matrix of "distances" between every pixel from img
distances = []
for i in range(IMG_SIZE[0] * IMG_SIZE[1]):
    distances.append([])
    for j in range(IMG_SIZE[0] * IMG_SIZE[1]):
        # combine color difference and actual distance to get a "distance"
        # (making sure that the real distance doesn't overlap rows)
        first = coords(i)
        second = coords(j)
        color_diff = (255 - img[first[1]][
            first[0]])  # int(math.sqrt((int(img[first[1]][first[0]]) - int(img[second[1]][second[0]])) ** 2)) // 5
        distance = color_diff + abs(first[0] - second[0]) + abs(first[1] - second[1])
        distances[i].append(distance)

template = open('template.tsp', 'r').read()
output = open('output.tsp', 'w')

matrix = '\n'.join(
    ' '.join(str(distances[i][j]) for j in range(IMG_SIZE[0] * IMG_SIZE[1])) for i in range(IMG_SIZE[0] * IMG_SIZE[1]))
print(matrix)

output.write(template.format(IMG_SIZE[0] * IMG_SIZE[1], matrix))
