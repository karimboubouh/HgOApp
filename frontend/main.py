from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.core.window import Window

from frontend.screens import *

Window.size = (336, 600)


class SmartFedApp(MDApp):

    def build(self):
        return Builder.load_file('template.kv')


SmartFedApp().run()
