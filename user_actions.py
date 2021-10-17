
def keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    self._keyboard.unbind(on_key_up=self._on_keyboard_up)
    self._keyboard = None

def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == 'left':
        print("LEFT")

    if keycode[1] == 'right':
        print("RIGHT")

    if keycode[1] == 'up':
        print("UP")

    if keycode[1] == 'down':
        print("DOWN")

    return True

def on_keyboard_up(self, keyboard, keycode):
    # return True
    pass


def on_touch_down(self, touch):
    pass

def on_touch_up(self, touch):
    pass