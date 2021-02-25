import pyglet
import os
import random

from functools import partial
from turns import TurnCounter
turn_counter = TurnCounter()

def load_from_resource_folder(name, anchor_x_perc=None, anchor_y_perc=None):
    image = pyglet.image.load(os.path.join(os.getcwd(), 'card_images', name))
    if not anchor_x_perc is None and isinstance(anchor_x_perc, int):
        image.anchor_x = int(image.width * min(max(anchor_x_perc, 0), 100) / 100)
    if not anchor_y_perc is None and isinstance(anchor_y_perc, int):
        image.anchor_y = int(image.height * min(max(anchor_y_perc, 0), 100) / 100)
    return image

def sprite_from_image(image):
    return pyglet.sprite.Sprite(image)

class Card:
    def is_castable_by(self, caster):
        if hasattr(self, 'energy_cost') and caster.energy < self.energy_cost:
            return False
        if hasattr(self, 'holy_power_cost') and caster.holy_power < self.holy_power_cost:
            return False
        if hasattr(self, 'combo_points_cost') and caster.combo_points < self.combo_points_cost:
            return False
        return True

    def casting(self, caster, target):
        if hasattr(self, 'energy_cost'):
            caster.energy -= self.energy_cost
        if hasattr(self, 'combo_points_cost'):
            caster.combo_points -= self.combo_points_cost
        if hasattr(self, 'holy_power_cost'):
            caster.holy_power -= self.holy_power_cost
        if hasattr(self, 'damage'):
            target.hp -= self.damage
        if hasattr(self, 'combo_points_gain'):
            caster.combo_points += self.combo_points_gain
        if hasattr(self, 'holy_power_gain'):
            caster.holy_power += self.holy_power_gain
        if hasattr(self, "heal"):
            caster.hp += self.heal
        if hasattr(self, 'special'):
            self.special(caster, target)

class CrusaderStrike(Card):
    def __init__(self):
        self.name = "Crusader Strike"
        self.energy_cost = 1
        self.damage = 6
        self.holy_power_gain = 1
        self.sprite = sprite_from_image(load_from_resource_folder('cs.png'))

class ShieldOfTheRighteous(Card):
    def __init__(self):
        self.name = "Shield of the Righteous"
        self.damage = 30
        self.holy_power_cost = 3
        self.sprite = sprite_from_image(load_from_resource_folder('shotr.png'))

class WordOfGlory(Card):
    def __init__(self):
        self.name = "Word of Glory"
        self.holy_power_cost = 3
        self.heal = 15
        self.sprite = sprite_from_image(load_from_resource_folder('wog.png'))

class AvengerShield(Card):
    def __init__(self):
        self.name = "Avenger Shield"
        self.holy_power_gain = 1
        self.damage = 9
        self.energy_cost = 1
        self.sprite = sprite_from_image(load_from_resource_folder("as.png"))

    def special(self, caster, target):
        if random.choice([True, False]):
            caster.deck.hand.append(AvengerShieldCopy())

class AvengerShieldCopy(AvengerShield):
    def __init__(self):
        super().__init__()
        self.energy_cost = 0
        self.exhaust = True

    def special(self, caster, target):
        pass

class Consecration(Card):
    def __init__(self):
        self.name = "Consecration"
        self.holy_power_gain = 1
        self.damage = 4
        self.energy_cost = 1
        self.sprite = sprite_from_image(load_from_resource_folder('cons.png'))

    def special(self, caster, target):
        action = partial(self.tick, caster, target)
        turn_counter.schedule_for_x_turns(6, action)
    
    def tick(self, caster, target):
        target.hp -= self.damage

class SliceAndDice(Card):
    def __init__(self):
        self.name = "Slice and Dice"
        self.combo_points_cost = 2
        self.energy_cost = 2
        self.sprite = sprite_from_image(load_from_resource_folder('snd.png'))
    
    def special(self, caster, target):
        caster.base_energy += 1
        caster.energy += 0 # updating label
        turn_counter.queue_action(turn_counter.current+11, partial(self.restore, caster, target))
    
    def restore(self, caster, target):
        caster.base_energy -= 1
        caster.energy += 0

class BackStab(Card):
    def __init__(self):
        self.name = "Backstab"
        self.energy_cost = 1
        self.combo_points_gain = 1
        self.damage = 6
        self.sprite = sprite_from_image(load_from_resource_folder('bs.png'))

class CrimsonVial(Card):
    def __init__(self):
        self.name = "Crimson Vial"
        self.heal = 30
        self.energy_cost = 2
        self.sprite = sprite_from_image(load_from_resource_folder('cv.png'))

class Eviscerate(Card):
    def __init__(self):
        self.name = "Eviscerate"
        self.energy_cost = 1
        self.damage_per_combo_points = 10
        self.sprite = sprite_from_image(load_from_resource_folder('evis.png'))
    
    def special(self, caster, target):
        target.hp -= self.damage_per_combo_points * max(min(caster.combo_points, 5), 0)
        caster.combo_points = 0

class AdrenalineRush(Card):
    def __init__(self):
        self.name = "Adrenaline Rush"
        self.exhaust = True
        self.retain = True
        self.sprite = sprite_from_image(load_from_resource_folder('ar.png'))
    
    def special(self, caster, target):
        caster.card_draw += 2
        caster.deck.card_draw = caster.card_draw
        turn_counter.queue_action(turn_counter.current+5, partial(self.restore, caster, target))
    
    def restore(self, caster, target):
        caster.card_draw -= 2
        caster.deck.card_draw -= 2
