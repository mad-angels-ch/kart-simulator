from kivy.config import Config

from client.output.application import MenuApp

Config.set("kivy", "exit_on_escape", "0")
Config.set("input", "mouse", "mouse,multitouch_on_demand")

MenuApp().run()
