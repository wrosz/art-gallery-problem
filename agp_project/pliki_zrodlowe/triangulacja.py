# Funkcje związane z triangulacją i znajdowaniem liczby strażników, oraz z ilustrowaniem wyników

import csv
from matplotlib.markers import MarkerStyle
from pygame import color
import tripy
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.patches as patches
import matplotlib
matplotlib.use('Agg')
import numpy as np
from pliki_zrodlowe.konfiguracja_okna import canvas_width, canvas_height


def read_coordinates_from_csv(filepath):
    '''Czyta współrzędne punktów wielokąta z pliku .csv.
    Zwraca krotkę ze współrzędnymi.
    '''
    with open(filepath) as f:
        reader = csv.reader(f, delimiter=',')
        next(reader, None)  # ominięcie pierwszej linijki z nagłówkami
        return tuple([(int(x), int(y)) for x, y in reader])


def triangulate_polygon(x):
    '''Zwraca krotkę krotek definiującą trójkąty, na które jest podzielony wielokąt.
    Argumenty:
    x - lista (krotka) współrzędnych kolejnych wierzchołków wielokąta
    '''
    return tripy.earclip(x)


def three_coloring(vertices, triangles):
    '''Znajduje dobre 3-kolorowanie wierzchołków striangularyzowanego wielokąta.
    Zwraca słownik postaci {vertex:color}, gdzie:
    vertex - krotka ze współrzędnymi wierzchołka
    color - kolor wierzchołka, liczba 0, 1, lub 2
    '''
    triangles = np.array(triangles)
    vertices = (v for v in vertices)
    colors = {vertex:-1 for vertex in vertices}  # słownik z kolorami wierzchołków, -1 oznacza, że wierzchołek jeszcze nie jest pokolorowany
    to_color = np.array([True for triangle in triangles])  # jeśli True, to znaczy że trójkąt ma jeszcze co najmniej jeden niepokolorowany wierzchołek
    indexes = np.arange(len(triangles))  # indeksy wszystkich trójkątów w triangles

    # pokolorowanie pierwszego trójkąta:
    triangle = tuple(triangles[0])
    colors[tuple(triangle[0])] = 0
    colors[tuple(triangle[1])] = 1
    colors[tuple(triangle[2])] = 2
    to_color[0] = False

    while any(to_color): # powtarzanie pętli tak długo, aż wszystkie trójkąty są pokolorowane
        for i in indexes[to_color]:
            triangle = triangles[i]
            triangle_colors = np.array([colors[tuple(triangle[i])] for i in range(3)])  # wektor kolorów wierzchołków trójkąta
            if sum(triangle_colors >= 0) < 2:  # jeśli jescze co najmniej dwa niepokolorowane, przechodzimy do kolejnego trójkąta
                continue
            elif sum(triangle_colors >= 0) == 3:
                to_color[i] = False  # jeśli jakiś trójkąt pokolorowaliśmy przy okazjy w poprzedniej iteracji, to wyrzucamy go ze zbioru do pokolorowania i kontynuujemy
                continue
            third_vertex = triangle[np.array([colors[tuple(vertex)] == -1 for vertex in triangle])][0]
            third_color = np.setdiff1d(np.array([-1, 0, 1, 2]), triangle_colors)[0]
            colors[tuple(third_vertex)] = int(third_color)
            to_color[i] = False
    return colors


def min_guards(coloring):
    '''Zwraca dwa obiekty:
    guards - lista ze strażnikami (współrzędnymi wierzchołków pokolorowanych na najrzadziej występujący kolor
    min_color - liczba 0, 1 lub 2 oznaczająca najrzadziej występujący kolor
    '''
    colors_occ = [0, 0, 0]
    guards = []
    for vertex, color in coloring.items():
        colors_occ[color] += 1
    min_occ = min(colors_occ)  # minimalna liczba strażników
    min_color = colors_occ.index(min_occ)  # kolor tych strażników
    for vertex, color in coloring.items():
        if color == min_color:
            guards.append(vertex)
    return guards, min_color


