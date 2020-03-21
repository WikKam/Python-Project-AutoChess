import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("AutoChess")
running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
