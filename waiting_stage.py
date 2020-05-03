import pygame
from recruitment_stage import recruitment
from static_resources import waiting_background
from static_resources import clock


def waiting(current_player, network, screen):
    screen.blit(waiting_background, (0, 0))
    pygame.display.flip()
    running = True
    while running:
        clock.tick(60)
        players, opponent = network.send(current_player)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        if players[opponent].ready:
            running = False
            recruitment(current_player, network, screen)
