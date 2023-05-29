import pygame
from sys import exit
from erintkezesek import *
from Palya import Palya

pygame.init()

# pálya osztály
palyak: list[Palya] = []
palya_szama: int = 1
for e in range(3):
    fajl_neve: str = 'pályák/palya' + str(palya_szama) + '.txt'
    with open(fajl_neve, 'r', encoding='utf-8') as fajl:
        palyak.append(Palya(fajl.readlines()))
    palya_szama += 1

# ablak beállításai
ablak = pygame.display.set_mode((1200, 600))
pygame.display.set_caption('platformer játék')
pygame.display.set_icon(pygame.image.load('képek/icon.png'))

# óra
clock = pygame.time.Clock()

# egér
eger = pygame.mouse.get_pos()

# menü
start_gomb = pygame.image.load('képek/start-gomb.png').convert()
start_gomb_rect = start_gomb.get_rect(midbottom=(600, 250))
reset_gomb = pygame.image.load('képek/reset-gomb.png').convert()
reset_gomb_rect = start_gomb.get_rect(midbottom=(600, 300))
menu_felirat_font = pygame.font.Font(None, 100)
menu_felirat_font2 = pygame.font.Font('Pixeltype.ttf', 125)
menu_felirat_font3 = pygame.font.Font('Pixeltype.ttf', 125)
menu_felirat = menu_felirat_font2.render('Platformer Jatek', False, 'Yellow')
menu_felirat_arnyek = menu_felirat_font3.render('Platformer Jatek', False, 'Black')
menu = True
karakterek_gomb = pygame.image.load('képek/karakter-valasztas-gomb.png').convert()
karakterek_gomb_rect = karakterek_gomb.get_rect(midbottom=(600, 350))
vissza_gomb = pygame.image.load('képek/vissza-gomb.png').convert()
mentes_gomb = pygame.image.load('képek/mentes-gomb.png').convert()
karakter_valasztas_felirat = menu_felirat_font.render('Válassz karaktert!', False, 'White')


# mezők
teszt_mezo1 = pygame.image.load('képek/teszt-mezo1.png').convert()
teszt_mezo2 = pygame.image.load('képek/teszt-mezo2.png').convert()
mezok: list[pygame.Rect] = []  # amelyik rectangelek ebben a listában vannak azokon nem tud átmenni a játékos

# mozgó mező
# mozgo_mezo1 = pygame.image.load('képek/teszt-mezo1.png').convert()
# mozgo_mezo1_rect = mozgo_mezo1.get_rect(midbottom=(-1000, 280))
# mozgo_mezo_frame = 0
# mozgo_mezo_iranya = -2
# mozgo_mezok: list[pygame.Rect] = []

# sebződés
sebzo_mezo1 = pygame.image.load('képek/sebzo-mezo2.png').convert()
sebzo_mezok: list[pygame.Rect] = []
halhatatlan_frame = 0

# halál
halal = False
halal_felirat = menu_felirat_font.render('Meghaltál!', False, 'Red')
ujra_gomb = pygame.image.load('képek/ujra-gomb.png').convert()
ujra_gomb_rect = start_gomb.get_rect(midbottom=(600, 250))

# kamera
kamera_mozgas = 0
kamera_mozgas_frame_bal = 0
kamera_mozgas_frame_jobb = 0

# hátterek
hatter1 = pygame.image.load('képek/hatter2.png').convert()
hatter2 = pygame.image.load('képek/hatter1.png').convert()

# elmentett adatok lekérése


def mentett_adatok_lekerese(sor):
    mentes: str = ''
    with open('mentes.txt', 'r', encoding='utf-8') as file:
        mentes = file.read().splitlines()[sor]
    file.close()
    return mentes


# lekért adatokból változók
melyik_palyan_van = int(mentett_adatok_lekerese(1))
melyik_skin = mentett_adatok_lekerese(3)

