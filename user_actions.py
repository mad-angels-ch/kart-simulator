import game.events
from kivy.lang import Builder

def keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self.on_keyboard_down)
    self._keyboard.unbind(on_key_up=self.on_keyboard_up)
    self._keyboard = None

def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == 'left':
        if self.kart_ID:
            self.eventsList.append(game.events.KartTurningEvent(turning=1,targetFormID=self.kart_ID))
        self.eventsList.append(game.events.FlipperEvent(upward=True, targetsName="leftFlipper"))
        print("LEFT")


    if keycode[1] == 'right':
        if self.kart_ID:
            self.eventsList.append(game.events.KartTurningEvent(turning=-1,targetFormID=self.kart_ID))
        self.eventsList.append(game.events.FlipperEvent(upward=True, targetsName="rightFlipper"))

        print("RIGHT")

    if keycode[1] == 'up':
        if self.kart_ID:
            self.eventsList.append(game.events.KartAccelerationEvent(acceleration=2,targetFormID=self.kart_ID))
        print("UP")

    if keycode[1] == 'down':
        if self.kart_ID:
            self.eventsList.append(game.events.KartAccelerationEvent(acceleration=-2,targetFormID=self.kart_ID))
        print("DOWN")
        
    if keycode[1] == 'escape':
        if self.play:
            self.play = False
            self.parentScreen.pauseMode()
        else:
            self.parentScreen.resumeGame(self.parentScreen.pauseMenu.chosen_music)
            self.play = True
        print("PAUSE/RESUME")
        
    return True

def on_keyboard_up(self, keyboard, keycode):
    if keycode[1] == 'left':
        self.eventsList.append(game.events.FlipperEvent(upward=False, targetsName="leftFlipper"))

    if keycode[1] == 'right':
        self.eventsList.append(game.events.FlipperEvent(upward=False, targetsName="rightFlipper"))
        
    if keycode[1] == 'up':
        if self.kart_ID:
            self.eventsList.append(game.events.KartAccelerationEvent(acceleration=0,targetFormID=self.kart_ID))
        
    if keycode[1] == 'down':
        if self.kart_ID:
            self.eventsList.append(game.events.KartAccelerationEvent(acceleration=0,targetFormID=self.kart_ID))

def on_touch_down(self, touch):
    pass

def on_touch_up(self, touch):
    pass