import WikiPage

import kivy
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen


class TimeLine(Screen):
    pass



class MyGrid(Screen,RelativeLayout):
    search_by_url = ObjectProperty(None)
    search_by_name_first = ObjectProperty(None)
    search_by_name_last = ObjectProperty(None)
    # sm = ScreenManager()


    # button for getting the recommendetions
    def btn(self):
        url=""
        if self.search_by_url.text!="":
            url = self.search_by_url.text
            self.search_by_url.text=""

        elif self.search_by_name_first.text!="" and self.search_by_name_last!="":
            url = "https://en.wikipedia.org/wiki/"+self.search_by_name_first.text+"_" + self.search_by_name_last.text
            self.search_by_name_first.text=""
            self.search_by_name_last.text=""
        if url!="":
            page = WikiPage.WikiPage(url)
            if page.check_url():
                page.init_detail()
                print(page.getDictByYear())
                self.parent.current = "TimeLine"
            else:
                print("wrong")




class Fronted(App):
    def build(self):
        return MyGrid()


if __name__ == '__main__':
    Fronted().run()