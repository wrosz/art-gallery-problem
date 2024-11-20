# Plik główny, zawierający main()

import pygame
from pliki_zrodlowe.konfiguracja_okna import *
from pliki_zrodlowe.rysowanie_okna import *
from pliki_zrodlowe.funkcje_pomocnicze import *
from pliki_zrodlowe.triangulacja import oblicz_liczbe_straznikow, zapisz_obrazy, min_guards


def main():

    # Inicjalizacja i rysowanie okna
    screen = init_window()
    canvas_rect = draw_canvas_area(screen)
    komunikat_rect = draw_komunikat_area(screen)
    draw_grid(screen)
    draw_axes(screen)

    # Obsługa menu
    ktory_aktywny = None
    ktore_mozliwe = [False, False, False, True]
    menu = wyswietl_menu(screen, ktory_aktywny, ktore_mozliwe)
    rysunki_do_wyswietlenia = ['pliki_wielokat/rysunek_wielokat.png', 'pliki_wielokat/rysunek_triangulacja.png', 'pliki_wielokat/rysunek_straznicy.png']

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

    wyswietl_tekst('Narysuj pierwszy wierzchołek wielokąta, klikając myszą w dowolne miejsce w obszarze płótna.', screen, komunikat_rect)

    liczba_straznikow = None
    wyswietl_liczbe_straznikow(screen, liczba_straznikow)

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:  # wyjście z programu
                running = False

            if event.type == pygame.MOUSEMOTION:  # wyświetlenie współrzędnych kursora myszy na dole ekranu
                mouse_x, mouse_y = event.pos
                if canvas_rect.collidepoint(mouse_x, mouse_y):
                    (x, y) = wspol_osiowe((mouse_x, mouse_y), canvas_rect)
                    wyswietl_tekst(f'x:{x}, y:{y}', screen, wspolrzedne_rect, font_size=15, background_color=GREY)
                else:
                    wyswietl_tekst('', screen, wspolrzedne_rect, background_color=GREY)

            if event.type == pygame.MOUSEBUTTONDOWN:  # obsuga kliknięcia przycisku myszy
                mouse_x, mouse_y = event.pos

                # OBSŁUGA MENU:
                for i in range(3):  # obsługa pierwszych trzech pozycji, wyświetla wielokąt i strażników 
                                    # (0: tylko strażników, 1: triangulację i strażników, 3: obszary, które widzą strażnicy)
                    if menu[i].collidepoint(mouse_x, mouse_y) and ktore_mozliwe[i]:
                        wyswietl_wielokat(screen, rysunki_do_wyswietlenia[i])
                        ktory_aktywny = i
                        ktore_mozliwe = [True for i in range(4)]
                        wyswietl_menu(screen, ktory_aktywny, ktore_mozliwe) 

                if menu[3].collidepoint(mouse_x, mouse_y) and ktore_mozliwe[3]: # rysowanie nowego wielokąta
                        wyczysc_plotno(screen)
                        ktory_aktywny = None
                        ktore_mozliwe = [False, False, False, True]
                        wyswietl_menu(screen, ktory_aktywny, ktore_mozliwe)
                        wyswietl_tekst('Narysuj pierwszy wierzchołek wielokąta, klikając myszą w dowolne miejsce w obszarze płótna.', screen, komunikat_rect)
                        # wyczyszczenie zmiennych potrzebnych do rysowania:
                        draw_enabled = True 
                        co_najmniej_trzy_punkty = False  
                        czy_pierwszy_wierzcholek = True  
                        last_pos = None  
                        current_pos = None 
                        first_pos = None 
                        punkty = []  


                # WPROWADZANIE PRZEZ UŻYTKOWNIKA WIELOKĄTA:
                if draw_enabled:
                    
                    if canvas_rect.collidepoint(mouse_x, mouse_y):  # gdy kliknięto w obszarze płótna,
                                                                    # pobrane współrzędne są wierzchołkiem wielokąta

                        # gdy zamykamy wielokąt, wyłączamy tryb rysowania i zapisujemy plik ze współrzędnymi punktów oraz z rysunkiem wielokąta
                        if circle_collidepoint(first_pos, point_radius, (mouse_x, mouse_y)) and co_najmniej_trzy_punkty:  # sprawdza, czy nie ma samoprzecięć
                            current_pos_osiowe = wspol_osiowe((mouse_x, mouse_y), canvas_rect)
                            if sprawdz_samoprzeciecia(current_pos_osiowe, punkty):  # sprawdza, czy rysowany bok wielokąta nie będzie przecinał figury
                                wyswietl_tekst(['Nie można nanieść punktu, wielokąt będzie zawierał samoprzecięcia.', 'Zaznacz inny punkt.'],
                                               screen, komunikat_rect)
                            else:
                                draw_enabled = False
                                pygame.draw.line(screen, RED, last_pos, first_pos, width=2)
                                zapisz_wspolrzedne(punkty)
                                wyswietl_tekst(['Wielokąt zamknięty.', 'Trwa obliczanie wyników...'], screen, komunikat_rect)
                                pygame.display.flip()
                                zapisz_obrazy()
                                liczba_straznikow = oblicz_liczbe_straznikow()
                                wyswietl_liczbe_straznikow(screen, liczba_straznikow)
                                i = 0  # domyślnie wybiera się opcja 'Wyświetl wielokąt' z menu po prawej stronie
                                wyswietl_wielokat(screen, rysunki_do_wyswietlenia[i])
                                ktory_aktywny = i
                                ktore_mozliwe = [True for i in range(4)]
                                wyswietl_menu(screen, ktory_aktywny, ktore_mozliwe)
                                wyswietl_tekst(['Gotowe!','Aby wyświetlić wyniki, wybierz jedną z opcji po prawej stronie.'], screen, komunikat_rect)

                        else:
                            current_pos_osiowe = wspol_osiowe((mouse_x, mouse_y), canvas_rect)
                            if sprawdz_samoprzeciecia(current_pos_osiowe, punkty):  # sprawdza, czy rysowany bok wielokąta nie będzie przecinał figury
                                wyswietl_tekst(['Nie można nanieść punktu, wielokąt będzie zawierał samoprzecięcia.', 'Zaznacz inny punkt.'],
                                               screen, komunikat_rect)
                            else:  # jeśli nie, to rysujemy nowy bok wielokąta i dodajemy punkt do listy
                                current_pos = (mouse_x, mouse_y)
                                pygame.draw.circle(screen, RED, current_pos, point_radius)
                                punkty.append(current_pos_osiowe)  # dołączamy do listy współrzędne rysowanego punktu, 
                                                                   # zgodnie z pozycją kursora myszy wyświetlaną na ekranie
                                wyswietl_tekst(['Zaznacz kolejne wierzchołki wielokąta.',
                                                    'Następnie zamknij wielokąt, klikając pierwszy narysowany wierzchołek.'], screen, komunikat_rect)
                                if czy_pierwszy_wierzcholek:
                                    first_pos = current_pos
                                    czy_pierwszy_wierzcholek = False
                                else:
                                    pygame.draw.line(screen, RED, last_pos, current_pos, width=2)
                                last_pos = current_pos

                                if (not co_najmniej_trzy_punkty) and len(punkty) >= 3:  # w momencie, gdy rysowany jest trzeci punkt,
                                                                                        # zmieniamy zmienną co_najmniej_trzy_punkty na False
                                    co_najmniej_trzy_punkty = True

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
