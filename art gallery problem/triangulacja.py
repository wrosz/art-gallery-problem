import csv
from pygame import color
import tripy
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.patches as patches
import matplotlib
matplotlib.use('Agg')
from rysowanie_okna import canvas_width, canvas_height


    
def read_coordinates_from_csv(filepath):
    with open(filepath) as f:
        reader = csv.reader(f, delimiter=',')
        next(reader, None)  
        return [[int(x), int(y)] for x, y in reader]


def triangulate_polygon(x):
    return tripy.earclip(x)


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


def zapisz_obrazy():

    # pobranie danych z pliku i obliczenie triangulacji, minimalnego kolorowania i strażników
    f = "wspolrzedne_punktow.csv"
    coordinates = read_coordinates_from_csv(f)
    triangles = triangulate_polygon(coordinates)
    coloring = three_coloring(coordinates, triangles)
    guards = min_guards(coloring)

    # rysowanie wykresu
    fig, ax = plt.subplots(frameon=False)
    ax.set_aspect('equal')
    ax.set_xlim(0, canvas_width)
    ax.set_ylim(0, canvas_height)
    ax.set_axis_off()

    # sam pokolorowany wielokąt
    x = [point[0] for point in coordinates]
    y = [point[1] for point in coordinates]
    plt.fill(x, y, "y")
    plt.savefig("rysunek_wielokat.png", bbox_inches='tight', pad_inches=0, dpi=600)

    # pokolorowany wielokąt + triangulacja + kolorowanie
    for triangle in triangles:
        x = [point[0] for point in triangle] + [triangle[0][0]]
        y = [point[1] for point in triangle] + [triangle[0][1]]
        ax.plot(x, y, 'k-', marker='o', markersize=5)
    for vertex in coordinates:
        vertex = tuple(vertex)
        if coloring[vertex] == 0:
            marker_str = 'ro'
        elif coloring[vertex] == 1:
            marker_str = 'go'
        elif coloring[vertex] == 2:
            marker_str = 'bo'
        ax.plot(vertex[0], vertex[1], marker_str, markersize=5)

        plt.savefig("rysunek_triangulacja.png", bbox_inches='tight', pad_inches=0, dpi=600)


        # for guard in guards:
        # for g in guard:
        #     ax.plot(*g, 'ro', markersize=5)

