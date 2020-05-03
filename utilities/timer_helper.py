import pygame
from static_resources import create_image_with_size

recruitment_time = 5
shop_time = 20
combat_time = 15


def timer_display(time, x, y, win, content):
    if time <= 0:
        if content == "shop":
            win.blit(create_image_with_size("images/black_beam.JPG", 140, 80), (x - 10, y - 10))
            win.blit(digits[0].convert_alpha(), (x + 30, y))
        else:
            win.blit(create_image_with_size("images/beam_texture.jpg", 140, 80), (x - 10, y - 10))
            win.blit(recruitment_digits[0].convert_alpha(), (x + 30, y))
    if time >= 10:
        if content == "shop":
            win.blit(create_image_with_size("images/black_beam.JPG", 140, 80), (x - 10, y - 10))
            win.blit(digits[time // 10].convert_alpha(), (x, y))
            win.blit(digits[time % 10].convert_alpha(), (x + 50, y))
        else:
            win.blit(create_image_with_size("images/beam_texture.jpg", 140, 80), (x - 10, y - 10))
            win.blit(recruitment_digits[time // 10].convert_alpha(), (x, y))
            win.blit(recruitment_digits[time % 10].convert_alpha(), (x + 50, y))
    else:
        if content == "shop":
            win.blit(create_image_with_size("images/black_beam.JPG", 140, 80), (x - 10, y - 10))
            win.blit(digits[time].convert_alpha(), (x + 30, y))
        else:
            win.blit(create_image_with_size("images/beam_texture.jpg", 140, 80), (x - 10, y - 10))
            win.blit(recruitment_digits[time].convert_alpha(), (x + 30, y))
    pygame.display.update()


# DIGITS
digits = {
    0: create_image_with_size("images/Digits/zero.PNG", 50, 70),
    1: create_image_with_size("images/Digits/one.png", 50, 70),
    2: create_image_with_size("images/Digits/two.png", 50, 70),
    3: create_image_with_size("images/Digits/three.png", 50, 70),
    4: create_image_with_size("images/Digits/four.png", 50, 70),
    5: create_image_with_size("images/Digits/five.png", 50, 70),
    6: create_image_with_size("images/Digits/six.png", 50, 70),
    7: create_image_with_size("images/Digits/seven.png", 50, 70),
    8: create_image_with_size("images/Digits/eight.png", 50, 70),
    9: create_image_with_size("images/Digits/nine.PNG", 50, 70)
}

recruitment_digits = {
    0: create_image_with_size("images/Digits/zero_red.png", 50, 70),
    1: create_image_with_size("images/Digits/one_red.png", 50, 70),
    2: create_image_with_size("images/Digits/two_red.png", 50, 70),
    3: create_image_with_size("images/Digits/three_red.png", 50, 70),
    4: create_image_with_size("images/Digits/four_red.png", 50, 70),
    5: create_image_with_size("images/Digits/five_red.png", 50, 70),
    6: create_image_with_size("images/Digits/six_red.png", 50, 70),
    7: create_image_with_size("images/Digits/seven_red.png", 50, 70),
    8: create_image_with_size("images/Digits/eight_red.png", 50, 70),
    9: create_image_with_size("images/Digits/nine_red.png", 50, 70)
}