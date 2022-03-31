import game.events

# Liens utilisateur-programme à travers le clavier, relié à la class SingleplayerGame lors de l'instanciation d'un partie


def keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self.on_keyboard_down)
    self._keyboard.unbind(on_key_up=self.on_keyboard_up)
    self._keyboard = None


def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] in ["left", "a"]:
        self.newEvent(game.events.KartTurnEvent(1, -1))

    if keycode[1] in ["right", "d"]:
        self.newEvent(game.events.KartTurnEvent(-1, -1))

    if keycode[1] in ["up", "w"]:
        self.newEvent(game.events.KartMoveEvent(1, -1))

    if keycode[1] in ["down", "s"]:
        self.newEvent(game.events.KartMoveEvent(-1, -1))

    if keycode[1] == "escape":
        self.change_gameState()

    if keycode[1] == "x":
        self.newEvent(game.events.FireBallEvent(-1))

    return True


def on_keyboard_up(self, keyboard, keycode):
    if keycode[1] in ["left", "a"]:
        self.newEvent(game.events.KartTurnEvent(0, -1))

    if keycode[1] in ["right", "d"]:
        self.newEvent(game.events.KartTurnEvent(0, -1))

    if keycode[1] in ["up", "w"]:
        self.newEvent(game.events.KartMoveEvent(0, -1))

    if keycode[1] in ["down", "s"]:
        self.newEvent(game.events.KartMoveEvent(0, -1))


def on_touch_down(self, touch):
    pass


def on_touch_up(self, touch):
    pass
