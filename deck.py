import random
from label import Label

class Deck:
    def __init__(self, *base_cards, card_draw):
        self.card_draw = card_draw
        self.base_deck = [card for card in base_cards]
        self.deck_label = Label(f'0', x=10, y=100, font_size=15, anchor_x='left', anchor_y='center')
        self.discard_label = Label(f'0', x=790, y=100, font_size=15, anchor_x='right', anchor_y='center')
        self.start_combat()

    def start_combat(self):
        self.deck = [card for card in self.base_deck]
        self.hand = []
        self.discard = []
        self.exhaust = []

    def _draw_card(self):
        if len(self.deck) == 0 and len(self.discard) == 0:
            return
        elif len(self.deck) == 0:
            for _ in range(len(self.discard)):
                self.deck.append(self.discard.pop(0))
        self.hand.append(self.deck.pop(self.deck.index(random.choice(self.deck))))

    def update_labels(self):
        self.deck_label.text = f'{len(self.deck)} (+{self.card_draw})'
        self.discard_label.text = f'{len(self.discard)}'

    def draw(self, amount):
        for _ in range(amount):
            self._draw_card()

    def on_draw(self):
        self.update_labels()
        self.deck_label.on_draw()
        self.discard_label.on_draw()
        for idx, card in enumerate(self.hand):
            card.sprite.update(x=100*idx+100, y=20)
            card.sprite.draw()

    def end_turn(self):
        for idx in range(len(self.hand))[::-1]:
            if hasattr(self.hand[idx], 'retain') and self.hand[idx].retain:
                continue
            self.discard.append(self.hand.pop(idx))
