import pygame


# megnézi, hogy a játékos talajon van-e
def erintkezes_lefele(megadott_mezo_lista, megadott_rectangle: pygame.Rect):
    erintkezes_le = False
    for mezo_rect in megadott_mezo_lista:
        mezo_rect_x = range(mezo_rect.centerx - 20, mezo_rect.centerx + 20)
        if megadott_rectangle.bottom == mezo_rect.top:
            if megadott_rectangle.left + 1 in mezo_rect_x or megadott_rectangle.right - 1 in mezo_rect_x:
                erintkezes_le = True
                break
    return erintkezes_le

# megnézi, hogy van-e fal a játékos mellett vagy felett
def erintkezes_balra(megadott_mezo_lista, megadott_rectangle: pygame.Rect):
    erintkezes_bal = False
    for mezo_rect in megadott_mezo_lista:
        mezo_rect_y = range(mezo_rect.centery - 20, mezo_rect.centery + 20)
        if megadott_rectangle.left == mezo_rect.right:
            if megadott_rectangle.bottom - 1 in mezo_rect_y or megadott_rectangle.top + 1 in mezo_rect_y:
                erintkezes_bal = True
                break
    return erintkezes_bal


def erintkezes_jobbra(megadott_mezo_lista, megadott_rectangle: pygame.Rect):
    erintkezes_jobb = False
    for mezo_rect in megadott_mezo_lista:
        mezo_rect_y = range(mezo_rect.centery - 20, mezo_rect.centery + 20)
        if megadott_rectangle.right == mezo_rect.left:
            if megadott_rectangle.bottom - 1 in mezo_rect_y or megadott_rectangle.top + 1 in mezo_rect_y:
                erintkezes_jobb = True
                break
    return erintkezes_jobb


def erintkezes_felfele(megadott_mezo_lista, megadott_rectangle: pygame.Rect):
    erintkezes_fel = False
    for mezo_rect in megadott_mezo_lista:
        mezo_rect_x = range(mezo_rect.centerx - 20, mezo_rect.centerx + 20)
        if megadott_rectangle.top == mezo_rect.bottom:
            if megadott_rectangle.left + 1 in mezo_rect_x or megadott_rectangle.right - 1 in mezo_rect_x:
                erintkezes_fel = True
                break
    return erintkezes_fel

def erintkezes_barhogy(megadott_rect1: pygame.Rect, megadott_rect2: pygame.Rect):
    erintkezes_barhogy = False
    megadott_rect2_x = range(megadott_rect2.centerx - 20, megadott_rect2.centerx + 20)
    megadott_rect2_y = range(megadott_rect2.centery - 20, megadott_rect2.centery + 20)
    if megadott_rect1.left in megadott_rect2_x or megadott_rect1.right in megadott_rect2_x:
        if megadott_rect1.bottom in megadott_rect2_y or megadott_rect1.top in megadott_rect2_y:
            erintkezes_barhogy = True
    return erintkezes_barhogy