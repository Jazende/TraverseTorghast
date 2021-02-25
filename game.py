import pyglet
import random

from pyglet.gl import *

from label import Label
from turns import TurnCounter
from classes import Paladin, Rogue
from enemies import Boar, Defias, Worgen

class Game:
    def __init__(self):
        self.end_turn_label = Label('END TURN', x=400, y=200, anchor_x='center', anchor_y='center')
        self.mouse_position = {'mouse_x': 0, 'mouse_y': 0, }

        self.player = Paladin()
        self.enemy = Boar()
        self.enemy_list = [Defias(), Boar(5), Worgen(), Defias(5), Worgen(5), ]
        self.wins = 0

        self.turn_counter = TurnCounter()
    
    @property
    def turn(self):
        return self.turn_counter.current

    @turn.setter
    def turn(self, value):
        self.turn_counter.current = value
        if value % 2 == 0:
            self.player.global_start_turn()

    def update(self, dt):
        if self.turn < 0:
            self.turn += 1
        if self.enemy.hp <= 0:
            self.wins += 1
            if len(self.enemy_list) == 0:
                return
            self.enemy = self.enemy_list.pop(0)

    def on_draw(self):
        self.setup_ui()
        self.player.on_draw()
        self.enemy.on_draw()
        self.end_turn_label.on_draw()

        # if not self.mouse_position['mouse_y'] <= 230:
        #     return

        for card in self.player.deck.hand:
            # if not (card.sprite.x <= self.mouse_position['mouse_x'] <= card.sprite.x + card.sprite.width and \
            #     card.sprite.y <= self.mouse_position['mouse_y'] <= card.sprite.y + card.sprite.width):
            #     continue
                
            left = card.sprite.x-1
            right = card.sprite.x+card.sprite.width+1
            bot = card.sprite.y-1
            top = card.sprite.y+card.sprite.height+1

            color = (1, 0, 0) if card.is_castable_by(self.player) == False else (0, 1, 0)
                
            glLineWidth(2)
            glBegin(GL_LINE_LOOP)
            glColor3f(*color)
            glVertex2f(left, bot)
            glVertex2f(right, bot)
            glVertex2f(right, top)
            glVertex2f(left, top)
            glEnd()

    def setup_ui(self):
        if not hasattr(self, 'vertex_list_base'):
            self.vertex_list_base = pyglet.graphics.vertex_list(8,
                ('v2f', (
                      0, 200, 320, 200,   # bottom left half
                    400, 230, 400, 600,   # middle beam
                    480, 200, 800, 200,   # bottom right half
                      0, 600, 800, 600,   # top bar
                    )),
                ('c4f', (0, 0, 0, 1)*8)
            )
        if not hasattr(self, 'vertex_list_button'):
            self.vertex_list_button = pyglet.graphics.vertex_list(8,
                ('v2f', (
                    320, 230, 320, 170, # Left Border End Turn Button
                    480, 230, 480, 170, # Right Border End Turn Button
                    350, 230, 450, 230, # Top Border End Turn Button
                    350, 170, 450, 170, # Bottom Border End Turn Button
                )),
                ('c4f', (0, 0, 0, 1)*8)
            )            
        if not hasattr(self, 'vertex_list_red_button'):
            self.vertex_list_red_button = pyglet.graphics.vertex_list(8,
                ('v2f', (
                    320, 170, 320, 230, # left border end turn button glow
                    320, 230, 480, 230, # top border end tun button glow
                    480, 230, 480, 170, # right border end turn button glow
                    480, 170, 320, 170, # bottom border end turn button glow
                )),
                ('c4f', (1, 0, 0, 1)*8)
            )
        glLineWidth(1)
        self.vertex_list_base.draw(pyglet.gl.GL_LINES)
        if 320 <= self.mouse_position['mouse_x'] <= 480 and 170 <= self.mouse_position['mouse_y'] <= 230:
            self.vertex_list_red_button.draw(pyglet.gl.GL_LINES)
        else:
            self.vertex_list_button.draw(pyglet.gl.GL_LINES)

    def enemy_turn(self, *args):
        if not self.enemy.hp > 0:
            return
        enemy_action = random.choice(self.enemy.actions)
        enemy_action(self.player)
        self.turn += 1

    def player_turn_start(self):
        self.player.start_turn()

    def on_mouse_motion(self, mouse_x, mouse_y, delta_x, delta_y):
        self.mouse_position['mouse_x'] = mouse_x
        self.mouse_position['mouse_y'] = mouse_y

    def on_mouse_drag(self, mouse_x, mouse_y, delta_x, delta_y, button, modifiers):
        self.mouse_position['mouse_x'] = mouse_x
        self.mouse_position['mouse_y'] = mouse_y

    def on_mouse_press(self, mouse_x, mouse_y, button, modifiers):
        self.mouse_position['mouse_x'] = mouse_x
        self.mouse_position['mouse_y'] = mouse_y

        if not self.turn % 2 == 0:
            return
        
        if 320 <= mouse_x <= 480 and 170 <= mouse_y <= 230:
            self.player.deck.end_turn()
            self.turn += 1
            pyglet.clock.schedule_once(self.enemy_turn, 1)

        if mouse_y <= 200:
            for card in self.player.deck.hand:
                if card.sprite.x <= mouse_x <= card.sprite.x + card.sprite.width and \
                    card.sprite.y <= mouse_y <= card.sprite.y + card.sprite.width:
                    self.player.play_card(card, self.enemy)

    def on_mouse_release(self, mouse_x, mouse_y, button, modifiers):
        self.mouse_position['mouse_x'] = mouse_x
        self.mouse_position['mouse_y'] = mouse_y
