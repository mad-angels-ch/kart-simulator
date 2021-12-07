from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

Builder.load_file("action_bar.kv")

class BoxLayoutWithActionBar(BoxLayout):
    title = StringProperty()
