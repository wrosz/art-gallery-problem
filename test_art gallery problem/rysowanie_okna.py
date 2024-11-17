# Plik zawierający funkcje potrzebne do stworzenia okna w Pygame i narysowania jego elementów, wywołane w main().
# Zawiera też zmienne konfigurujące wielkość i położenie poszczególnych elementów interfejsu oraz krotki definiujące podstawowe kolory.

import pygame
from test_funkcje_pomocnicze import wspol_osiowe, wyswietl_tekst


# ---------------------------- KONFIGURACJA ----------------------------

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
RED = (255, 0, 0)

# Wymiary elementów okna
canvas_width, canvas_height = 700, 500  # Wymiary płótna
komunikat_width, komunikat_height = canvas_width, 40  # Wymiary komunikatów wyświetlanych na górze okna
odstep_gora, odstep_boki, odstep_dol = 10, 40, 80  # Odstępy elementów od krawędzi

# Wyliczenia wymiarów okna
window_width = canvas_width + 2 * odstep_boki
window_height = canvas_height + komunikat_height + 2 * odstep_gora + odstep_dol

# Współrzędne elementów
canvas_rect = pygame.Rect(odstep_boki, komunikat_height + 2 * odstep_gora, canvas_width, canvas_height)
komunikat_rect = pygame.Rect(odstep_boki, odstep_gora, komunikat_width, komunikat_height)
wspolrzedne_rect = pygame.Rect(odstep_boki, window_height - odstep_dol/2, canvas_width, odstep_dol/2)


# ---------------------------- FUNKCJE ----------------------------

def init_window():
    """Inicjalizuje pygame i tworzy okno."""
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    screen.fill(GREY)
    return screen


def draw_canvas_area(screen):
    """Rysuje główne płótno na obszarze canvas_rect."""
    pygame.draw.rect(screen, WHITE, canvas_rect)
    return canvas_rect


def draw_komunikat_area(screen):
    """Rysuje obszar na komunikaty na górze okna."""
    pygame.draw.rect(screen, WHITE, komunikat_rect)
    return komunikat_rect


def draw_grid(screen):
    """Rysuje siatkę na płótnie."""
    for x in range(0, canvas_width + 1, 20):  # Linie pionowe siatki
        x_pos = canvas_rect.left + x
        pygame.draw.line(screen, GREY, (x_pos, canvas_rect.bottom), (x_pos, canvas_rect.top), 1)
    for y in range(0, canvas_height + 1, 20):  # Linie poziome siatki
        y_pos = canvas_rect.bottom - y
        pygame.draw.line(screen, GREY, (canvas_rect.left, y_pos), (canvas_rect.right, y_pos), 1)


def draw_axes(screen):
    """Rysuje osie X i Y oraz etykiety co 100 jednostek."""
    # Rysowanie linii osi
    pygame.draw.line(screen, BLACK, canvas_rect.topleft, canvas_rect.bottomleft, 2)  # Oś Y
    pygame.draw.line(screen, BLACK, canvas_rect.bottomleft, canvas_rect.bottomright, 2)  # Oś X

    font = pygame.font.SysFont(None, 24)

    # Rysowanie etykiet na osi X co 100 jednostek
    for x in range(0, canvas_width + 1, 100):
        x_pos = canvas_rect.left + x
        pygame.draw.line(screen, BLACK, (x_pos, canvas_rect.bottom), (x_pos, canvas_rect.top), 1)
        label = font.render(str(x), True, BLACK)
        screen.blit(label, (x_pos - 10, canvas_rect.bottom + 10))

    # Rysowanie etykiet na osi Y co 100 jednostek
    for y in range(100, canvas_height + 1, 100):
        y_pos = canvas_rect.bottom - y
        pygame.draw.line(screen, BLACK, (canvas_rect.left, y_pos), (canvas_rect.right, y_pos), 1)
        label = font.render(str(y), True, BLACK)
        screen.blit(label, (canvas_rect.left - 35, y_pos - 6))


def wyswietl_wspolrzedne_kursora(screen, mouse_x, mouse_y):
    """Wyświetla współrzędne kursora myszy jeśli znajduje się on w obszarze płótna, w przeciwnym przypadku współrzędne znikają"""

    (x, y) = wspol_osiowe((mouse_x, mouse_y), canvas_rect)
    if canvas_rect.collidepoint(mouse_x, mouse_y):
        wyswietl_tekst(f'x:{x}, y:{y}', screen, wspolrzedne_rect, font_size=15, background_color=GREY)
    else:
        pygame.draw.rect(screen, GREY, wspolrzedne_rect)



