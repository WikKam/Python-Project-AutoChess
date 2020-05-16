import json
from game_elements.gameElements import *


def get_effect_from_Json(effects):
    return [StatBuffEffect(effect["health"],
                           effect["attack"],
                           TriggerOn(effect["trigger_when"]),
                           TargetKind(effect["kind"]),
                           Tribe(effect["target_tribe"])) for effect in effects if effect["type"] == "StatBuff"]


def get_minions_from_Json():
    ret = []
    with open('json/minions.json') as json_file:
        data = json.load(json_file)
        for minion in data['minions']:
            m = Minion(minion["name"], Tribe(minion["tribe"]), get_effect_from_Json(minion["effects"]),
                       State(minion["state"]),
                       Stats(minion["stats"]["health"], minion["stats"]["attack"], minion["stats"]["tier"]),
                       minion["icon_path"], minion["card_path"])
            ret.append(m)
    return ret


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

