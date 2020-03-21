import enum


class Tribe(enum.Enum):
    human = 1
    orc = 2
    dwarf = 3
    elf = 4
    none = 5


class Condition:
    def check_condition(self, target):
        pass


class TribeCondition(Condition):
    def __init__(self, tribe):
        self.tribe = tribe

    def check_condition(self, target):
        return self.tribe == target.tribe


class Effect:
    def __init__(self, condition):
        self.condition = condition

    def trigger_effect(self, caster, target):
        pass


class BuffEffect(Effect):
    def __init__(self, health, attack, condition):
        super().__init__(condition)
        self.health = health
        self.attack = attack

    def trigger_effect(self, caster, targets):
        for t in targets:
            t.stats.update_attack(self.attack)
            t.stats.update_health(self.health)


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
    def __init__(self, tribe, effects, state, stats, position):
        self.tribe = tribe
        self.effects = effects
        self.state = state
        self.stats = stats
        self.position = position
        self.isDead = False

    def attack(self, target):
        self.stats.update_stats_after_attack(target.stats)
        target.stats.update_stats_after_attack(self.stats)
        if self.stats.health <= 0:
            self.isDead = True
        if target.stats.health <= 0:
            target.isDead = True


class Hero:
    max_minion_no = 7
    max_hand_no = 10
    start_hp = 30
    max_tier = 6
    starting_tier = 1

    def __init__(self, name, hero_power):
        self.name = name
        self.hero_power = hero_power
        self.current_tier = 1
        self.current_hp = Hero.start_hp
        self.is_dead = False;

    def upgrade_tier(self):
        if self.current_tier < Hero.max_tier: self.current_tier += 1

    def update_HP(self, val):
        self.current_hp += val
        if self.current_hp > Hero.start_hp:
            self.current_hp = Hero.start_hp
        elif self.current_hp < 0:
            self.is_dead = True
