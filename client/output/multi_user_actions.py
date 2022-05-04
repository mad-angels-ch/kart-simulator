import game.events

# Liens utilisateur-programme à travers le clavier, reliés à la classe MultiplayerGame lors de l'instanciation d'une partie
# Les <on_> présents devant les méthodes en solo ont été supprémés pour ne pas faire d'interférences/confusions avec l'interaction serveur-client


def keyboard_closed(self) -> None:
    self._keyboard.unbind(on_key_down=self.keyboard_down)
    self._keyboard.unbind(on_key_up=self.keyboard_up)
    self.app.bind_keyboard()


def keyboard_down(self, keyboard, keycode, text, modifiers) -> True:
    if (
        keycode[1] in ["left", "a"]
        and self.play
        and self.myKart()
        and not self._rotating
    ):  # Si aucun kart ne nous a encore été attribué, self.myKart() a comme valeur par défaut "None".
        self._rotating = True
        self.newEvent(game.events.KartTurnEvent(1, self.myKart().formID()))

    if (
        keycode[1] in ["right", "d"]
        and self.play
        and self.myKart()
        and not self._rotating
    ):
        self._rotating = True
        self.newEvent(game.events.KartTurnEvent(-1, self.myKart().formID()))

    if keycode[1] in ["up", "w"] and self.play and self.myKart() and not self._moving:
        self._moving = True
        self.newEvent(game.events.KartMoveEvent(1, self.myKart().formID()))

    if keycode[1] in ["down", "s"] and self.play and self.myKart() and not self._moving:
        self._moving = True
        self.newEvent(game.events.KartMoveEvent(-1, self.myKart().formID()))

    if keycode[1] == "escape":
        self.change_gameState()

    if keycode[1] == "x" and self.play and self.myKart():
        self.newEvent(game.events.FireBallEvent(self.myKart().formID()))

    return True


def keyboard_up(self, keyboard, keycode) -> None:
    if keycode[1] in ["left", "a"] and self.play and self.myKart():
        self._rotating = False
        self.newEvent(game.events.KartTurnEvent(0, self.myKart().formID()))

    if keycode[1] in ["right", "d"] and self.play and self.myKart():
        self._rotating = False
        self.newEvent(game.events.KartTurnEvent(0, self.myKart().formID()))

    if keycode[1] in ["up", "w"] and self.play and self.myKart():
        self._moving = False
        self.newEvent(game.events.KartMoveEvent(0, self.myKart().formID()))

    if keycode[1] in ["down", "s"] and self.play and self.myKart():
        self._moving = False
        self.newEvent(game.events.KartMoveEvent(0, self.myKart().formID()))


def touch_down(self, touch) -> None:
    pass


def touch_up(self, touch) -> None:
    pass
