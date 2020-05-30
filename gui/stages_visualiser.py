import pygame
import static_resources as sr
from utilities.timer_helper import timer_display
from gui.scoreboard import draw_scoreboard




def recruitment_visualizer(screen, heroes, time, active=None):
    screen.blit(sr.recruitment_background, (0, 0))
    timer_display(time, 350, 400, screen, "recruitment")
    if active is not None:
        active_hero = sr.create_image_with_size("images/heroes_portraits/Active.png", 170, 270)
        screen.blit(active_hero, (150 + active*175, 115, 170, 270))
    for i in range(len(heroes)):
        screen.blit(heroes[i], (160 + i * 175, 120))


def redraw_shop(win, shop, pos, timer, current_player, players):
    win.blit(sr.board, (0, 0))
    shop.draw(win)
    for btn in shop.minion_btns:
        btn.update_hover(pos, win)
    shop.hero.update_hover(pos, win)
    timer_display(timer, 665, 500, win, "shop")
    draw_scoreboard(players, current_player, win)
    pygame.display.flip()
