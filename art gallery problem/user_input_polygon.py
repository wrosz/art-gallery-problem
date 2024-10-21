import pygame
import sys
import csv

# -------------- FUNKCJE POMOCNICZE --------------

def circle_collidepoint(center, radius, point):
    '''Sprawdza, czy punkt o współrzędnych point należy do koła o środku w punkcie center i promieniu radius'''
    if center is None:
        return False
    elif (center[0] - point[0]) ** 2 + (center[1] - point[1]) ** 2 <= radius ** 2:
        return True
    else:
        return False


def zapisz_wspolrzedne(punkty):
    '''Zapisuje współrzędne punktów do pliku CSV'''
    with open('wspolrzedne_punktow.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['X', 'Y'])  # Nagłówki kolumn
        for punkt in punkty:
            writer.writerow(punkt)  # Zapisuje każdy punkt


# -------------- ZMIENNE --------------

# ustawienia okna
window_width, window_height = 800, 600
canvas_width, canvas_height = 600, window_height - 10
canvas_rect = pygame.Rect(5, 5, canvas_width, canvas_height)

# kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
RED = (255, 0, 0)

point_radius = 5  # promień okręgu oznaczającego wierzchołek wielokąta


# -------------- RYSOWANIE OKNA --------------

pygame.init()
screen = pygame.display.set_mode((window_width, window_height))

screen.fill(GREY)
pygame.draw.rect(screen, WHITE, canvas_rect)


# -------------- RYSOWANIE I GŁÓWNA PĘTLA PROGRAMU --------------

draw_enabled = True  # czy możemy rysować, czy zmieniamy na False gdy zamknęliśmy wielokąt
co_najmniej_trzy_punkty = False  # czy narysowaliśmy co najmniej 3 punkty
czy_pierwszy_wierzcholek = True  # czy rysujemy aktualnie pierwszy wierzchołek, czy kolejne

last_pos = None  # współrzędne ostatniego narysowanego punktu
current_pos = None  # współrzędne aktualnego punktu
first_pos = None  # współrzędne pierwszego wierzchołka

punkty = []  # lista do przechowywania punktów

while True:
    for event in pygame.event.get():

        # zamknięcie programu
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # kliknięcie myszą
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if draw_enabled:
                if canvas_rect.collidepoint(mouse_x, mouse_y):  # czy kliknięto obszar płótna

                    current_pos = (mouse_x, mouse_y)

                    # gdy zamykamy wielokąt, kończymy rysowanie i zapisujemy plik ze współrzędnymi
                    if circle_collidepoint(first_pos, point_radius, current_pos):
                        if co_najmniej_trzy_punkty:
                            draw_enabled = False
                            pygame.draw.line(screen, BLACK, last_pos, first_pos)
                            zapisz_wspolrzedne(punkty)
                        continue

                    pygame.draw.circle(screen, center=current_pos, radius=point_radius, color=BLACK)  # rysowanie punktu na płótnie
                    punkty.append(current_pos)  # dodajemy punkt do listy
                    if czy_pierwszy_wierzcholek:
                        first_pos = current_pos
                        czy_pierwszy_wierzcholek = False
                    else:
                        pygame.draw.line(screen, BLACK, last_pos, current_pos)
                    last_pos = current_pos

                    if not co_najmniej_trzy_punkty:
                        if len(punkty) == 3:
                            co_najmniej_trzy_punkty = True
 

    pygame.display.update()
