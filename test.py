from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty, StringProperty, DictProperty, ListProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

import WikiPage

Builder.load_file("test.kv")

class SearchWindow(Screen,RelativeLayout):
    search_by_url = ObjectProperty(None)
    search_by_name_first = ObjectProperty(None)
    search_by_name_last = ObjectProperty(None)

    # sm = ScreenManager()

    # button for getting the recommendetions
    def btn(self):
        close_button = Button(text="close")
        layout = GridLayout(cols=1)




        url = ""
        if self.search_by_url.text != "":
            url = self.search_by_url.text
            self.search_by_url.text = ""

        elif self.search_by_name_first.text != "" and self.search_by_name_last != "":
            url = "https://en.wikipedia.org/wiki/" + self.search_by_name_first.text + "_" + self.search_by_name_last.text
            self.search_by_name_first.text = ""
            self.search_by_name_last.text = ""
        if url != "":
            page = WikiPage.WikiPage(url)
            if page.check_url():
                try:
                    page.init_detail()
                    self.manager.page = page
                    self.manager.get_screen("player").update_details()
                    self.manager.get_screen('time_line').player_dict = page.dict_by_year
                    self.manager.get_screen('time_line').keys = self.manager.get_screen('time_line').player_dict.keys()
                    self.manager.get_screen('time_line').curr_year = self.manager.get_screen('time_line').keys[0]
                    self.manager.get_screen('time_line').next_year = self.manager.get_screen('time_line').keys[1]
                    self.manager.get_screen('time_line').index = 0
                    self.manager.get_screen('time_line').insert_current_year()
                    self.manager.current = "player"
                except:
                    layout.add_widget(Label(text='Player Not Found'))
                    layout.add_widget(close_button)
                    popup = Popup(title='Search Error', content=layout, size_hint=(None, None), size=(500, 500))
                    popup.open()
                    close_button.bind(on_press=popup.dismiss)
            else:
                layout.add_widget(Label(text='Player Not Found'))
                layout.add_widget(close_button)
                popup = Popup(title='Search Error', content=layout, size_hint=(None, None), size=(500, 500))
                popup.open()
                close_button.bind(on_press=popup.dismiss)
        else:
            layout.add_widget(Label(text='Please Enter Valid Input'))
            layout.add_widget(close_button)
            popup = Popup(title='Search Error', content=layout, size_hint=(None, None), size=(500, 500))
            popup.open()
            close_button.bind(on_press=popup.dismiss)



class PlayerScreen(Screen,GridLayout):
    player_name = StringProperty('')
    photo_url = StringProperty('')
    born_place = StringProperty('')
    born_date = StringProperty('')
    high_school = StringProperty('')
    college = StringProperty('')


    def update_details(self):
        self.player_name = self.manager.page.name
        self.photo_url = "http:" + self.manager.page.photo_url
        self.born_place = self.manager.page.born_place
        self.born_date = self.manager.page.born_date
        self.high_school = self.manager.page.high_school
        self.college = self.manager.page.college

    def btn(self):
        print(self.player_name)
        print(self.photo_url)
        print(self.born_place)
        print(self.born_date)
        print(self.high_school)
        print(self.college)
        # print(self.manager.page.dict_by_year)
        # self.manager.current='search'


class TimeLineScreen(Screen,Widget):
    player_dict =DictProperty({})
    prev_year = StringProperty("")
    curr_year = StringProperty("")
    next_year = StringProperty("")
    keys =  ListProperty([])
    index = 0

    def btn(self):
        print(self.player_dict)
        print(self.keys)
        print(self.curr_year)
        print(self.next_year)
        label = Label(text=str(self.index))
        self.ids.grid.add_widget(label)

    def prev_btn(self):
        if not self.index==0:
            self.index = self.index-1
            self.next_year = self.curr_year
            self.curr_year = self.prev_year
            if self.index==0:
                self.prev_year = ""
            else:
                self.prev_year = self.keys[self.index-1]
            self.insert_current_year()

    def next_btn(self):
        if not self.index==len(self.keys)-1:
            self.index = self.index+1
            self.prev_year = self.curr_year
            self.curr_year = self.next_year
            if self.index==len(self.keys)-1:
                self.next_year = ""
            else:
                self.next_year= self.keys[self.index+1]
            self.insert_current_year()

    def insert_current_year(self):
        self.ids.grid.clear_widgets()
        label = Label(text=self.curr_year)
        self.ids.grid.add_widget(label)
        achievements = self.player_dict[self.curr_year]
        for achievement in achievements:
            label = Label(text = achievement)
            self.ids.grid.add_widget(label)


class Manager(ScreenManager):
    page = None




class TestApp(App):
    def build(self):
        manager = Manager()
        manager.add_widget(SearchWindow(name='search'))
        manager.add_widget(PlayerScreen(name='player'))
        manager.add_widget(TimeLineScreen(name='time_line'))

        # Create the screen manager


        return manager

if __name__ == '__main__':
    TestApp().run()