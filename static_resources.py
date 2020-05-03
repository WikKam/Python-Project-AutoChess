import pygame
from utilities.json_helper import get_heroes_from_Json

clock = pygame.time.Clock()


def create_image_with_size(path, x, y):
    result = pygame.image.load(path)
    return pygame.transform.scale(result, (x, y))


board = create_image_with_size("images/tmp_board.jpg", 800, 600)
waiting_background = create_image_with_size("images/waiting_background.png", 800, 600)
recruitment_background = create_image_with_size("images/recruitment_backgound.png", 800, 600)
heroes = get_heroes_from_Json()
