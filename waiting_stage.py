import pygame
import static_resources as sr
from network import Network


def waiting(n, screen, clock):
    current_player = n.getP()  # actual player
    screen.fill((255, 255, 255))
    screen.blit(sr.waiting_background, (0, 0))
    pygame.display.flip()
    running = True
    while running:
        clock.tick(60)
        player2 = n.send(current_player)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        if player2.ready:
            running = False
            recruitment(current_player)