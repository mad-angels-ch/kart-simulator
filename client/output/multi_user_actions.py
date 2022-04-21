import game.events

# Liens utilisateur-programme à travers le clavier, reliés à la classe MultiplayerGame lors de l'instanciation d'une partie


def keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self.keyboard_down)
    self._keyboard.unbind(on_key_up=self.keyboard_up)
    self._keyboard = None


def keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] in ["left", "a"] and self._myKart: # Si aucun kart ne nous a encore été attribué, self._myKart a comme valeur par défaut "None".
        self.newEvent(game.events.KartTurnEvent(1, self._myKart.formID()))

    if keycode[1] in ["right", "d"] and self._myKart:
        self.newEvent(game.events.KartTurnEvent(-1, self._myKart.formID()))

    if keycode[1] in ["up", "w"] and self._myKart:
        self.newEvent(game.events.KartMoveEvent(1, self._myKart.formID()))

    if keycode[1] in ["down", "s"] and self._myKart:
        self.newEvent(game.events.KartMoveEvent(-1, self._myKart.formID()))

    if keycode[1] == "escape":
        self.change_gameState()

    if keycode[1] == "x" and self._myKart:
        self.newEvent(game.events.FireBallEvent(self._myKart.formID()))

    return True


def keyboard_up(self, keyboard, keycode):
    if keycode[1] in ["left", "a"] and self._myKart:
        self.newEvent(game.events.KartTurnEvent(0, self._myKart.formID()))

    if keycode[1] in ["right", "d"] and self._myKart:
        self.newEvent(game.events.KartTurnEvent(0, self._myKart.formID()))

    if keycode[1] in ["up", "w"] and self._myKart:
        self.newEvent(game.events.KartMoveEvent(0, self._myKart.formID()))

    if keycode[1] in ["down", "s"] and self._myKart:
        self.newEvent(game.events.KartMoveEvent(0, self._myKart.formID()))


def touch_down(self, touch):
    pass


def touch_up(self, touch):
    pass
