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
from kivy.graphics import *
from kivy.animation import Animation,AnimationTransition

from kivy.clock import Clock
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.uix.image import Image


import Backend

Builder.load_file("Fronted.kv")

#this class display the search window
class SearchWindow(Screen,RelativeLayout):
    search_by_url = ObjectProperty(None)
    search_by_name_first = ObjectProperty(None)
    search_by_name_last = ObjectProperty(None)

    # sm = ScreenManager()

    # button for getting the player detailes
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
            page = Backend.WikiPage(url)
            #import the page of the player
            if page.check_url():
                try:
                    #init deatils of the player, parsing his all championship Trophies and etc
                    page.init_detail()
                    self.manager.page = page
                    #update_details  of the player as date of birth, place of birth,high school, college
                    self.manager.get_screen("player").update_details()
                    self.manager.get_screen('time_line').player_dict = page.dict_by_year
                    self.manager.get_screen('time_line').keys = self.manager.get_screen('time_line').player_dict.keys()
                    self.manager.get_screen('time_line').prev_year = "Back To Player Page"
                    self.manager.get_screen('time_line').curr_year = self.manager.get_screen('time_line').keys[0]
                    self.manager.get_screen('time_line').next_year = self.manager.get_screen('time_line').keys[1]
                    self.manager.get_screen('time_line').player_name = page.name + " Timeline"
                    self.manager.get_screen('time_line').index = 0
                    self.manager.get_screen('time_line').insert_current_year()
                    self.manager.current = "player"
                except:
                    #exception if the player is not exist
                    layout.add_widget(Label(text='Player Not Found'))
                    layout.add_widget(close_button)
                    popup = Popup(title='Search Error', content=layout, size_hint=(None, None), size=(500, 500))
                    popup.open()
                    close_button.bind(on_press=popup.dismiss)
            else:
                #pop up to the user  if the player is not exist
                layout.add_widget(Label(text='Player Not Found'))
                layout.add_widget(close_button)
                popup = Popup(title='Search Error', content=layout, size_hint=(None, None), size=(500, 500))
                popup.open()
                close_button.bind(on_press=popup.dismiss)
        else:
            # pop up to the user  if the player is not exist

            layout.add_widget(Label(text='Please Enter Valid Input'))
            layout.add_widget(close_button)
            popup = Popup(title='Search Error', content=layout, size_hint=(None, None), size=(500, 500))
            popup.open()
            close_button.bind(on_press=popup.dismiss)


#this class display the player window with his detailes

class PlayerScreen(Screen,GridLayout):
    player_name = StringProperty('')
    photo_url = StringProperty('')
    born_place = StringProperty('')
    born_date = StringProperty('')
    high_school = StringProperty('')
    college = StringProperty('')

    #this functiom update player's details
    def update_details(self):
        self.player_name = self.manager.page.name
        self.photo_url = "http:" + self.manager.page.photo_url
        self.born_place = self.manager.page.born_place
        self.born_date = self.manager.page.born_date
        self.high_school = self.manager.page.high_school
        self.college = self.manager.page.college



#this class display the timeline window of the player

