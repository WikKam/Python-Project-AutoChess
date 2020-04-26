from gameElements import *
import pygame
import time
import json


recruitment_time = 4
shop_time = 5


def create_image_with_size(path, x, y):
    result = pygame.image.load(path)
    return pygame.transform.scale(result, (x, y))


def timer_display(time, x, y, win, content):
        if time <= 0:
            if content == "shop":
                win.blit(create_image_with_size("images/black_beam.JPG", 140, 80), (x - 10, y - 10))
                win.blit(digits[0].convert_alpha(), (x, y))
            else:
                win.blit(create_image_with_size("images/beam_texture.jpg", 140, 80), (x-10, y-10))
                win.blit(recruitment_digits[0].convert_alpha(), (x, y))
        if time >= 10:
            if content == "shop":
                win.blit(create_image_with_size("images/black_beam.JPG", 140, 80), (x - 10, y - 10))
                win.blit(digits[time // 10].convert_alpha(), (x, y))
                win.blit(digits[time % 10].convert_alpha(), (x + 50, y))
            else:
                win.blit(create_image_with_size("images/beam_texture.jpg", 140, 80), (x-10, y-10))
                win.blit(recruitment_digits[time // 10].convert_alpha(), (x, y))
                win.blit(recruitment_digits[time % 10].convert_alpha(), (x + 50, y))
        else:
            if content == "shop":
                win.blit(create_image_with_size("images/black_beam.JPG", 140, 80), (x - 10, y - 10))
                win.blit(digits[time].convert_alpha(), (x, y))
            else:
                win.blit(create_image_with_size("images/beam_texture.jpg", 140, 80), (x-10, y-10))
                win.blit(recruitment_digits[time].convert_alpha(), (x, y))
        pygame.display.update()


def redraw_shop(win, shop): # need separate func for shop and combat
    win.blit(board, (0, 0))
    shop.draw(win)
    pygame.display.flip()
    # player.draw(win)
    #pygame.display.update()


def get_heroes_from_Json():
    res = []
    with open('heroes.json') as json_file:
        data = json.load(json_file)
        for hero in data['heroes']:
            h = Hero(hero["name"], hero["power"], hero["image"])
            res.append(h)
    return res


# DIGITS
digits = {
    0: create_image_with_size("Digits/zero.PNG", 50, 70),
    1: create_image_with_size("Digits/one.png", 50, 70),
    2: create_image_with_size("Digits/two.png", 50, 70),
    3: create_image_with_size("Digits/three.png", 50, 70),
    4: create_image_with_size("Digits/four.png", 50, 70),
    5: create_image_with_size("Digits/five.png", 50, 70),
    6: create_image_with_size("Digits/six.png", 50, 70),
    7: create_image_with_size("Digits/seven.png", 50, 70),
    8: create_image_with_size("Digits/eight.png", 50, 70),
    9: create_image_with_size("Digits/nine.PNG", 50, 70)
}

recruitment_digits = {
    0: create_image_with_size("Digits/zero_red.png", 50, 70),
    1: create_image_with_size("Digits/one_red.png", 50, 70),
    2: create_image_with_size("Digits/two_red.png", 50, 70),
    3: create_image_with_size("Digits/three_red.png", 50, 70),
    4: create_image_with_size("Digits/four_red.png", 50, 70),
    5: create_image_with_size("Digits/five_red.png", 50, 70),
    6: create_image_with_size("Digits/six_red.png", 50, 70),
    7: create_image_with_size("Digits/seven_red.png", 50, 70),
    8: create_image_with_size("Digits/eight_red.png", 50, 70),
    9: create_image_with_size("Digits/nine_red.png", 50, 70)
}


board = create_image_with_size("images/tmp_board.jpg", 800, 600)
waiting_background = create_image_with_size("images/waiting_background.png", 800, 600)
recruitment_background = create_image_with_size("images/recruitment_backgound.png", 800, 600)
heroes = get_heroes_from_Json()
