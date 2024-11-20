# Plik zawierający funkcje potrzebne do stworzenia okna w Pygame i narysowania jego elementów, wywołane w main().
# Zawiera też zmienne konfigurujące wielkość i położenie poszczególnych elementów interfejsu oraz krotki definiujące podstawowe kolory.

import pygame
from typing import List, Union
from funkcje_pomocnicze import wspol_osiowe, wyswietl_tekst
from konfiguracja_okna import *


def init_window():
    '''Inicjalizuje pygame i tworzy okno.'''
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    screen.fill(GREY)
    return screen


def draw_canvas_area(screen):
    '''Rysuje główne płótno na obszarze canvas_rect.'''
    pygame.draw.rect(screen, WHITE, canvas_rect)
    return canvas_rect


def draw_komunikat_area(screen):
    '''Rysuje obszar na komunikaty na górze okna.'''
    pygame.draw.rect(screen, WHITE, komunikat_rect)
    return komunikat_rect


def draw_grid(screen):
    '''Rysuje siatkę na płótnie.'''
    for x in range(0, canvas_width + 1, 20):  # Linie pionowe siatki
        x_pos = canvas_rect.left + x
        if x % 100 == 0:
            col = BLACK
        else: col = GREY
        pygame.draw.line(screen, col, (x_pos, canvas_rect.bottom), (x_pos, canvas_rect.top), 1, )
    for y in range(0, canvas_height + 1, 20):  # Linie poziome siatki
        y_pos = canvas_rect.bottom - y
        if y % 100 == 0:
            col = BLACK
        else: col = GREY
        pygame.draw.line(screen, col, (canvas_rect.left, y_pos), (canvas_rect.right, y_pos), 1)


def draw_axes(screen):
    '''Rysuje osie X i Y oraz etykiety co 100 jednostek.'''
    # Rysowanie linii osi
    pygame.draw.line(screen, BLACK, canvas_rect.topleft, canvas_rect.bottomleft, 2)  # Oś Y
    pygame.draw.line(screen, BLACK, canvas_rect.bottomleft, canvas_rect.bottomright, 2)  # Oś X

    font = pygame.font.SysFont(None, 24)

    # Rysowanie etykiet na osi X co 100 jednostek
    for x in range(0, canvas_width + 1, 100):
        x_pos = canvas_rect.left + x
        label = font.render(str(x), True, BLACK)
        screen.blit(label, (x_pos - 10, canvas_rect.bottom + 10))

    # Rysowanie etykiet na osi Y co 100 jednostek
    for y in range(100, canvas_height + 1, 100):
        y_pos = canvas_rect.bottom - y
        label = font.render(str(y), True, BLACK)
        screen.blit(label, (canvas_rect.left - 35, y_pos - 6))


def wyswietl_wspolrzedne_kursora(screen, mouse_x, mouse_y):
    '''Wyświetla współrzędne kursora myszy jeśli znajduje się on w obszarze płótna, w przeciwnym przypadku współrzędne znikają'''

    (x, y) = wspol_osiowe((mouse_x, mouse_y), canvas_rect)
    if canvas_rect.collidepoint(mouse_x, mouse_y):
        wyswietl_tekst(f'x:{x}, y:{y}', screen, wspolrzedne_rect, font_size=15, background_color=GREY)
    else:
        pygame.draw.rect(screen, GREY, wspolrzedne_rect)  # współrzędne znikają, gdy kursor myszy poza obszarem płótna


def wyswietl_wielokat(screen, sciezka_do_pliku:str):
    '''Wyświetla na płótnie wielokąt załadowany z pliku'''

    rysunek = pygame.image.load(sciezka_do_pliku)
    rysunek = pygame.transform.scale(rysunek, (canvas_width, canvas_height))
    draw_canvas_area(screen) # wyczyszczenie płótna
    screen.blit(rysunek, canvas_rect.topleft)  # naniesienie striangulowanego wielokąta
    draw_grid(screen)
    

def wyswietl_menu(screen, ktory_aktywny:Union[int, None], ktore_mozliwe:List[int]):
    dlugosc_menu = 4
    menu = [None for i in range(dlugosc_menu)]  # prostokąty z elementami menu
    teksty = ['Pokaż wielokąt', 'Pokaż triangulację', ['Pokaż obszary,', 'które widzą strażnicy'], 'Rysuj nowy wielokąt']  # teksty wyświetlane na elementach menu
    kolory_tekstu = [BLACK if ktore_mozliwe[i] else DARK_GREY for i in range(3)] + [WHITE]
    kolory_menu = [WHITE if ktore_mozliwe[i] else LIGHT_GREY for i in range(3)] + [DARK_RED]  # kolory elementów menu, zależne od argumentów ktory_aktywny i ktore_mozliwe
    if ktory_aktywny is not None:
        kolory_tekstu[ktory_aktywny] = BLACK
        kolory_menu[ktory_aktywny] = YELLOW
    
    for i in range(dlugosc_menu):
        menu[i] = pygame.Rect(canvas_rect.right + 20, canvas_rect.top + (i + 1) * 100, odstep_prawa-40, 80)
        wyswietl_tekst(teksty[i], screen, menu[i], color=kolory_tekstu[i], background_color=kolory_menu[i])

    return menu

def wyswietl_liczbe_straznikow(screen, liczba_straznikow):
    height_offset = 12

    ramka_wspolrzedne = pygame.Rect(canvas_rect.right + 20, komunikat_rect.top, odstep_prawa-40, komunikat_height + odstep_gora + 60)
    tekst1_wspolrzedne = pygame.Rect(canvas_rect.right + 20, komunikat_rect.top + height_offset, odstep_prawa-40, komunikat_height)
    tekst2_wspolrzedne = pygame.Rect(canvas_rect.right + 20, komunikat_rect.bottom + height_offset, odstep_prawa-40, komunikat_height)

    tekst1 = 'Liczba strażników:'
    fontsize1 = 20
    fontsize2 = 60
    if liczba_straznikow is None:
        kolor_ramki = DARK_GREY
        kolor1 = LIGHT_GREY
        kolor2 = LIGHT_GREY
        tekst2 = '...'
    else:
        kolor_ramki = GREEN
        kolor1 = BLACK
        kolor2 = BLACK
        tekst2 = str(liczba_straznikow)
    
    pygame.draw.rect(screen, color=kolor_ramki, rect=ramka_wspolrzedne)
    wyswietl_tekst(tekst1, screen, tekst1_wspolrzedne, font_size=fontsize1, color=kolor1, background_color=kolor_ramki)
    wyswietl_tekst(tekst2, screen, tekst2_wspolrzedne, font_size=fontsize2, color=kolor2, background_color=kolor_ramki)


def wyczysc_plotno(screen):
    pygame.draw.rect(screen, GREY, pygame.Rect(0, komunikat_height + odstep_gora,
                                               odstep_lewa + canvas_width + 20, window_height - (komunikat_height + odstep_gora)))
    draw_canvas_area(screen)
    draw_grid(screen)
    draw_axes(screen)