class TimeLineScreen(Screen,Widget):
    player_name=StringProperty("")
    player_dict =DictProperty({})
    prev_year = StringProperty("")
    curr_year = StringProperty("")
    next_year = StringProperty("")
    keys =  ListProperty([])
    index = 0

    #this function moves the timeline to the previous year of the timeline
    def prev_btn(self):
        if not self.index==0:
            self.index = self.index-1
            self.next_year = self.curr_year
            self.curr_year = self.prev_year
            if self.index==0:
                self.prev_year = "Back To Player Page"
            else:
                self.prev_year = self.keys[self.index-1]
            self.insert_current_year()
        else:
            self.manager.current = 'player'

    #this function moves the timeline to the next year of the timeline
    def next_btn(self):
        if not self.index==len(self.keys)-1:
            self.index = self.index+1
            self.prev_year = self.curr_year
            self.curr_year = self.next_year
            if self.index==len(self.keys)-1:
                self.next_year = "Back To Search"
            else:
                self.next_year= self.keys[self.index+1]
            self.insert_current_year()
        else:
            self.manager.current = 'search'
    #this function insert all the player's achievments to the timeline
    def insert_current_year(self):
        grid = self.ids.grid
        grid.clear_widgets()
        #creating a dictionary of the champio
        photo_dict={}
        photo_dict["50–40–90 club"] = "images/504090 club.jpg"
        photo_dict["All-NBA First Team"] = "images/AllNBA First Team.jpg"
        photo_dict["All-NBA Second Team"] = "images/AllNBA Second Team .png"
        photo_dict["Arrived to Atlanta Hawks"] = "images/atl.png"
        photo_dict["Arrived to Brooklyn Nets"] = "images/bkn.png"
        photo_dict["Arrived to Boston Celtics"] = "images/bos.png"
        photo_dict["Arrived to Charlotte Hornets"] = "images/cha.png"
        photo_dict["Arrived to Chicago Bulls"] = "images/chi.png"
        photo_dict["Arrived to Cleveland Cavaliers"] = "images/cle.png"
        photo_dict["Arrived to Dallas Mavericks"] = "images/dal.png"
        photo_dict["Arrived to Denver Nuggets"] = "images/den.png"
        photo_dict["Arrived to Golden State Warriors"] = "images/gs.png"
        photo_dict["Arrived to Detroit Pistons"] = "images/det.png"
        photo_dict["Arrived to Houston Rockets"] = "images/hou.png"
        photo_dict["Arrived to Indiana Pacers"] = "images/ind.png"
        photo_dict["Arrived to Los Angeles Clippers"] = "images/lac.png"
        photo_dict["Arrived to Los Angeles Lakers"] = "images/lal.png"
        photo_dict["Arrived to Memphis Grizzlies"] = "images/mem.png"
        photo_dict["Arrived to Miami Heat"] = "images/mia.png"
        photo_dict["Arrived to Milwaukee Bucks"] = "images/mil.png"
        photo_dict["Arrived to Minnesota Timberwolves"] = "images/min.png"
        photo_dict["Arrived to New Orleans Pelicans"] = "images/no.png"
        photo_dict["Arrived to New York Knicks"] = "images/ny.png"
        photo_dict["Arrived to Oklahoma City Thunder"] = "images/okc.png"
        photo_dict["Arrived to Orlando Magic"] = "images/orl.png"
        photo_dict["Arrived to Philadelphia 76ers"] = "images/phi.png"
        photo_dict["Arrived to Phoenix Suns"] = "images/phx.png"
        photo_dict["Arrived to Portland Trail Blazers"] = "images/por.png"
        photo_dict["Arrived to San Antonio Spurs"] = "images/sa.png"
        photo_dict["Arrived to Sacramento Kings"] = "images/sac.png"
        photo_dict["Arrived to Toronto Raptors"] = "images/tor.png"
        photo_dict["Arrived to Utah Jazz"] = "images/utah.png"
        photo_dict["Arrived to Washington Wizards"] = "images/wsh.png"

        photo_dict["NBA All-Defensive First Team"] = "images/NBA AllDefensive First Team.jpg"
        photo_dict["NBA All-Defensive Second Team"] = "images/NBA AllDefensive Second Team.jpg"
        photo_dict["NBA All-Rookie First Team"] = "images/NBA All-Rookie First Team.jpg"
        photo_dict["NBA All-Star"] = "images/NBA AllStar.png"
        photo_dict["NBA assists leader"] = "images/NBA assists leader.jpg"
        photo_dict["McDonald's All-American Game MVP"] = "images/NBA Most Valuable Player.jpg"
        photo_dict["NBA All-Star Game MVP"] = "images/NBA Most Valuable Player.jpg"
        photo_dict["NBA Finals MVP"] = "images/NBA Most Valuable Player.jpg"
        photo_dict["NBA Most Valuable Player"] = "images/NBA Most Valuable Player.jpg"
        photo_dict["NBA Rookie of the Year"] = "images/NBA Rookie of the Year.jpg"
        photo_dict["NBA steals leader"] = "images/NBA steals leader.jpg"



        #adding empty labels
        label1 = Label()
        self.ids.grid.add_widget(label1)
        label2 = Label()
        self.ids.grid.add_widget(label2)
        label3 = Label()
        self.ids.grid.add_widget(label3)
        label7 = Label()
        self.ids.grid.add_widget(label7)
        label8 = Label()
        self.ids.grid.add_widget(label8)
        label9 = Label()
        self.ids.grid.add_widget(label9)

        #display the achivments of the player
        achievements = self.player_dict[self.curr_year]
        for achievement in achievements:
            for_time_line = achievement.rstrip()
            if len(for_time_line)>25:
                lst = for_time_line.split(" ")
                for_time_line = lst[0]
                found = False
                for i in lst[1:]:
                    if len(for_time_line)<25 and not found:
                        for_time_line = for_time_line+" "+i
                    else:
                        if not found:
                            found = True
                            for_time_line = for_time_line + "\n"
                        for_time_line = for_time_line+i
            new_grid = GridLayout(cols=1)
            new_grid.add_widget(Label(text = for_time_line, bold=True))
            if for_time_line in photo_dict.keys():
                new_grid.add_widget(Image(source=photo_dict[for_time_line]))
            elif "Selected by the" in for_time_line:
                new_grid.add_widget(Image(source="images/nbadraftlogo.png"))
            else:
                new_grid.add_widget(Image(source="images/NBA.jpg"))
            # new_grid.add_widget(Image(source="atl.png"))
            self.ids.grid.add_widget(new_grid)
            # self.ids.grid.add_widget(Label(text = achievement))
        #add empty labels
        label4 = Label()
        self.ids.grid.add_widget(label4)
        label5 = Label()
        self.ids.grid.add_widget(label5)
        label6 = Label()
        self.ids.grid.add_widget(label6)


class Manager(ScreenManager):
    page = None


class Line(Widget):
    pass


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