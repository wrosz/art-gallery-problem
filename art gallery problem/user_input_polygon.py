import pygame
import sys
import csv
from typing import List, Tuple, Union



# -------------- FUNKCJE POMOCNICZE --------------

def circle_collidepoint(center: Tuple[int, int], radius: float, point: Tuple[int, int]) -> bool:
    '''Sprawdza, czy punkt o współrzędnych point należy do koła o środku w punkcie center i promieniu radius'''
    if center is None:
        return False
    elif (center[0] - point[0]) ** 2 + (center[1] - point[1]) ** 2 <= radius ** 2:
        return True
    else:
        return False


def zapisz_wspolrzedne(punkty: List[Tuple[int, int]]) -> None:
    '''Zapisuje współrzędne punktów do pliku wspolrzedne_punktow.csv'''
    with open('wspolrzedne_punktow.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['X', 'Y'])  # Nagłówki kolumn
        for punkt in punkty:
            writer.writerow(punkt)  # Zapisuje każdy punkt


def wyswietl_komunikat(teksty: Union[str, List[str]], screen, komunikat_font_size=20, color=pygame.Color('black')):
    '''
    Wyświetla komunikat na ekranie. Każdy element listy teksty będzie wyświetlany w nowej linijce.
    
    Parametry:
    - teksty: lista tekstów (każdy element to nowa linijka)
    - screen: obiekt ekranu Pygame
    - komunikat_rect: prostokąt, w którym ma zostać wyświetlony komunikat
    - komunikat_font_size: rozmiar czcionki (domyślnie 24)
    - color: kolor tekstu (domyślnie czarny)
    '''
    if isinstance(teksty, str):
        teksty = [teksty]  # Konwersja na listę, jeśli podany jest pojedynczy string

    font = pygame.font.Font(None, komunikat_font_size)
    
    # Czyszczenie prostokąta (rysowanie białego tła)
    pygame.draw.rect(screen, WHITE, komunikat_rect)
    
    # Obliczenie całkowitej wysokości tekstu
    total_height = len(teksty) * font.get_height()
    
    # Wyśrodkowanie tekstu pionowo w prostokącie
    y_offset = komunikat_rect.top + (komunikat_rect.height - total_height) // 2
    
    # Renderowanie każdej linijki tekstu
    for tekst in teksty:
        text_surface = font.render(tekst, True, color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = komunikat_rect.centerx  # Wyśrodkowanie w poziomie
        text_rect.top = y_offset  # Ustawienie pionowo na odpowiedniej wysokości
        screen.blit(text_surface, text_rect)
        
        # Przesunięcie w dół o wysokość tekstu
        y_offset += font.get_height()



# -------------- ZMIENNE --------------

# wymiary elementów okna 
canvas_width, canvas_height = 700, 500  # wymiary płótna
komunikat_width, komunikat_height = canvas_width, 40  # wymiary komunikatów wyświetlanych na górze okna
odstep_gora, odstep_boki, odstep_dol = 10, 10, 40  # odstępy elementów od: górnej, bocznych i dolnej krawędzi okna
window_width = canvas_width + 2 * odstep_boki  # szerokość okna
window_height = canvas_height + komunikat_height + 2 * odstep_gora + odstep_dol  # wysokość okna

# współrzędne elementów
canvas_rect = pygame.Rect(odstep_boki, komunikat_height + 2 * odstep_gora, canvas_width, canvas_height)
komunikat_rect = pygame.Rect(odstep_gora, odstep_boki, komunikat_width, komunikat_height)

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
pygame.draw.rect(screen, WHITE, canvas_rect)  # rysowanie płótna
pygame.draw.rect(screen, WHITE, komunikat_rect)  # rysowanie prostokąta do wyświetlania komunikatów



# -------------- WPROWADZANIE WIELOKĄTA I GŁÓWNA PĘTLA PROGRAMU --------------

draw_enabled = True  # czy możemy rysować, czy zmieniamy na False gdy zamknęliśmy wielokąt
co_najmniej_trzy_punkty = False  # czy narysowaliśmy co najmniej 3 punkty
czy_pierwszy_wierzcholek = True  # czy rysujemy aktualnie pierwszy wierzchołek, czy kolejne

last_pos = None  # współrzędne ostatniego narysowanego punktu
current_pos = None  # współrzędne aktualnego punktu
first_pos = None  # współrzędne pierwszego wierzchołka

punkty = []  # lista do przechowywania punktów

wyswietl_komunikat('Narysuj pierwszy punkt wielokąta, klikając myszą w dowolne miejsce w obszarze płótna.', screen)

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
                if canvas_rect.collidepoint(mouse_x, mouse_y):  # gdy kliknięto obszar płótna

                    current_pos = (mouse_x, mouse_y)

                    # gdy zamykamy wielokąt, kończymy rysowanie i zapisujemy plik ze współrzędnymi
                    if circle_collidepoint(first_pos, point_radius, current_pos):
                        if co_najmniej_trzy_punkty:
                            draw_enabled = False
                            pygame.draw.line(screen, BLACK, last_pos, first_pos)
                            zapisz_wspolrzedne(punkty)
                            wyswietl_komunikat(['Wielokąt zamknięty!','Aby wyjść z programu, zamknij okno.'], screen)
                        continue

                    pygame.draw.circle(screen, center=current_pos, radius=point_radius, color=BLACK)  # rysowanie punktu na płótnie
                    punkty.append(current_pos)  # dodajemy punkt do listy
                    if czy_pierwszy_wierzcholek:
                        first_pos = current_pos
                        czy_pierwszy_wierzcholek = False
                        wyswietl_komunikat(['Zaznacz kolejne wierzchołki wielokąta.', 'Następnie zamknij wielokąt, ponownie klikając pierwszy narysowany wierzchołek.'], screen)
                    else:
                        pygame.draw.line(screen, BLACK, last_pos, current_pos)
                    last_pos = current_pos

                    if not co_najmniej_trzy_punkty:
                        if len(punkty) == 3:
                            co_najmniej_trzy_punkty = True
 

    pygame.display.update()
