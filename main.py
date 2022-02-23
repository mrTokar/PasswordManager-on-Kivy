from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window
Window.size = (480, 853)

from db_functions import DB

class Container(BoxLayout):

    search = ObjectProperty()

    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)
        self.db = DB(user)

    def test(self):
        self.search.text = str(self.db.load("Example"))

class MainApp(App):
    
    def build(self):
        return Container("tokar")

if __name__ == "__main__":
    MainApp().run()