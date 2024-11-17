# Plik zawiera dodatkowe funkcje pomocnicze wywoływane w innych miejscach kodu, w szczególności:
# - circle_collidepoint
# - zapisz_wspolrzedne
# - wyswietl_tekst
# - wspol_osiowe
# - sprawdz_samoprzeciecia (oraz dodatkowe funkcje onSegment, orientation i doIntersect wywoływane w ciele funkcji sprawdz_samoprzeciecia)

import pygame
import csv
from typing import List, Tuple, Union



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


def wyswietl_tekst(teksty: Union[str, List[str]], screen, tekst_rect, font_size=20, color=pygame.Color('black'), background_color=pygame.Color('white')):
    '''
    Wyświetla komunikat na ekranie. Każdy element listy teksty będzie wyświetlany w nowej linijce.
    
    Parametry:
    - teksty: lista tekstów (każdy element to nowa linijka)
    - screen: obiekt ekranu Pygame
    - komunikat_rect: obiekt prostokąta w Pygame, na którym wyświetlamy komunikat
        (domyślnie na górze okna, w miejscu do wyświetlania komunikatów/instrukcji dla użytkownika)
    - komunikat_font_size: rozmiar czcionki (domyślnie 20)
    - color: kolor tekstu (domyślnie czarny)
    - background_color: kolor tła (domyślnie biały)
    '''

    if isinstance(teksty, str):
        teksty = [teksty]  # Konwersja na listę, jeśli podany jest pojedynczy string

    font = pygame.font.Font(None, font_size)
    pygame.draw.rect(screen, background_color, tekst_rect)  # Czyszczenie prostokąta (rysowanie tła)
    total_height = len(teksty) * font.get_height()  # Obliczenie całkowitej wysokości tekstu
    y_offset = tekst_rect.top + (tekst_rect.height - total_height) // 2  # Wyśrodkowanie tekstu pionowo w prostokącie
    
    # Renderowanie każdej linijki tekstu
    for tekst in teksty:
        text_surface = font.render(tekst, True, color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = tekst_rect.centerx  # Wyśrodkowanie w poziomie
        text_rect.top = y_offset  # Ustawienie pionowo na odpowiedniej wysokości
        screen.blit(text_surface, text_rect)
        y_offset += font.get_height()  # Przesunięcie w dół o wysokość tekstu


def wspol_osiowe(punkt:Tuple[int, int], canvas_rect:pygame.Rect):
    """Zamienia współrzędne pobrane z pygame na takie, by były zgodne z narysowanymi osiami
    (punkt (0.0) w lewym dolnym rogu płótna, wzrost wartości y w kierunku górnym)"""
    x = punkt[0]
    y = punkt[1]
    return (x - canvas_rect.left, - y + canvas_rect.bottom)



# --------- SPRAWDZANIE SAMOPRZECIĘĆ WIELOKĄTA ---------

# funkcje pomocnicze:

def onSegment(p, q, r): 
    """Zakładamy, że punkty p, q, r są współliniowe. Funkcja zwraca True, jeśli punkt q leży na odcinku pr"""
    if ( (q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and 
            (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))): 
        return True
    return False
  
def orientation(p, q, r): 
    """Funkcja zwraca orientację trójkąta pqr. Zwracane wartości:
    0 - punkty współliniowe
    1 - orientacja dodatnia (przeciwna do ruchu wskazówek zegara)
    2 - orientacja ujemna (zgodna z ruchem wskazówek zegara)
    """
    val =  (float(q[0] - p[0]) * (r[1] - q[1])) - (float(q[1] - p[1]) * (r[0] - q[0]))
    if (val > 0): # dodatnia
        return 1
    elif (val < 0): # ujemna
        return 2
    else: # punkty współliniowe
        return 0
  
def doIntersect(p1,q1,p2,q2):
    """Sprawdza czy odcinki p1q1 i p2q2 się przecinają, korzystając z funkcji orientation i onSegment"""
    # Sprawdzamy orientacje trójkątów potrzebnych do rozpatrzenia różnych przypadków
    o1 = orientation(p1, q1, p2) 
    o2 = orientation(p1, q1, q2) 
    o3 = orientation(p2, q2, p1) 
    o4 = orientation(p2, q2, q1) 

    if ((o1 != o2) and (o3 != o4)): # przypadek ogólny (odcinki nie są równoległe i się przecinają)
        return True
  
    # specjalne przypadki  
    if ((o1 == 0) and onSegment(p1, p2, q1)):  # p1, q1 i p2 są współliniowe, p2 leży na p1q1
        return True
    if ((o2 == 0) and onSegment(p1, q2, q1)):  # p1, q1 i q1 są wspóliniowe, q2 leży na p1q1
        return True
    if ((o3 == 0) and onSegment(p2, p1, q2)):  # p2, q2 i p1 są współliniowe, p1 leży na p2q2
        return True
    if ((o4 == 0) and onSegment(p2, q1, q2)):  # p2, q2 i q1 są współliniowe, q1 leży na p2q2
        return True
  
    # żaden z powyższych przypadków nie zachodzi
    return False


def sprawdz_samoprzeciecia(p1, punkty:List[int]):  # https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
    """Główna funkcja. Zwraca True, jeśli punkt odcinek łączący punkt p1 z ostatnim elementem listy punkty
    przecina któryś z segmentów ścieżki łączącej poprzednie punkty z tej listy."""
    # jeśli odcinek łączący punkt (x,y) i ostatni punkt z listy punkty przecina jakikolwiek poprzedni odcinek (poza ostatnim), zwracamy False.
    # W przeciwnym wypadku zwracamy True
    for i in range(0, len(punkty)-2):
        q1 = punkty[-1]
        p2 = punkty[i]
        q2 = punkty[i+1]
        if doIntersect(p1, q1, p2, q2):
            return True
    return False



