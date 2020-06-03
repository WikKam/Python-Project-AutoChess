import pygame
from static_resources import create_image_with_size

recruitment_time = 5
shop_time = 20
combat_time = 15


def timer_display(time, x, y, win, content):
    if time <= 0:
        if content == "shop":
            win.blit(create_image_with_size("images/black_beam.JPG", 140, 80), (x - 10, y - 10))
            win.blit(get_digit(digits[0]), (x + 30, y))
        else:
            win.blit(create_image_with_size("images/beam_texture.jpg", 140, 80), (x - 10, y - 10))
            win.blit(get_digit(digits[0]), (x + 30, y))
    if time >= 10:
        if content == "shop":
            win.blit(create_image_with_size("images/black_beam.JPG", 140, 80), (x - 10, y - 10))
            win.blit(get_digit(digits[time // 10]), (x, y))
            win.blit(get_digit(digits[time % 10]), (x + 50, y))
        else:
            win.blit(create_image_with_size("images/beam_texture.jpg", 140, 80), (x - 10, y - 10))
            win.blit(get_digit(digits[time // 10]), (x, y))
            win.blit(get_digit(digits[time % 10]), (x + 50, y))
    else:
        if content == "shop":
            win.blit(create_image_with_size("images/black_beam.JPG", 140, 80), (x - 10, y - 10))
            win.blit(get_digit(digits[time]), (x + 30, y))
        else:
            win.blit(create_image_with_size("images/beam_texture.jpg", 140, 80), (x - 10, y - 10))
            win.blit(get_digit(digits[time]), (x + 30, y))


# DIGITS
digits = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine"
}


def get_digit(name):
    return create_image_with_size('images/Digits/{}.png'.format(name), 50, 70)
