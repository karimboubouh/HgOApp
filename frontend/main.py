from kivy.lang.builder import Builder
from kivymd.app import MDApp

from src.screens import *
# Window.size = (336, 600)


class SmartFedApp(MDApp):

    def build(self):
        return Builder.load_file('src/template.kv')


SmartFedApp().run()