# pálya vége
palya_vege = pygame.image.load('képek/teszt-mezo3.png').convert_alpha()
palya_vege_rect = palya_vege.get_rect(midbottom=(-5000, -5000))
palya_vege_kepernyo = False
palya_teljesitve_felirat = menu_felirat_font.render(str(melyik_palyan_van) + '. pálya teljesítve!', False, 'Yellow')
kovetkezo_palya_gomb = pygame.image.load('képek/kovetkezo-palya-gomb.png').convert()
kovetkezo_palya_gomb_rect = kovetkezo_palya_gomb.get_rect(midbottom=(600, 250))

# játékos
jatekos_x_koordinata = palyak[melyik_palyan_van - 1].kezdo_pont_x
jatekos_y_koordinata = palyak[melyik_palyan_van - 1].kezdo_pont_y
eredeti_gravitacio: int = 5
gravitacio: int = eredeti_gravitacio
ugras_frame = 0
jatekos = pygame.image.load(melyik_skin).convert_alpha()
jatekos_rect = jatekos.get_rect(midbottom=(jatekos_x_koordinata, jatekos_y_koordinata))

# életerő
eletero_pont = pygame.image.load('képek/hp.png').convert()
eletero_pont_rect = eletero_pont.get_rect(midbottom=(150, 40))
eletero_szama = 5
eletero_kiiras_seged = 0

# adatok kiírásához kellenek
palya_szama_font = pygame.font.Font(None, 50)
palya_szama_kiiras = palya_szama_font.render(str(melyik_palyan_van) + '. pálya', False, 'White')
kiiras_hatter = pygame.image.load('képek/kiiras-hatter1.png').convert()
kiiras_hatter_rect = kiiras_hatter.get_rect(midbottom=(0, 45))

# idő számolása
szamlalo_masodperc = 0
szamlalo_perc = 0
pygame.time.set_timer(pygame.USEREVENT, 1000)
szamlalo_font = pygame.font.SysFont('Consolas', 30)
szamlalo_kiiras = szamlalo_font.render(str(szamlalo_perc) + ':' + str(szamlalo_masodperc), False, 'White')
ossz_masodperc = 0
ossz_perc = 0


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
        elif mezo == '3':
            palya_vege_rect.topleft = (mezo_x_koordinata, mezo_y_koordinata)
            ablak.blit(palya_vege, (mezo_x_koordinata, mezo_y_koordinata))
        elif mezo == '4':
            sebzo_mezok.append(pygame.draw.rect(ablak, (0, 0, 0), (mezo_x_koordinata, mezo_y_koordinata, 40, 40)))
            ablak.blit(sebzo_mezo1, (mezo_x_koordinata, mezo_y_koordinata))

        mezo_x_koordinata += 40


