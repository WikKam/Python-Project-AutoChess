import enum
import copy


class Tribe(enum.Enum):
    human = 1
    orc = 2
    dwarf = 3
    elf = 4
    none = 5


class State(enum.Enum):
    in_shop = 1
    in_hand = 2
    in_play = 3
    in_storage = 4
    dead = 5


class TriggerOn(enum.Enum):
    on_enter_play = 1
    on_enter_hand = 2
    on_death = 3
    whenever_minion_played = 4


class Condition:
    def check_condition(self, target):
        pass


class TribeCondition(Condition):
    def __init__(self, tribe):
        self.tribe = tribe

    def check_condition(self, target):
        return self.tribe == target.tribe


class Effect:
    def __init__(self, condition, trigger_when):
        self.condition = condition
        self.triggerWhen = trigger_when

    def trigger_effect(self, caster, targets):
        pass


class StatBuffEffect(Effect):
    def __init__(self, health, attack, condition, triggered_when):
        super().__init__(condition, triggered_when)
        self.health = health
        self.attack = attack

    def trigger_effect(self, caster, targets):
        for t in targets:
            t.stats.update_attack(self.attack)
            t.stats.update_health(self.health)


class EffectManager:
    def check_effect(self, prev, current, source):
        pass

    def activate_effects(self, source):
        pass

    def __init__(self, turn_manager):
        self.turn_manager = turn_manager


class SummonEffect(Effect):
    def __init__(self, minion, condition, triggered_when):
        super().__init__(condition, triggered_when)
        self.minion = minion

    def trigger_effect(self, caster, targets):
        if targets is None:
            return
        for _ in targets:
            _ = self.minion


class Stats:
    def __init__(self, health, attack, tier):
        self.health = health
        self.attack = attack
        self.tier = tier

    def update_health(self, change):
        self.health += change

    def update_attack(self, attack):
        self.attack += attack

    def update_stats_after_attack(self, other):
        self.update_health(-other.health)
        self.update_attack(-other.attack)


class Minion:
    def __init__(self, name, tribe, effects, state, stats):
        self.tribe = tribe
        self.effects = effects
        self.state = state
        self.stats = stats
        self.combat_stats = copy.deepcopy(stats)
        self.isDead = False
        self.name = name

    def attack(self, target):
        self.stats.update_stats_after_attack(target.combat_stats)
        target.stats.update_stats_after_attack(self.combat_stats)
        if self.combat_stats.health <= 0:
            self.isDead = True
            self.check_effects(State.in_play, State.dead, self)
        if target.combat_stats.health <= 0:
            target.isDead = True
            target.check_effects(State.in_play, State.dead, self)

    def set_position(self, position):
        self.position = position

    def on_new_turn(self):
        self.combat_stats = copy.deepcopy(self.stats)

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def check_effects(self, prev, curr, target):
        pass


def find_first_free_index(lt):
    ret = -1
    for i, item in enumerate(lt):
        if item is None:
            ret = i
            break
    print(ret)
    return ret


class Hero:
    max_minion_no = 7
    max_hand_no = 6
    start_hp = 30
    max_tier = 6
    starting_tier = 1
    max_gold = 10
    current_max_gold = 3

    def __init__(self, name, hero_power):
        self.name = name
        self.hero_power = hero_power
        self.current_tier = 1
        self.current_hp = Hero.start_hp
        self.is_dead = False
        self.minions = [None, None, None, None, None, None, None]
        self.hand = [None, None, None, None, None]
        self.current_gold = 3

    def upgrade_tier(self):
        if self.current_tier < Hero.max_tier: self.current_tier += 1

    def update_HP(self, val):
        self.current_hp += val
        if self.current_hp > Hero.start_hp:
            self.current_hp = Hero.start_hp
        elif self.current_hp < 0:
            self.is_dead = True

    def buy_minion(self, minion):
        if self.current_gold < 3:
            return False
        else:
             if not self.add_minion_in_hand(minion): return False
             else:
                self.current_gold -= 3
                minion.set_state(State.in_hand)
                return True

    def play_minion(self, minion):
        self.hand[minion.position] = None
        if not self.add_minion(minion): return False
        minion.set_state(State.in_play)
        minion.check_effects(State.in_hand, State.in_play, minion)
        return True

    def sell_minion(self, minion):
        if minion.get_state() != State.in_play: return False
        self.minions[minion.position] = None
        minion.state = State.in_storage
        self.current_gold = min(self.current_gold + 1, Hero.current_max_gold)
        return True

    def on_new_turn(self):
        self.current_max_gold = min(self.current_max_gold + 1, Hero.max_gold)
        self.current_gold = self.current_max_gold

    def get_minions(self):
        return self.minions

    def get_hand(self):
        return self.hand

    def add_minion_in_hand(self, minion):
        index = find_first_free_index(self.hand)
        if index < 0: return False
        minion.set_position(index)
        self.hand[index] = minion
        return True

    def add_minion(self, minion):
        index = find_first_free_index(self.minions)
        if index < 0: return False
        minion.set_position(index)
        self.minions[index] = minion
        return True

    def get_current_tier(self):
        return self.current_tier


class Player:
    def __init__(self, hero):
        self.hero = Hero("test", None)

    def get_hero(self):
        return self.hero
