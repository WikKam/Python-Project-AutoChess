import pygame
import static_resources as sr
from network import Network
from recruitment_stage import recruitment


def waiting(n, screen, clock):
    players, current_player = n.getP() # actual player
    screen.blit(sr.waiting_background, (0, 0))
    pygame.display.flip()
    # players, opponent = n.send(players[current_player])
    running = True
    while running:
        clock.tick(60)
        players, opponent = n.send(players[current_player])
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        if players[opponent].ready:
            running = False
            recruitment(players, current_player, n, clock, screen)