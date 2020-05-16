from static_resources import game_over, clock
import pygame


def game_over_lost(screen):
    screen.blit(game_over, (0, 0))
    pygame.display.flip()
    running = True
    while running:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False