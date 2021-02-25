from label import Label

class HPLabel:
    @property
    def hp(self):
        return self._hp
    
    @hp.setter
    def hp(self, value):
        self._hp = max(value, 0)
        if hasattr(self, 'max_hp'):
            self._hp = min(self.max_hp, self._hp)
        if hasattr(self, 'hp_label'):
            self.hp_label.text = f'{self._hp}'

class Player(HPLabel):
    def __new__(cls):
        obj = super(Player, cls).__new__(cls)
        cls.__init__(obj)
        Player.__init__(obj)
        return obj

    def __init__(self):
        self.hp_label = Label(f'{self.hp}', 200, 250, font_size=30, anchor_x='center', anchor_y='center')
        self.base_energy = 3
        self.energy = 0
        self.energy_label = Label(f'E: {self.energy} (+{self.base_energy})', 10, 580, font_size=15, anchor_x='left')
        self.card_draw = 4

    def global_start_turn(self):
        self.energy = self.base_energy
        self.deck.draw(self.card_draw)
        if hasattr(self, 'start_turn'):
            self.start_turn

    def play_card(self, card, target):
        if card.is_castable_by(self):
            card.casting(self, target)
            if hasattr(card, 'exhaust') and card.exhaust:
                self.deck.exhaust.append(self.deck.hand.pop(self.deck.hand.index(card)))
            else:
                self.deck.discard.append(self.deck.hand.pop(self.deck.hand.index(card)))

    def on_draw(self):
        self.hp_label.on_draw()
        self.energy_label.on_draw()
        self.deck.on_draw()

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, value):
        self._energy = value
        if hasattr(self, 'energy_label'):
            self.energy_label.text = f'E: {self.energy} (+{self.base_energy})'

class Enemy(HPLabel):
    def __new__(cls, *args, **kwargs):
        obj = super(Enemy, cls).__new__(cls)
        cls.__init__(obj, *args, **kwargs)
        Enemy.__init__(obj)
        return obj

    def __init__(self):
        self.hp_label = Label(f'{self.hp}', 600, 250, font_size=30, anchor_x='center', anchor_y='center')
        diff_label = f'(+{self.difficulty})' if self.difficulty else ''
        self.name_label = Label(f'{self.__class__.__name__} {diff_label}', 600, 580, font_size=25, anchor_x='center', anchor_y='center')

    def on_draw(self):
        self.hp_label.on_draw()
        self.name_label.on_draw()

    def __str__(self):
        return f'{self.__class__.__name__}(+{self.difficulty})'
