import game.events
from kivy.lang import Builder

# Liens utilisateur-programme à travers le clavier, relié à la class MainWidget lors de l'instanciation d'un partie


def keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self.on_keyboard_down)
    self._keyboard.unbind(on_key_up=self.on_keyboard_up)
    self._keyboard = None


def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] in ["left", "a"]:
        if self.kart_ID:
            self.eventsList.append(game.events.KartTurnEvent(1, self.kart_ID))
        self.eventsList.append(game.events.FlipperEvent(True, "leftFlipper"))

    if keycode[1] in ["right", "d"]:
        if self.kart_ID:
            self.eventsList.append(game.events.KartTurnEvent(-1, self.kart_ID))
        self.eventsList.append(game.events.FlipperEvent(True, "rightFlipper"))

    if keycode[1] in ["up", "w"]:
        if self.kart_ID:
            self.eventsList.append(game.events.KartMoveEvent(1, self.kart_ID))

    if keycode[1] in ["down", "s"]:
        if self.kart_ID:
            self.eventsList.append(game.events.KartMoveEvent(-1, self.kart_ID))

    if keycode[1] == "escape":
        if self.play:
            self.play = False
            self.parentScreen.pauseMode()
        else:
            self.parentScreen.resumeGame()
            self.play = True

    if keycode[1] == "x":
        if self.kart_ID:
            self.eventsList.append(game.events.FireBallEvent(self.kart_ID))

    return True


def on_keyboard_up(self, keyboard, keycode):
    if keycode[1] in ["left", "a"]:
        if self.kart_ID:
            self.eventsList.append(game.events.KartTurnEvent(0, self.kart_ID))
        self.eventsList.append(game.events.FlipperEvent(False, "leftFlipper"))

    if keycode[1] in ["right", "d"]:
        if self.kart_ID:
            self.eventsList.append(game.events.KartTurnEvent(0, self.kart_ID))
        self.eventsList.append(game.events.FlipperEvent(False, "rightFlipper"))

    if keycode[1] in ["up", "w"]:
        if self.kart_ID:
            self.eventsList.append(game.events.KartMoveEvent(0, self.kart_ID))

    if keycode[1] in ["down", "s"]:
        if self.kart_ID:
            self.eventsList.append(game.events.KartMoveEvent(0, self.kart_ID))


def on_touch_down(self, touch):
    pass


def on_touch_up(self, touch):
    pass
