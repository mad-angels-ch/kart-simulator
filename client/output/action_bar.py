from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

Builder.load_file("client/output/action_bar.kv")

class BoxLayoutWithActionBar(BoxLayout):
    """Outil qui permet de naviguer entre les différents screens, 
    à l'aide de l'icone en haut à gauche de la page"""
    title = StringProperty()
