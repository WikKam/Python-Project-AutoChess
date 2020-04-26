import enum
import copy
import random


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


class State(enum.Enum):
    in_shop = 1
    in_hand = 2
    in_play = 3
    in_storage = 4
    on_battlefield = 5
    dead = 6


class TriggerOn(enum.Enum):
    on_enter_play = 1
    on_enter_hand = 2
    on_death = 3
    whenever_minion_played = 4
    on_end_of_turn = 5


def mapStatesToTriggerOn(before, after):
    if before == State.in_hand and after == State.in_play:
        return TriggerOn.on_enter_play
    if before == State.in_shop and after == State.in_hand:
        return TriggerOn.on_enter_hand
    if before == State.on_battlefield and after == State.dead:
        return TriggerOn.on_death
    if before == State.in_play and after == State.on_battlefield:
        return TriggerOn.on_end_of_turn


class Effect:
    def __init__(self, trigger_when, kind, target_tribe):
        self.trigger_when = trigger_when
        self.kind = kind
        self.target_tribe = target_tribe

    def trigger_effect(self, caster, target):
        pass


class StatBuffEffect(Effect):
    def __init__(self, health, attack, triggered_when, kind, target_tribe):
        super().__init__(triggered_when, kind, target_tribe)
        self.health = health
        self.attack = attack

    def trigger_effect(self, caster, target):
        target.stats.update_health(self.health)
        target.stats.update_attack(self.attack)


class EffectManager:

    def activate_effects(self, prev, current, source):
        for effect in source.effects:
            trigger_on = mapStatesToTriggerOn(prev, current)
            if trigger_on == effect.trigger_when:
                if effect.kind == TargetKind.random:
                    target = self.pick_random_target(effect,source)
                    if target:
                        effect.trigger_effect(self, target)

    def __init__(self, minions_in_play):
        self.minions_in_play = minions_in_play

    def pick_random_target(self, effect, source):
        matching_targets = [minion for minion in self.minions_in_play
                            if minion is not None and
                            minion != source and
                            (minion.tribe == effect.target_tribe or
                             (effect.target_tribe or minion.tribe == Tribe.all))]
        if len(matching_targets) == 0:
            return None
        else:
            index = random.randint(0, len(matching_targets) - 1)
            return matching_targets[index]


class SummonEffect(Effect):
    def __init__(self, minion, triggered_when, kind, target_tribe):
        super().__init__(triggered_when, kind, target_tribe)
        self.minion = minion

    def trigger_effect(self, caster, target):
        target = self.minion


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
    def __init__(self, name, tribe, effects, state, stats, icon_path):
        self.tribe = tribe
        self.effects = effects
        self.state = state
        self.stats = stats
        self.combat_stats = copy.deepcopy(stats)
        self.isDead = False
        self.name = name
        self.icon_path = icon_path

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

    def __init__(self, name, hero_power, icon):
        self.name = name
        self.hero_power = hero_power
        self.current_tier = 1
        self.current_hp = Hero.start_hp
        self.is_dead = False
        self.minions = [None, None, None, None, None, None, None]
        self.hand = [None, None, None, None, None]
        self.current_gold = 6
        self.current_upgrade_cost = 6
        self.max_upgrade_cost = 6
        self.reroll_cost = 1
        self.icon = icon
        self.effect_manager = EffectManager(self.minions)

    def can_upgrade_tier(self):
        return self.current_upgrade_cost < self.current_gold and self.current_tier < Hero.max_tier

    def upgrade_tier(self):
        if not self.can_upgrade_tier(): return False
        self.current_tier += 1
        self.current_gold -= self.current_upgrade_cost
        self.current_upgrade_cost = self.max_upgrade_cost
        return True

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
            if not self.add_minion_in_hand(minion):
                return False
            else:
                self.current_gold -= 3
                minion.set_state(State.in_hand)
                self.effect_manager.activate_effects(State.in_shop, State.in_hand, minion)
                return True

    def play_minion(self, minion):
        self.hand[minion.position] = None
        if not self.add_minion(minion): return False
        minion.set_state(State.in_play)
        self.effect_manager.activate_effects(State.in_hand, State.in_play, minion)
        return True

    def sell_minion(self, minion):
        if minion.get_state() != State.in_play: return False
        self.minions[minion.position] = None
        minion.set_state(State.in_storage)
        self.current_gold = min(self.current_gold + 1, Hero.current_max_gold)
        self.effect_manager.activate_effects(State.in_shop, State.in_storage, minion)
        return True

    def on_new_turn(self):
        self.current_max_gold = min(self.current_max_gold + 1, Hero.max_gold)
        self.current_gold = self.current_max_gold
        self.current_upgrade_cost = max(self.current_upgrade_cost - 1, 0)
        minions = [minion for minion in self.minions if minion is not None]
        for minion in minions:
            minion.set_state(State.in_play)
            self.effect_manager.activate_effects(State.on_battlefield, State.in_play, minion)

    def on_turn_end(self):
        minions = [minion for minion in self.minions if minion is not None]
        for minion in minions:
            minion.set_state(State.on_battlefield)
            self.effect_manager.activate_effects(State.in_play,State.on_battlefield, minion)

    def get_minions(self):
        return self.minions

    def get_hand(self):
        return self.hand

    def add_minion_in_hand(self, minion):
        minion.state = State.in_hand
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

    def on_tavern_reroll(self):
        self.current_gold -= self.reroll_cost

    def can_reroll_tavern(self):
        return self.current_gold >= self.reroll_cost


class Player:
    def __init__(self, hero, id):
        self.hero = hero
        self.id = id
        self.ready = False

    def get_hero(self):
        return self.hero

    def recruit_hero(self, hero):
        self.hero = hero
