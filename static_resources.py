from gameElements import *
import pygame
import time


def create_image_with_size(path, x, y):
    result = pygame.image.load(path)
    return pygame.transform.scale(result, (x, y))


def timer_display(time, x, y, win, content):
        if time >= 10:
            if content == "shop":
                win.blit(digits[time // 10].convert_alpha(), (x, y))
                win.blit(digits[time % 10].convert_alpha(), (x + 50, y))
            else:
                win.blit(recruitment_digits[time // 10].convert_alpha(), (x, y))
                win.blit(recruitment_digits[time % 10].convert_alpha(), (x + 50, y))
        else:
            if content == "shop":
                win.blit(digits[time].convert_alpha(), (x, y))
            else:
                win.blit(recruitment_digits[time].convert_alpha(), (x, y))
        pygame.display.update()



minions = [Minion("Axe", Tribe.orc, [], None, Stats(4, 4, 1), "minions_icons/Axe.png"),
           Minion("Mars", Tribe.orc, [], None, Stats(4, 4, 1), "minions_icons/Mars.png"),
           Minion("Enigma", Tribe.orc, [], None, Stats(4, 4, 1), "minions_icons/Enigma.png"),
           Minion("Medusa", Tribe.orc, [], None, Stats(4, 4, 1), "minions_icons/Medusa.png"),
           Minion("Sven", Tribe.orc, [], None, Stats(4, 4, 1), "minions_icons/Sven.png"),
           Minion("Slardar", Tribe.orc, [], None, Stats(4, 4, 1), "minions_icons/Slardar.png"),
           Minion("Zeus", Tribe.orc, [], None, Stats(4, 4, 1), "minions_icons/Zeus.png"),
           Minion("Tinker", Tribe.orc, [], None, Stats(4, 4, 1), "minions_icons/Tinker.png"),
           Minion("Tusk", Tribe.orc, [], None, Stats(4, 4, 1), "minions_icons/Tusk.png"),
           Minion("Windranger", Tribe.orc, [], None, Stats(4, 4, 1), "minions_icons/Windranger.png"),
           Minion("Clockwerk", Tribe.orc, [], None, Stats(4, 4, 1), "minions_icons/Clockwerk.png"),
           Minion("Templar_Assassin", Tribe.orc, [], None, Stats(4, 4, 1), "minions_icons/Templar_Assassin.png")]

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


board = create_image_with_size("tmp_board.jpg", 800, 600)
waiting_background = create_image_with_size("waiting_background.png", 800, 600)
recruitment_background = create_image_with_size("recruitment_backgound.png", 800, 600)