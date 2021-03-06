import pygame
from utilities.json_helper import get_heroes_from_Json
from game_elements.gameElements import PlayerState

clock = pygame.time.Clock()

images_cache = {}


def create_image_with_size(path, x, y):
    if path in images_cache:
        return pygame.transform.scale(images_cache.get(path), (x, y))
    else:
        result = pygame.image.load(path).convert_alpha()
        images_cache[path] = result
        return pygame.transform.scale(result, (x, y))


def check_end_of_game(players, current_player_id):
    for player in players:
        if player.id != current_player_id and player.status != PlayerState.dead:
            return False
    return True


def is_clicked(pos, x, y, width, height):
    x1 = pos[0]
    y1 = pos[1]
    return x <= x1 <= (x + width) and y <= y1 <= (y + height)


heroes = get_heroes_from_Json()


def get_board():
    return create_image_with_size("images/Background.png", 800, 600)


def get_waiting_background():
    return create_image_with_size("images/waiting_background.png", 800, 600)


def get_recruitment_background():
    return create_image_with_size("images/recruitment_backgound.png", 800, 600)


def get_lost():
    return create_image_with_size("images/game_over.JPG", 800, 600)


def get_victory():
    return create_image_with_size("images/victory.png", 800, 600)
