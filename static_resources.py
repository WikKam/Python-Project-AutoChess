from game_elements.gameElements import *
import pygame
import time
import json
from server_communication.network import Network

recruitment_time = 5
shop_time = 20
combat_time = 15
clock = pygame.time.Clock()


network = Network()
current_player = network.get_player()


def get_effect_from_Json(effects):
    return [StatBuffEffect(effect["health"],
                           effect["attack"],
                           TriggerOn(effect["trigger_when"]),
                           TargetKind(effect["kind"]),
                           effect["target_tribe"]) for effect in effects if effect["type"] == "StatBuff"]


def get_minions_from_Json():
    ret = []
    with open('json/minions.json') as json_file:
        data = json.load(json_file)
        for minion in data['minions']:
            m = Minion(minion["name"], Tribe(minion["tribe"]), get_effect_from_Json(minion["effects"]),
                       State(minion["state"]),
                       Stats(minion["stats"]["health"], minion["stats"]["attack"], minion["stats"]["tier"]),
                       minion["icon_path"])
            ret.append(m)
    return ret


def create_image_with_size(path, x, y):
    result = pygame.image.load(path)
    return pygame.transform.scale(result, (x, y))


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


def redraw_shop(win, shop):  # need separate func for shop and combat
    win.blit(board, (0, 0))
    shop.draw(win)
    pygame.display.flip()
    # player.draw(win)
    # pygame.display.update()


def get_hero_power_from_json(power):
    if power is None:
        return None
    passive = HeroStats()
    hp = HeroPower(HeroPowerKind(power["kind"]), get_effect_from_Json(power["active"]), passive, power["cost"])
    for attr in power["passive"]:
        setattr(passive, attr, power["passive"][attr])
    return hp


def get_heroes_from_Json():
    res = []
    with open('json/heroes.json') as json_file:
        data = json.load(json_file)
        for hero in data['heroes']:
            h = Hero(hero["name"], get_hero_power_from_json(hero["power"]), hero["image"])
            res.append(h)
    return res


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

board = create_image_with_size("images/tmp_board.jpg", 800, 600)
waiting_background = create_image_with_size("images/waiting_background.png", 800, 600)
recruitment_background = create_image_with_size("images/recruitment_backgound.png", 800, 600)
heroes = get_heroes_from_Json()
