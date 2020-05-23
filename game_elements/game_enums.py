import enum


class HeroPowerKind(enum.Enum):
    passive = 1
    active = 2


class Tribe(enum.Enum):
    human = 1
    orc = 2
    dwarf = 3
    elf = 4
    none = 5
    all = 6


class TargetKind(enum.Enum):
    random = 1
    targeted = 2
    self = 3
    all = 4
    minion_that_changed_state = 5


class State(enum.Enum):
    in_shop = 1
    in_hand = 2
    in_play = 3
    in_storage = 4
    on_battlefield = 5
    dead = 6


class PlayerState(enum.Enum):
    not_connected = 1
    connected = 2
    in_shop = 3
    in_combat = 4
    after_combat = 5
    dead = 10


class AttackTurn(enum.IntEnum):
    attack_first = 1
    attack_second = -1


class TriggerOn(enum.Enum):
    on_enter_play = 1
    on_enter_hand = 2
    on_death = 3
    whenever_minion_played = 4
    on_end_of_turn = 5
    on_hero_power_pressed = 6
    whenever_minion_bought = 7
    whenever_minion_sold = 8
    on_enter_shop = 9