def oblicz_liczbe_straznikow():
    '''Zwraca liczbę strażników dla wielokąta zdefiniowanego w pliku wspolrzedne_punktow.csv'''
    f = 'pliki_wielokat/wspolrzedne_punktow.csv'
    coordinates = read_coordinates_from_csv(f)
    triangles = triangulate_polygon(coordinates)
    coloring = three_coloring(coordinates, triangles)
    guards, min_color = min_guards(coloring)
    return len(guards)
    

def zapisz_obrazy():
    '''Zapisuje trzy obrazy:
    rysunek_wielokat.png - wielokąt wypełniony kolorem w środku
    rysunek_triangulacja.png - wielokąt podzielony na trójkąty, z 3-kolorowaniem wierzchołków
    rysunek_straznicy.png - wielokąt z zaznaczonymi strażnikami i obszarami, które widzą (jeszcze niegotowe)
    '''

    # pobranie danych z pliku i obliczenie triangulacji, minimalnego kolorowania i strażników
    f = 'pliki_wielokat/wspolrzedne_punktow.csv'
    coordinates = read_coordinates_from_csv(f)
    triangles = triangulate_polygon(coordinates)
    coloring = three_coloring(coordinates, triangles)
    guards, min_color = min_guards(coloring)

    # rysowanie wykresu
    fig, ax = plt.subplots(frameon=False)
    ax.set_aspect('equal')
    ax.set_xlim(0, canvas_width)
    ax.set_ylim(0, canvas_height)
    ax.set_axis_off()

    marker_strings = ['ro', 'go', 'bo']

    # pokolorowany wielokąt ze strażnikami
    x = [point[0] for point in coordinates]
    y = [point[1] for point in coordinates]
    plt.fill(x, y, 'y')
    for guard in guards:  # zaznaczenie wierzchołków ze strażnikami
        ax.plot(guard[0], guard[1], marker_strings[min_color], markersize = 10, markeredgecolor='k')
    plt.savefig('pliki_wielokat/rysunek_wielokat.png', bbox_inches='tight', pad_inches=0, dpi=600)

    # pokolorowany wielokąt + triangulacja + kolorowanie wierzchołków
    for triangle in triangles:
        x = [point[0] for point in triangle] + [triangle[0][0]]
        y = [point[1] for point in triangle] + [triangle[0][1]]
        ax.plot(x, y, 'k-', marker='o', markersize=2)
    for vertex in coordinates:
        vertex = tuple(vertex)
        marker_str = marker_strings[coloring[vertex]]
        if coloring[vertex] == min_color:
            ax.plot(vertex[0], vertex[1], marker_str, markersize=10, markeredgecolor='k')  # wyróżnienie wierzchołków będących strażnikami
        else:
            ax.plot(vertex[0], vertex[1], marker_str, markersize=5)
    plt.savefig('pliki_wielokat/rysunek_triangulacja.png', bbox_inches='tight', pad_inches=0, dpi=600)

    # obszary, które widzą strażnicy
    plt.cla()
    ax.set_aspect('equal')
    ax.set_xlim(0, canvas_width)
    ax.set_ylim(0, canvas_height)
    ax.set_axis_off()
    guards_x = [guard[0] for guard in guards]
    guards_y = [guard[1] for guard in guards]
    guard_colors = plt.cm.gist_rainbow(np.linspace(0, 1, len(guards)))
    np.random.shuffle(guard_colors)
    for triangle in triangles:
        x = [triangle[i][0] for i in range(3)]
        y = [triangle[i][1] for i in range(3)]
        for i in range(3):
            try:
                guard_index = guards.index(triangle[i])
                break
            except ValueError:
                continue
        triangle_color = guard_colors[guard_index]
        plt.fill(x, y, color=triangle_color)
    plt.scatter(guards_x, guards_y, c=guard_colors, linewidth=1, s=100, edgecolor='black')
    plt.savefig('pliki_wielokat/rysunek_straznicy.png', bbox_inches='tight', pad_inches=0, dpi=600)
        