import pygame


# megnézi hogy a játékos talajon van-e
def erintkezes_le(megadott_mezo_lista, megadott_rectangle: pygame.Rect):
    erintkezes_le = False
    for mezo_rect in megadott_mezo_lista:
        mezo_rect_x = range(mezo_rect.centerx - 20, mezo_rect.centerx + 20)
        if megadott_rectangle.bottom == mezo_rect.top:
            if megadott_rectangle.left + 1 in mezo_rect_x or megadott_rectangle.right - 1 in mezo_rect_x:
                erintkezes_le = True
                break
    return erintkezes_le
    
# megnézi hogy van-e fal a játékos mellett vagy felett
def erintkezes_bal(megadott_mezo_lista, megadott_rectangle: pygame.Rect):
    erintkezes_bal = False
    for mezo_rect in megadott_mezo_lista:
        mezo_rect_y = range(mezo_rect.centery - 20, mezo_rect.centery + 20)
        if megadott_rectangle.left == mezo_rect.right:
            if megadott_rectangle.bottom - 1 in mezo_rect_y or megadott_rectangle.top + 1 in mezo_rect_y:
                erintkezes_bal = True
                break
    return erintkezes_bal
    
def erintkezes_jobb(megadott_mezo_lista, megadott_rectangle: pygame.Rect):
    erintkezes_jobb = False
    for mezo_rect in megadott_mezo_lista:
        mezo_rect_y = range(mezo_rect.centery - 20, mezo_rect.centery + 20)
        if megadott_rectangle.right == mezo_rect.left:
            if megadott_rectangle.bottom - 1 in mezo_rect_y or megadott_rectangle.top + 1 in mezo_rect_y:
                erintkezes_jobb = True
                break
    return erintkezes_jobb
    
def erintkezes_fel(megadott_mezo_lista, megadott_rectangle: pygame.Rect):
    erintkezes_fel = False
    for mezo_rect in megadott_mezo_lista:
        mezo_rect_x = range(mezo_rect.centerx - 20, mezo_rect.centerx + 20)
        if megadott_rectangle.top == mezo_rect.bottom:
            if megadott_rectangle.left + 1 in mezo_rect_x or megadott_rectangle.right - 1 in mezo_rect_x:
                erintkezes_fel = True
                break
    return erintkezes_fel