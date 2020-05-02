import pygame
import static_resources as sr


def is_clicked(pos, hero_nr):
    x1 = pos[0]
    y1 = pos[1]
    return (160 + hero_nr * 175) <= x1 <= (310 + hero_nr * 175) and 120 <= y1 <= 370


def recruitment_visualizer(screen, heroes, time, active=None):
    screen.blit(sr.recruitment_background, (0, 0))
    sr.timer_display(time, 350, 400, screen, "recruitment")
    if active is not None:
        pygame.draw.rect(screen, (255, 0, 0), (155 + active*175, 115, 160, 260))
    for i in range(len(heroes)):
        screen.blit(heroes[i], (160 + i * 175, 120))
    pygame.display.update()