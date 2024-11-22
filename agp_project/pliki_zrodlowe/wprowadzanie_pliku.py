# Funkcje do �adowania wsp�rz�dnych z pliku

import re
from itertools import islice
import tkinter as tk
from tkinter import filedialog
from pliki_zrodlowe.konfiguracja_okna import canvas_width, canvas_height
from pliki_zrodlowe.funkcje_pomocnicze import sprawdz_samoprzeciecia, zapisz_wspolrzedne


def plik_z_okna_dialogowego():
    '''Zwraca ścieżkę pliku wybranego przez użytkownika w oknie dialogowym, za pomocą biblioteki Tkinter'''
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title='Wybierz plik')
    root.destroy()
    return file_path


def akceptuj_linijke(line:str, line_number=None):
    '''Sprawdza, czy string line jest postaci "X,Y", gdzie:
    X - liczba całkowita z przedziału [0, canvas_width],
    Y - liczba całkowita z przedziału [0, canvas_height]
    Jeżeli któryś z warunków nie jest spełniony, to rzucany jest wyjątek z odpowiednim komunikatem.
    '''
    if line_number == 1:  # sprawdzenie linijki z nagłówkiem
        if line == 'X,Y\n':
            return None
        else:
            raise Exception('Pierwsza linijka powinna być napisem "X,Y"')

    if not re.fullmatch(r"^[0123456789]+,[0123456789]+\n$", line):  # czy linijka jest postaci X,Y
        raise Exception(f'Nie można odczytać wspórzędnych z linijki {line_number}')

    x, y = line.split(sep=',')
    x, y = int(x), int(y)
    if (not 0  <= x <= canvas_width) or (not 0 <= y <= canvas_height):  # czy wspórzędne punktu nie wykraczają poza zakres płótna
        raise Exception(f'Wspórzędne w linijce {line_number} nie mieszczą się na płótnie')

    return x, y


def sprawdz_plik(file_path:str):
    '''Sprawdza, czy plik spełnia następujące warunki:
    - jest w formacie .csv
    - 
    '''
    if not file_path.endswith('.csv'):  # sprawdza, czy plik jest w formacie .csv
        raise Exception('Wskazany plik nie jest w formacie .csv')

    punkty = []

    with open(file_path) as f:
        for line_number, line in enumerate(f, start=1):
            punkt = akceptuj_linijke(line, line_number)  # w pierwszej linijce sprawdzamy tylko, czy nie rzuca wyjątku (punkt = None)
            if line_number > 1:  # później dopisujemy punkty odczytane w pliku do listy
                punkty.append(punkt)

    if len(punkty) < 3:  # wielokąt musi mieć co najmniej trzy punkty
        raise Exception('Plik musi zawierać co najmniej trzy punkty')

    # sprawdzenie samoprzecięć
    if sprawdz_samoprzeciecia(punkty[0], punkty):
        raise Exception('Wielokąt zawiera samoprzecięcia')
    for i in range(1, len(punkty)):
        sprawdz_samoprzeciecia(punkty[i], punkty[:i-1])

    # zapisanie odczytanych współrzędnych w pliku w projekcie, jeśli wszystko się zgadza
    zapisz_wspolrzedne(punkty)