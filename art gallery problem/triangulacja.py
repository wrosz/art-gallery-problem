import csv
import tripy
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.patches as patches



def read_coordinates_from_csv(filepath):
    with open(filepath) as f:
        return [[int(x), int(y)] for x, y in csv.reader(f, delimiter=',')]


def triangulate_polygon(x):

    return tripy.earclip(x)


def draw_polygon(triangles, guards):

    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    for triangle in triangles:
        x = [point[0] for point in triangle] + [triangle[0][0]]
        y = [point[1] for point in triangle] + [triangle[0][1]]
        ax.plot(x, y, 'b-', marker='o', markersize=5)

    for guard in guards:
        for g in guard:
            ax.plot(*g, 'ro', markersize=5)

    ax.axis('off')
    plt.gca().invert_yaxis()
    plt.show()


def three_coloring(vertices, triangles):

    adjacency_list = defaultdict(set)
    for triangle in triangles:
        for i in range(3):
            for j in range(i + 1, 3):
                adjacency_list[triangle[i]].add(triangle[j])
                adjacency_list[triangle[j]].add(triangle[i])
    colors = {}
    available_colors = {0, 1, 2}
    for vertex in vertices:
        vertex = tuple(vertex)
        neighbor_colors = {colors[neighbor] for neighbor in adjacency_list[vertex] if neighbor in colors}
        for color in available_colors:
            if color not in neighbor_colors:
                colors[vertex] = color
                break
    return colors

def min_guards(coloring):
    colors_occ = [0, 0, 0]
    guards = []
    minimum = []
    for vertex, color in coloring.items():
        colors_occ[color] +=1
    min_occ = min(colors_occ)
    for i in range(3):
        if colors_occ[i] == min_occ:
            minimum.append(i)
    for el in minimum:
        g = []
        for vertex, color in coloring.items():
            if color == el:
                g.append(vertex)
        guards.append(g)
    return guards


f = "wspolrzedne_punktow.csv"
coordinates = read_coordinates_from_csv(f)
# print(coordinates)
triangles = triangulate_polygon(coordinates)
print(triangles)
coloring = three_coloring(coordinates, triangles)
print(coloring)
guards = min_guards(coloring)
# print(guards)
draw_polygon(triangles, guards)