# karakter kiválasztására
def karakterek_menu():
    pygame.init()

    kepernyo_hossza = 1200
    keprernyo_magassaga = 600
    screen = pygame.display.set_mode((kepernyo_hossza, keprernyo_magassaga))
    pygame.display.set_caption("Platformer játék")

    BLACK = (0, 0, 0)
    választott_skin = ["képek/skin1.png", "képek/skin2.png"]
    karakter_index = 0

    character_images = []
    for skin in választott_skin:
        character_images.append(pygame.image.load(skin))

    gomb_x = kepernyo_hossza - 120
    gomb_y = keprernyo_magassaga - 70

    vissza_gomb_rect = vissza_gomb.get_rect(midbottom=(gomb_x, gomb_y))
    mentes_gomb_rect = mentes_gomb.get_rect(midbottom=(gomb_x - 200, gomb_y))

    karakter_valasztas = True

    while karakter_valasztas:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    karakter_index = (karakter_index - 1) % len(választott_skin)
                elif event.key == pygame.K_RIGHT:
                    karakter_index = (karakter_index + 1) % len(választott_skin)

            if event.type == pygame.MOUSEBUTTONDOWN:
                eger = pygame.mouse.get_pos()

                if vissza_gomb_rect.collidepoint(eger):
                    karakter_valasztas = False
                    break
                

                if mentes_gomb_rect.collidepoint(eger):
                    save_selected_skin(választott_skin[karakter_index])

        screen.fill(BLACK)

        selected_skin_image = character_images[karakter_index]
        screen.blit(selected_skin_image, (kepernyo_hossza // 2 - selected_skin_image.get_width() // 2, keprernyo_magassaga // 2 - selected_skin_image.get_height() // 2))

        screen.blit(vissza_gomb, vissza_gomb_rect)
        screen.blit(mentes_gomb, mentes_gomb_rect)
        ablak.blit(karakter_valasztas_felirat, (325, 100))

        pygame.display.flip()

def save_selected_skin(kivalaszotott_karakter):
    with open('mentes.txt', 'r+', encoding='utf-8') as file:
            sorok = file.readlines()
            sorok[3] = ''
            sorok.insert(3, kivalaszotott_karakter + '\n')
            file.seek(0)
            file.writelines(sorok)
    file.close()


# játék
while True:
    # menü
    while menu:
        for event in pygame.event.get():

            # játék bezárása (menüben)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            eger = pygame.mouse.get_pos()

            # start gomb
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_gomb_rect.collidepoint(eger):
                    szamlalo_masodperc = 0
                    szamlalo_perc = 0
                    menu = False
                    break

            # reset gomb
            if event.type == pygame.MOUSEBUTTONDOWN:
                if reset_gomb_rect.collidepoint(eger):
                    with open('eredeti-mentes.txt', 'r', encoding='utf-8') as uj_fajl:
                        with open('mentes.txt', 'w', encoding='utf-8') as regi_fajl:
                            regi_fajl.write(uj_fajl.read())
                    melyik_palyan_van = 1
                    kamera_mozgas = 0
                    palya_vege_rect = palya_vege.get_rect(midbottom=(-5000, -5000))
                    jatekos_x_koordinata = palyak[melyik_palyan_van - 1].kezdo_pont_x
                    jatekos_y_koordinata = palyak[melyik_palyan_van - 1].kezdo_pont_y
                    jatekos_rect = jatekos.get_rect(midbottom=(jatekos_x_koordinata, jatekos_y_koordinata))
                    palya_szama_kiiras = palya_szama_font.render(str(melyik_palyan_van) + '. pálya', False, 'White')
                    break

            # karakterválasztás
            if event.type == pygame.MOUSEBUTTONDOWN:
                if karakterek_gomb_rect.collidepoint(eger):
                    karakterek_menu()
        
        ablak.blit(hatter1, (0, 0))
        ablak.blit(start_gomb, start_gomb_rect)
        ablak.blit(reset_gomb, reset_gomb_rect)
        ablak.blit(menu_felirat_arnyek, (300, 100))
        ablak.blit(menu_felirat, (298, 98))
        ablak.blit(karakterek_gomb, karakterek_gomb_rect)

        pygame.display.update()

        clock.tick(60)
    # menü vége

    for event in pygame.event.get():

        # számláló
        if event.type == pygame.USEREVENT:
            szamlalo_masodperc += 1
            szamlalo_kiiras = szamlalo_font.render(str(szamlalo_perc) + ':' + str(szamlalo_masodperc), False, 'White')
        if szamlalo_masodperc == 60:
            szamlalo_masodperc = 0
            szamlalo_perc += 1

        # játék bezárása
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # ugrás
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if erintkezes_lefele(mezok, jatekos_rect):
                    gravitacio -= 15
                    ugras_frame += 15

    # kiüríti a mezők listát hogy ne laggoljon a játék
    mezok = []
    sebzo_mezok = []

    # háttér megjelenítése
    ablak.blit(hatter1, (0, 0))

    # képernyőre kiírt infók
    ablak.blit(kiiras_hatter, kiiras_hatter_rect)
    ablak.blit(palya_szama_kiiras, (0, 0))
    eletero_kiiras_seged = 0
    for e in range(eletero_szama):
        eletero_pont_rect = eletero_pont.get_rect(midbottom=(150 + eletero_kiiras_seged, 40))
        ablak.blit(eletero_pont, eletero_pont_rect)
        eletero_kiiras_seged += 39
    ablak.blit(szamlalo_kiiras, (1116, 0))

    # átvált a következő pályára
    if erintkezes_barhogy(jatekos_rect, palya_vege_rect):
        palya_vege_kepernyo = True
        # kírja, hogy teljesítetted a pályát
        while palya_vege_kepernyo:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                egér = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if kovetkezo_palya_gomb_rect.collidepoint(eger):
                        palya_vege_kepernyo = False
                        break

            palya_teljesitve_felirat = menu_felirat_font.render(str(melyik_palyan_van) + '. pálya teljesítve!', False, 'Yellow')
            ablak.blit(hatter2, (0, 0))
            ablak.blit(palya_teljesitve_felirat, (325, 100))
            ablak.blit(kovetkezo_palya_gomb, kovetkezo_palya_gomb_rect)
            szamlalo_kiiras = szamlalo_font.render('idő: ' + str(szamlalo_perc) + ':' + str(szamlalo_masodperc), False, 'White')
            ablak.blit(szamlalo_kiiras, (325, 350))

            pygame.display.update()

            clock.tick(60)
        kamera_mozgas = 0
        szamlalo_masodperc = 0
        szamlalo_perc = 0
        szamlalo_kiiras = szamlalo_font.render(str(szamlalo_perc) + ':' + str(szamlalo_masodperc), False, 'White')
        melyik_palyan_van += 1
        jatekos_x_koordinata = palyak[melyik_palyan_van - 1].kezdo_pont_x
        jatekos_y_koordinata = palyak[melyik_palyan_van - 1].kezdo_pont_y
        with open('mentes.txt', 'r+', encoding='utf-8') as file:
            sorok = file.readlines()
            uj_palya_szama = int(sorok[1]) + 1
            sorok[1] = ''
            sorok.insert(1, str(uj_palya_szama) + '\n')
            file.seek(0)
            file.writelines(sorok)
        file.close()
        jatekos_rect = jatekos.get_rect(midbottom=(jatekos_x_koordinata, jatekos_y_koordinata))
        palya_szama_kiiras = palya_szama_font.render(str(melyik_palyan_van) + '. pálya', False, 'White')

    # mezők megjelenítése
    mezok_megjelenitese(palyak[melyik_palyan_van - 1].txt_fajl)

    # sebződés
    if halhatatlan_frame == 0:
        if erintkezes_sebzovel(jatekos_rect, sebzo_mezok):
            eletero_szama -= 1
            if eletero_szama > 0:
                halhatatlan_frame += 60
    # halál
    if eletero_szama == 0 or jatekos_rect.centery > 700:
        halal = True
        while halal:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                eger = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ujra_gomb_rect.collidepoint(eger):
                        kamera_mozgas = 0
                        jatekos_x_koordinata = palyak[melyik_palyan_van - 1].kezdo_pont_x
                        jatekos_y_koordinata = palyak[melyik_palyan_van - 1].kezdo_pont_y
                        jatekos_rect = jatekos.get_rect(midbottom=(jatekos_x_koordinata, jatekos_y_koordinata))
                        eletero_szama = 5
                        #szamlalo_masodperc = 0
                        #szamlalo_perc = 0
                        halal = False
                        break

            ablak.blit(hatter2, (0, 0))
            ablak.blit(halal_felirat, (425, 100))
            ablak.blit(ujra_gomb, ujra_gomb_rect)

            pygame.display.update()

            clock.tick(60)

    # mozgó mező
    # if mozgo_mezo_frame < 200:
    #     mozgo_mezo1_rect.centerx += mozgo_mezo_iranya
    #     mozgo_mezo_frame += 1
    # if mozgo_mezo_frame == 200:
    #     mozgo_mezo_frame = 0
    #     mozgo_mezo_iranya *= -1

    # mezok.append(mozgo_mezo1_rect)
    # mozgo_mezok.append(mozgo_mezo1_rect)
    # ablak.blit(mozgo_mezo1, (mozgo_mezo1_rect))

    # if erintkezes_lefele(mozgo_mezok, jatekos_rect):
    #     jatekos_rect.centerx += mozgo_mezo_iranya
    # if mozgo_mezo_iranya > 0 and erintkezes_balra(mozgo_mezok, jatekos_rect):
    #     jatekos_rect.centerx += mozgo_mezo_iranya
    # if mozgo_mezo_iranya < 0 and erintkezes_jobbra(mozgo_mezok, jatekos_rect):
    #     jatekos_rect.centerx += mozgo_mezo_iranya

    # mozgás jobbra és balra
    billentyu = pygame.key.get_pressed()

    if billentyu[pygame.K_d]:
        for e in range(8):
            if erintkezes_jobbra(mezok, jatekos_rect) == False:
                jatekos_rect.centerx += 1
                jatekos_x_koordinata += 1
    if billentyu[pygame.K_a]:
        for e in range(8):
            if erintkezes_balra(mezok, jatekos_rect) == False:
                jatekos_rect.centerx -= 1
                jatekos_x_koordinata -= 1

    # gravitáció
    if erintkezes_felfele(mezok, jatekos_rect):
        ugras_frame = 0
        gravitacio = eredeti_gravitacio
    if ugras_frame > 0:
        ugras_frame -= 1
        gravitacio += 1
    if erintkezes_lefele(mezok, jatekos_rect):
        gravitacio -= eredeti_gravitacio
    if gravitacio > 0:
        for e in range(gravitacio):
            jatekos_rect.centery += 1
            if erintkezes_lefele(mezok, jatekos_rect):
                break
    if gravitacio < 0:
        for e in range(-gravitacio):
            if erintkezes_felfele(mezok, jatekos_rect):
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

    # ha a játékos nagyon messze lenne a kamerától
    if jatekos_x_koordinata < 1400:
        kamera_mozgas_frame_bal = 1
    if kamera_mozgas_frame_bal > 0:
        jatekos_rect.centerx += 400
        kamera_mozgas += 400
        jatekos_x_koordinata += 400
        #mozgo_mezo1_rect.centerx += 400
        kamera_mozgas_frame_bal -= 1

    if jatekos_x_koordinata > -200:
        kamera_mozgas_frame_jobb = 1
    if kamera_mozgas_frame_jobb > 0:
        jatekos_rect.centerx -= 400
        kamera_mozgas -= 400
        jatekos_x_koordinata -= 400
        #mozgo_mezo1_rect.centerx -= 400
        kamera_mozgas_frame_jobb -= 1

    # kamera mozgatása balra és jobbra
    if jatekos_x_koordinata < 200:  # milyen távol van a játékos az ablak keretétől amikor a kamera el kezdd mozogni
        kamera_mozgas_frame_bal = 10  # milyen sebességgel és mennyit mozogjon a kamera
    if kamera_mozgas_frame_bal > 0:
        jatekos_rect.centerx += 8
        kamera_mozgas += 8
        jatekos_x_koordinata += 8
        #mozgo_mezo1_rect.centerx += 8
        kamera_mozgas_frame_bal -= 8

    if jatekos_x_koordinata > 1000:
        kamera_mozgas_frame_jobb = 10
    if kamera_mozgas_frame_jobb > 0:
        jatekos_rect.centerx -= 8
        kamera_mozgas -= 8
        jatekos_x_koordinata -= 8
        #mozgo_mezo1_rect.centerx -= 8
        kamera_mozgas_frame_jobb -= 8

    # játékos megjelenítése
    if halhatatlan_frame % 6 != 0 or halhatatlan_frame == 0:
        ablak.blit(jatekos, (jatekos_rect))

    # sebződés utáni halhatatlanság
    if halhatatlan_frame > 0:
        halhatatlan_frame -= 1

    pygame.display.update()

    # maximum fps
    clock.tick(60)
