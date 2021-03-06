import sys

from static_resources import clock
import pygame


def game_over(screen, background):
    screen.blit(background, (0, 0))
    pygame.display.flip()
    running = True
    while running:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                sys.exit()
