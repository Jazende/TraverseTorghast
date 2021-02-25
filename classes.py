from deck import Deck
from cards import AvengerShield, Consecration, CrusaderStrike, ShieldOfTheRighteous, WordOfGlory
from cards import AdrenalineRush, BackStab, CrimsonVial, Eviscerate, SliceAndDice 
from utils import Player
from label import Label

class Paladin(Player):
    def __init__(self):
        self.hp = 80
        self.max_hp = 80
        self.holy_power = 0
        self.holy_power_label = Label(f'HoPo: {self.holy_power}', 340, 580, font_size=15, anchor_x='center', anchor_y='center')
        
        self.deck = Deck(
            CrusaderStrike(), CrusaderStrike(), CrusaderStrike(), AvengerShield(), 
            CrusaderStrike(), CrusaderStrike(), ShieldOfTheRighteous(), WordOfGlory(),
            Consecration(), 
            card_draw=4, 
        )

    @property
    def holy_power(self):
        return self._holy_power

    @holy_power.setter
    def holy_power(self, value):
        self._holy_power = min(value, 5)
        if hasattr(self, 'holy_power_label'):
            self.holy_power_label.text = f'HoPo: {self._holy_power}'

    def on_draw(self):
        super().on_draw()
        self.holy_power_label.on_draw()

class Rogue(Player):
    def __init__(self):
        self.hp = 60
        self.max_hp = 60
        self.combo_points = 0
        self.combo_points_label = Label(f'Combo: {self.combo_points}', 340, 580, font_size=15, anchor_x='center', anchor_y='center')

        self.deck = Deck(
            BackStab(), BackStab(), BackStab(), BackStab(), BackStab(), BackStab(), 
            CrimsonVial(), Eviscerate(), SliceAndDice(), SliceAndDice(), AdrenalineRush(), AdrenalineRush(), AdrenalineRush(), 
            card_draw=4, 
        )

        self.base_energy = 4

    @property
    def combo_points(self):
        return self._combo_points

    @combo_points.setter
    def combo_points(self, value):
        self._combo_points = min(value, 5)
        if hasattr(self, 'combo_points_label'):
            self.combo_points_label.text = f'Combo: {self._combo_points}'

    def on_draw(self):
        super().on_draw()
        self.combo_points_label.on_draw()
