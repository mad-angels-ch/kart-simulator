from application import MenuApp
from kivy.config import Config
from kivy.core.window import Window

# Window.fullscreen = 'auto'
Config.set("kivy", "exit_on_escape", "0")
Config.set("input", "mouse", "mouse,multitouch_on_demand")


MenuApp().run()

# ##########################################################################
