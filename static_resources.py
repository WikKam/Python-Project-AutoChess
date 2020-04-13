from gameElements import *
import pygame
import time


def create_image_with_size(path, x, y):
    result = pygame.image.load(path)
    return pygame.transform.scale(result, (x, y))


def timer_display(timer, x, y, win):
        time_1 = None
        time_2 = None
        while timer > 0:
            if timer > 0:
                time_1 = None
                time_1 = win.blit(digits[timer // 10].convert_alpha(), (x, y))
                time_2 = win.blit(digits[timer % 10].convert_alpha(), (x + 50, y))
            else:
                win.blit(digits[timer].convert_alpha(), (x, y))
            pygame.display.update()
            time.sleep(1)
            timer -= 1


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


board = create_image_with_size("tmp_board.jpg", 800, 600)
waiting_background = create_image_with_size("waiting_background.png", 800, 600)
recruitment_background = create_image_with_size("recruitment_backgound.png", 800, 600)