import game.events
def keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self.on_keyboard_down)
    self._keyboard.unbind(on_key_up=self.on_keyboard_up)
    self._keyboard = None

def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == 'left':
        self.eventsList.append(game.events.FlipperEvent(upward=True, targetsName="leftFlipper"))
        print("LEFT")

    if keycode[1] == 'right':
        self.eventsList.append(game.events.FlipperEvent(upward=True, targetsName="rightFlipper"))

        print("RIGHT")

    if keycode[1] == 'up':
        print("UP")

    if keycode[1] == 'down':
        print("DOWN")

    return True

def on_keyboard_up(self, keyboard, keycode):
    if keycode[1] == 'left':
        self.eventsList.append(game.events.FlipperEvent(upward=False, targetsName="leftFlipper"))

    if keycode[1] == 'right':
        self.eventsList.append(game.events.FlipperEvent(upward=False, targetsName="rightFlipper"))


def on_touch_down(self, touch):
    pass

def on_touch_up(self, touch):
    pass