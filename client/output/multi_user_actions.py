import game.events

# Liens utilisateur-programme à travers le clavier, reliés à la classe MultiplayerGame lors de l'instanciation d'une partie


def keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self.keyboard_down)
    self._keyboard.unbind(on_key_up=self.keyboard_up)
    self._keyboard = None


def keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] in ["left", "a"]:
        self.newEvent(game.events.KartTurnEvent(1, self.myKart))

    if keycode[1] in ["right", "d"]:
        self.newEvent(game.events.KartTurnEvent(-1, self.myKart))

    if keycode[1] in ["up", "w"]:
        self.newEvent(game.events.KartMoveEvent(1, self.myKart))

    if keycode[1] in ["down", "s"]:
        self.newEvent(game.events.KartMoveEvent(-1, self.myKart))

    if keycode[1] == "escape":
        self.change_gameState()

    if keycode[1] == "x":
        self.newEvent(game.events.FireBallEvent(self.myKart))

    return True


def keyboard_up(self, keyboard, keycode):
    if keycode[1] in ["left", "a"]:
        self.newEvent(game.events.KartTurnEvent(0, self.myKart))

    if keycode[1] in ["right", "d"]:
        self.newEvent(game.events.KartTurnEvent(0, self.myKart))

    if keycode[1] in ["up", "w"]:
        self.newEvent(game.events.KartMoveEvent(0, self.myKart))

    if keycode[1] in ["down", "s"]:
        self.newEvent(game.events.KartMoveEvent(0, self.myKart))


def touch_down(self, touch):
    pass


def touch_up(self, touch):
    pass
