import pyglet

class Label:
    def __init__(
        self, text=None, x=None, y=None, font_name=None, font_size=None,
        font_color=None, anchor_x=None, anchor_y=None):
        self.text = " " if not text else text
        self.x = 100 if not x else x
        self.y = 100 if not y else y
        self.font_name = 'Times New Roman' if not font_name else font_name
        self.font_size = 16 if not font_size else font_size
        self.font_color = (0, 0, 0, 255) if not font_color else font_color
        self.anchor_x = 'center' if not anchor_x else anchor_x
        self.anchor_y = 'center' if not anchor_y else anchor_y
        
        self._label = pyglet.text.Label(
            self.text, x=self.x, y=self.y, font_name=self.font_name,
            color=self.font_color, font_size=self.font_size, 
            anchor_x=self.anchor_x, anchor_y=self.anchor_y)
        
        self.active = True
    
    def on_draw(self):
        if self.active:
            self._label.draw()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        if hasattr(self, '_label'):
            self._label.text = self._text
