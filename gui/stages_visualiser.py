import pygame
import static_resources as sr
from utilities.timer_helper import timer_display


def recruitment_visualizer(screen, heroes, time, active=None):
    screen.blit(sr.recruitment_background, (0, 0))
    timer_display(time, 350, 400, screen, "recruitment")
    if active is not None:
        pygame.draw.rect(screen, (255, 0, 0), (155 + active*175, 115, 160, 260))
    for i in range(len(heroes)):
        screen.blit(heroes[i], (160 + i * 175, 120))


def redraw_shop(win, shop, pos, timer):
    win.blit(sr.board, (0, 0))
    shop.draw(win)
    for btn in shop.minion_btns:
        btn.update_hover(pos, win)
    timer_display(timer, 665, 500, win, "shop")
    pygame.display.flip()
