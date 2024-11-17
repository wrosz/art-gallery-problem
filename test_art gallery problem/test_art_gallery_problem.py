# Plik główny, zawierający main()

import pygame
import pandas as pd
from rysowanie_okna import *
from test_funkcje_pomocnicze import *


def main():

    # Inicjalizacja i rysowanie okna
    screen = init_window()
    canvas_rect = draw_canvas_area(screen)
    komunikat_rect = draw_komunikat_area(screen)
    draw_grid(screen)
    draw_axes(screen)

    # Główna pętla programu
    running = True

    # zmienne potrzebne do wprowadzania wielokąta:
    draw_enabled = True  # True, gdy tryb rysowania jest włączony
    co_najmniej_trzy_punkty = False  # True, jeśli użytkownik już wprowadził co najmniej trzy wierzchołki (co pozwala zamknąc wielokąt)
    czy_pierwszy_wierzcholek = True  # True, jeśli użytkownik nie narysował jeszcze żadnego wierzchołka
    last_pos = None  # współrzędne poprzednio narysowanego wierzchołka
    current_pos = None  # współrzędne aktualnie rysowanego wierzchołka
    first_pos = None  # współrzędne pierwszego narysowanego wierzchołka
    punkty = []  # lista przechowująca współrzędne wierzchołków wielokąta
    point_radius=5  # promień koła oznaczającego wierzchołek wprowadzanego wielokąta

    wyswietl_tekst('Narysuj pierwszy wierzchołek wielokąta, klikając myszą w dowolne miejsce w obszarze płótna.', screen, komunikat_rect)

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:  # wyjście z programu
                running = False

            if event.type == pygame.MOUSEMOTION:  # wyświetlenie współrzędnych kursora myszy na dole ekranu
                mouse_x, mouse_y = event.pos
                wyswietl_tekst(f'x:{mouse_x}, y:{mouse_y}', screen, wspolrzedne_rect, font_size=15, background_color=GREY)

            # WPROWADZANIE PRZEZ UŻYTKOWNIKA WIELOKĄTA
            if draw_enabled:

                if event.type == pygame.MOUSEBUTTONDOWN:  # obsługa klikania przycisku myszy
                    mouse_x, mouse_y = event.pos # pobranie współrzędnych w miejscu, gdzie kliknął użytkownik
                    
                    if canvas_rect.collidepoint(mouse_x, mouse_y):  # gdy kliknięto w obszarze płótna,
                                                                    # pobrane współrzędne są wierzchołkiem wielokąta

                        # gdy zamykamy wielokąt, wyłączamy tryb rysowania i zapisujemy plik ze współrzędnymi punktów
                        if circle_collidepoint(first_pos, point_radius, (mouse_x, mouse_y)) and co_najmniej_trzy_punkty:
                            draw_enabled = False
                            pygame.draw.line(screen, RED, last_pos, first_pos, width=2)
                            zapisz_wspolrzedne(punkty)
                            wyswietl_tekst(['Wielokąt zamknięty!', 'Aby wyjść z programu, zamknij okno.'], screen, komunikat_rect)

                        else:
                            current_pos_osiowe = wspol_osiowe((mouse_x, mouse_y), canvas_rect)
                            if sprawdz_samoprzeciecia(current_pos_osiowe, punkty):  # sprawdza, czy rysowany bok wielokąta nie będzie przecinał figury
                                wyswietl_tekst(["Nie można nanieść punktu, wielokąt będzie zawierał samoprzecięcia.", "Zaznacz inny punkt."], screen, komunikat_rect)
                            else:  # jeśli nie, to rysujemy nowy bok wielokąta i dodajemy punkt do listy
                                current_pos = (mouse_x, mouse_y)
                                pygame.draw.circle(screen, RED, current_pos, point_radius)
                                punkty.append(current_pos_osiowe)  # dołączamy do listy współrzędne rysowanego punktu, zgodnie z pozycją kursora myszy wyświetlaną na ekranie
                                if czy_pierwszy_wierzcholek:
                                    first_pos = current_pos
                                    czy_pierwszy_wierzcholek = False
                                    wyswietl_tekst(['Zaznacz kolejne wierzchołki wielokąta.',
                                                    'Następnie zamknij wielokąt, klikając pierwszy narysowany wierzchołek.'], screen, komunikat_rect)
                                else:
                                    pygame.draw.line(screen, RED, last_pos, current_pos, width=2)
                                last_pos = current_pos

                                if (not co_najmniej_trzy_punkty) and len(punkty) >= 3:  # w momencie, gdy rysowany jest trzeci punkt,
                                                                                        # zmieniamy zmienną co_najmniej_trzy_punkty na False
                                    co_najmniej_trzy_punkty = True
            

        pygame.display.flip()

    pygame.quit()

class TestPunkty:
    def test_liczba_punktów(self):
        assert len(pd.read_csv(r'test_art gallery problem/wspolrzedne_punktow.csv')) > 2

if __name__ == "__main__":
    main()
