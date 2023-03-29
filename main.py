import pygame
from sys import exit
from erintkezesek import erintkezes_bal, erintkezes_jobb, erintkezes_fel, erintkezes_le

pygame.init()

# ablak beállításai
ablak = pygame.display.set_mode((1200, 600))
pygame.display.set_caption('platformer játék')
pygame.display.set_icon(pygame.image.load('képek/icon.png'))

# óra
clock = pygame.time.Clock()

# egér
egér = pygame.mouse.get_pos()

# menü
start_gomb = pygame.image.load('képek/start-gomb.png').convert()
start_gomb_rect = start_gomb.get_rect(midbottom=(600, 150))
menu = True

# mezők
teszt_mezo1 = pygame.image.load('képek/teszt-mezo1.png').convert()
teszt_mezo2 = pygame.image.load('képek/teszt-mezo2.png').convert()
mezok: list[pygame.Rect] = []  # amelyik rectangelek ebben a listában vannak azokon nem tud átmenni a játékos

# mozgó mező
mozgo_mezo1 = pygame.image.load('képek/teszt-mezo1.png').convert()
mozgo_mezo1_rect = mozgo_mezo1.get_rect(midbottom=(-1000, 280))
mozgo_mezo_frame = 0
mozgo_mezo_iranya = -2

mozgo_mezok: list[pygame.Rect] = []

# játékos
jatekos_x_koordinata = 600
jatekos_y_koordinata = 160
eredeti_gravitacio: int = 5
gravitacio: int = eredeti_gravitacio
ugras_frame = 0
jatekos = pygame.image.load('képek/jatekos.png').convert_alpha()
jatekos_rect = jatekos.get_rect(midbottom=(jatekos_x_koordinata, jatekos_y_koordinata))

# kamera
kamera_mozgas = 0
kamera_mozgas_frame_bal = 0
kamera_mozgas_frame_jobb = 0

# hátterek
hatter1 = pygame.image.load('képek/hatter1.png').convert()

# pálya beolvasása
with open('pályák/teszt-palya1.txt', 'r') as file:
    teszt_palya_1 = ''
    for szam in file.read():
        if szam != '\n':
            teszt_palya_1 += szam


def mezok_megjelenitese(palya):
    # (egy mező 40×40 pixel, összesen 100×14 mező van egy pályában)
    mezo_x_koordinata = -2000 + kamera_mozgas
    mezo_y_koordinata = 0
    hany_mezo = 0
    for mezo in palya:
        hany_mezo += 1

        # sorokat elválasztja
        if hany_mezo % 100 == 1:
            mezo_y_koordinata += 40
            mezo_x_koordinata = -2000 + kamera_mozgas

        # megjeleníti a mezőket, létrehoz rectangeleket mezőkhöz
        if mezo == '1':
            mezok.append(pygame.draw.rect(ablak, (0, 0, 0), (mezo_x_koordinata, mezo_y_koordinata, 40, 40)))
            ablak.blit(teszt_mezo1, (mezo_x_koordinata, mezo_y_koordinata))
        elif mezo == '2':
            mezok.append(pygame.draw.rect(ablak, (0, 0, 0), (mezo_x_koordinata, mezo_y_koordinata, 40, 40)))
            ablak.blit(teszt_mezo2, (mezo_x_koordinata, mezo_y_koordinata))

        mezo_x_koordinata += 40


