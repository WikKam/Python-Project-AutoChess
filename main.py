import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("AutoChess")

playersNumber = 0;


class Player():
    def __init__(self, x, y, width, height, color): ## do usunięcia, chce wiedzieć czy dobrze łacze sie z serverem XD
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.val = 3

    def draw(self, win): # represent character on to stream
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.val

        if keys[pygame.K_RIGHT]:
            self.x += self.val

        if keys[pygame.K_UP]:
            self.y -= self.val

        if keys[pygame.K_DOWN]:
            self.y += self.val

        self.rect = (self.x, self.y, self.width, self.height)


def redraw_window(win, player):
    win.fill((255, 255, 255))
    player.draw(win)
    pygame.display.update()


p = Player(50, 50, 100, 100, (0, 255, 0))
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    p.move()
    redraw_window(screen, p)


