import sentry_sdk

sentry_sdk.init(
    "https://fe63c5db7e2a4112b551a318061e751a@o1107229.ingest.sentry.io/6263977",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    release="kart-simulator@2.0.2",
)

from kivy.config import Config
from kivy.core.window import Window
from client.output.application import MenuApp

Window.fullscreen = 'auto'

Config.set("kivy", "exit_on_escape", "0")
Config.set("input", "mouse", "mouse,multitouch_on_demand")

MenuApp().run()