# játék
while True:
    # menü
    while menu:
        for event in pygame.event.get():

            # játék bezárása (menüben)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            egér = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_gomb_rect.collidepoint(egér):
                    menu = False
                    break

        ablak.blit(start_gomb, start_gomb_rect)

        pygame.display.update()

        clock.tick(60)

    for event in pygame.event.get():

        # játék bezárása
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # ugrás
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if erintkezes_le(mezok, jatekos_rect):
                    gravitacio -= 15
                    ugras_frame += 15

    # kiüríti a mezők listát hogy ne laggoljon a játék
    mezok = []

    # háttér megjelenítése
    ablak.blit(hatter1, (0, 0))

    # mezők megjelenítése
    mezok_megjelenitese(teszt_palya_1)

    # mozgó mező
    if mozgo_mezo_frame < 200:
        mozgo_mezo1_rect.centerx += mozgo_mezo_iranya
        mozgo_mezo_frame += 1
    if mozgo_mezo_frame == 200:
        mozgo_mezo_frame = 0
        mozgo_mezo_iranya *= -1

    mezok.append(mozgo_mezo1_rect)
    mozgo_mezok.append(mozgo_mezo1_rect)
    ablak.blit(mozgo_mezo1, (mozgo_mezo1_rect))

    if erintkezes_le(mozgo_mezok, jatekos_rect):
        jatekos_rect.centerx += mozgo_mezo_iranya
    if mozgo_mezo_iranya > 0 and erintkezes_bal(mozgo_mezok, jatekos_rect):
        jatekos_rect.centerx += mozgo_mezo_iranya
    if mozgo_mezo_iranya < 0 and erintkezes_jobb(mozgo_mezok, jatekos_rect):
        jatekos_rect.centerx += mozgo_mezo_iranya

    # mozgás jobbra és balra
    billentyu = pygame.key.get_pressed()

    if billentyu[pygame.K_d]:
        for e in range(8):
            if erintkezes_jobb(mezok, jatekos_rect) == False:
                jatekos_rect.centerx += 1
                jatekos_x_koordinata += 1
    if billentyu[pygame.K_a]:
        for e in range(8):
            if erintkezes_bal(mezok, jatekos_rect) == False:
                jatekos_rect.centerx -= 1
                jatekos_x_koordinata -= 1

    # gravitáció
    if erintkezes_fel(mezok, jatekos_rect):
        ugras_frame = 0
        gravitacio = eredeti_gravitacio
    if ugras_frame > 0:
        ugras_frame -= 1
        gravitacio += 1
    if erintkezes_le(mezok, jatekos_rect):
        gravitacio -= eredeti_gravitacio
    if gravitacio > 0:
        for e in range(gravitacio):
            jatekos_rect.centery += 1
            if erintkezes_le(mezok, jatekos_rect):
                break
    if gravitacio < 0:
        for e in range(-gravitacio):
            if erintkezes_fel(mezok, jatekos_rect):
                ugras_frame = 0
                gravitacio = eredeti_gravitacio
                break
            jatekos_rect.centery -= 1
    if ugras_frame == 0:
        gravitacio = eredeti_gravitacio

    # ha a játékos valahogy belekerülne egy mező belsejébe
    for mezo_rect in mezok:
        if jatekos_rect.center == mezo_rect.center:
            jatekos_rect.centery -= 40

    # kamera mozgatása balra és jobbra
    if jatekos_x_koordinata < 200:  # milyen távol van a játékos az ablak keretétől amikor a kamera el kezdd mozogni
        kamera_mozgas_frame_bal = 10  # milyen sebességgel és mennyit mozogjon a kamera
    if kamera_mozgas_frame_bal > 0:
        jatekos_rect.centerx += 8
        kamera_mozgas += 8
        jatekos_x_koordinata += 8
        mozgo_mezo1_rect.centerx += 8
        kamera_mozgas_frame_bal -= 8

    if jatekos_x_koordinata > 1000:
        kamera_mozgas_frame_jobb = 10
    if kamera_mozgas_frame_jobb > 0:
        jatekos_rect.centerx -= 8
        kamera_mozgas -= 8
        jatekos_x_koordinata -= 8
        mozgo_mezo1_rect.centerx -= 8
        kamera_mozgas_frame_jobb -= 8

    # játékos megjelenítése
    ablak.blit(jatekos, (jatekos_rect))

    pygame.display.update()

    # maximum fps
    clock.tick(60)
