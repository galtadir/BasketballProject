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
                    self.manager.get_screen('time_line').prev_year = "Back To Player Page"
                    self.manager.get_screen('time_line').curr_year = self.manager.get_screen('time_line').keys[0]
                    self.manager.get_screen('time_line').next_year = self.manager.get_screen('time_line').keys[1]
                    self.manager.get_screen('time_line').player_name = page.name + " TimeLine"
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

class LineEllipse1:
    pass
class ClockRect(Widget):
    velocity = ListProperty([10, 15])

    def __init__(self, **kwargs):
        super(ClockRect, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 60.)

    def update(self, *args):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        if self.x < 0 or (self.x + self.width) > Window.width:
            self.velocity[0] *= -1
        if self.y < 0 or (self.y + self.height) > Window.height:
            self.velocity[1] *= -1
class TimeLineScreen(Screen,Widget):
    player_name=StringProperty("")
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
                self.prev_year = "Back To Player Page"
            else:
                self.prev_year = self.keys[self.index-1]
            self.insert_current_year()
        else:
            self.manager.current = 'player'

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

    def insert_current_year(self):
        grid = self.ids.grid
        grid.clear_widgets()
        photo_dict={}
        photo_dict["50–40–90 club"] = "50–40–90 club.jpg"
        photo_dict["All-NBA First Team"] = "All-NBA First Team.jpg"
        photo_dict["All-NBA Second Team"] = "All-NBA Second Team .png"
        photo_dict["Arrived to Atlanta Hawks"] = "atl.png"
        photo_dict["Arrived to Brooklyn Nets"] = "bkn.png"
        photo_dict["Arrived to Boston Celtics"] = "bos.png"
        photo_dict["Arrived to Charlotte Hornets"] = "cha.png"
        photo_dict["Arrived to Chicago Bulls"] = "chi.png"
        photo_dict["Arrived to Cleveland Cavaliers"] = "cle.png"
        photo_dict["Arrived to Dallas Mavericks"] = "dal.png"
        photo_dict["Arrived to Denver Nuggets"] = "den.png"
        photo_dict["Arrived to Golden State Warriors"] = "gs.png"
        photo_dict["Arrived to Detroit Pistons"] = "det.png"
        photo_dict["Arrived to Houston Rockets"] = "hou.png"
        photo_dict["Arrived to Indiana Pacers"] = "ind.png"
        photo_dict["Arrived to Los Angeles Clippers"] = "lac.png"
        photo_dict["Arrived to Los Angeles Lakers"] = "lal.png"
        photo_dict["Arrived to Memphis Grizzlies"] = "mem.png"
        photo_dict["Arrived to Miami Heat"] = "mia.png"
        photo_dict["Arrived to Milwaukee Bucks"] = "mil.png"
        photo_dict["Arrived to Minnesota Timberwolves"] = "min.png"
        photo_dict["Arrived to New Orleans Pelicans"] = "no.png"
        photo_dict["Arrived to New York Knicks"] = "ny.png"
        photo_dict["Arrived to Oklahoma City Thunder"] = "okc.png"
        photo_dict["Arrived to Orlando Magic"] = "orl.png"
        photo_dict["Arrived to Philadelphia 76ers"] = "phi.png"
        photo_dict["Arrived to Phoenix Suns"] = "phx.png"
        photo_dict["Arrived to Portland Trail Blazers"] = "por.png"
        photo_dict["Arrived to San Antonio Spurs"] = "sa.png"
        photo_dict["Arrived to Sacramento Kings"] = "sac.png"
        photo_dict["Arrived to Toronto Raptors"] = "tor.png"
        photo_dict["Arrived to Utah Jazz"] = "utah.png"
        photo_dict["Arrived to Washington Wizards"] = "wsh.png"

        photo_dict["NBA All-Defensive First Team"] = "NBA All-Defensive First Team.jpg"
        photo_dict["NBA All-Defensive Second Team"] = "NBA All-Defensive Second Team.jpg"
        photo_dict["NBA All-Rookie First Team"] = "NBA All-Rookie First Team.jpg"
        photo_dict["NBA All-Star"] = "NBA All-Star.png"
        photo_dict["NBA assists leader"] = "NBA assists leader.jpg"
        photo_dict["McDonald's All-American Game MVP"] = "NBA Most Valuable Player.jpg"
        photo_dict["NBA All-Star Game MVP"] = "NBA Most Valuable Player.jpg"
        photo_dict["NBA Finals MVP"] = "NBA Most Valuable Player.jpg"
        photo_dict["NBA Most Valuable Player"] = "NBA Most Valuable Player.jpg"
        photo_dict["NBA Rookie of the Year"] = "NBA Rookie of the Year.jpg"
        photo_dict["NBA steals leader"] = "NBA steals leader.jpg"




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
                new_grid.add_widget(Image(source="nbadraftlogo.png"))
            else:
                new_grid.add_widget(Image(source="NBA.jpg"))
            # new_grid.add_widget(Image(source="atl.png"))
            self.ids.grid.add_widget(new_grid)
            # self.ids.grid.add_widget(Label(text = achievement))

        label4 = Label()
        self.ids.grid.add_widget(label4)
        label5 = Label()
        self.ids.grid.add_widget(label5)
        label6 = Label()
        self.ids.grid.add_widget(label6)

        # with self.canvas:
        #     # Add a red color
        #     Color(1., 0, 0)
        #
        #     # Add a rectangle
        # rec=Rectangle(pos=(10, 10), size=(500, 500))
        #
        #     Line(pos=(10, 10), size=(500, 500))
        # label = Label(text=self.curr_year,pos_hint={'top':1.0, 'right':.7})
        # self.ids.grid.add_widget(label)
        # print(self.curr_year)
        # grid = GridLayout()
        # grid.add_widget(ClockRect())
        # clock=LineEllipse1()
        # anim = Animation(pos=(100,100),duration=5)
        # anim.start(clock)
        # self.ids.grid.add_widget(anim)

        # self.ig = InstructionGroup()
        # self.line = Line(points=[100, 200, 300, 400])
        # self.ig.add(self.line)
        # self.canvas.add(self.ig)




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