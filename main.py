import pygame
from gameElements import Minion, Player, Hero
from gameElements import Tribe
from gameElements import State
from gameElements import Stats
from gui import MinionButton
from gui import ShopVisualiser
from network import Network

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("AutoChess")
board = pygame.image.load("tmp_board.jpg")


def redraw_window(win, shop): # need separate func for shop and combat
    win.fill((255, 255, 255))
    win.blit(board, (0, 0))
    shop.draw(win)
    # player.draw(win)
    #pygame.display.update()


# hero = Hero("test", None)
# minion = Minion("first", Tribe.orc, [], State.in_play, Stats(4, 4, 1))
# minion1 = Minion("first", Tribe.orc, [], State.in_play, Stats(4, 4, 1))
# minion2 = Minion("first", Tribe.orc, [], State.in_play, Stats(4, 4, 1))
# minion3 = Minion("first", Tribe.orc, [], State.in_play, Stats(4, 4, 1))
#
# hminion1 = Minion("first", Tribe.orc, [], State.in_hand, Stats(4, 4, 1))
# hminion2 = Minion("first", Tribe.orc, [], State.in_hand, Stats(4, 4, 1))
# hminion3 = Minion("first", Tribe.orc, [], State.in_hand, Stats(4, 4, 1))

#p.get_hero().add_minion(minion)
#p.get_hero().add_minion(minion1)
#p.get_hero().add_minion(minion2)
#p.get_hero().add_minion(minion3)
#p.get_hero().add_minion_in_hand(hminion1)
#p.get_hero().add_minion_in_hand(hminion2)
#p.get_hero().add_minion_in_hand(hminion3)

running = True
n = Network()
p = n.getP() # actual player
print(p)
clock = pygame.time.Clock()
shop = ShopVisualiser(p)
redraw_window(screen, shop)

while running:
    clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            for btn in shop.get_buttons():
                pos = pygame.mouse.get_pos()
                if btn.onclick(pos, shop):
                    redraw_window(screen, shop)
    # redraw_window(screen, p)
