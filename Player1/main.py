''' TODO:::
1) 
2) 
3)
'''

# LIB REQUIRED IMPORTS
from functools import partial
import time
import string
import threading
from socket import error as sock_error

#KIVY IMPORTS
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.scrollview import ScrollView

#MY IMPORTS
from file_handle_C import File_man
from conns import connections

Window.size = (300, 560)

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# GAME_
# ********************************************************


class Game(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.Rec = Recycle()
        self.FM = File_man()
        self.details()

        self.deck = []
        self.card_count = 0
        self.TURN = False

        Clock.schedule_interval(partial(self.ft_UPDATER), 1)

    def pos_update(self, move):
        print("\n***********************************************\nUPDATING\n")
        try:
            self.FM.write_file("SOCKET_DATA/GAME.txt", move, "w")
            self.ids.OPP.text='ACTIVE'+'\nOPP_TURN'
            self.TURN = False
            print("\n\n     *****UPDATED*****\n\n*************************************\n", move)
            return "DONE"
        except:
            print("POSITION_CHANGE [NOT_UPDATED]")
            pass

    def at_hand(self):
        print("CARD_COUNT:: ", str(self.card_count))
        if self.card_count < 1:
            print("OUT OF CARDs")
            return
        if self.TURN == False:
            print("WAIT YOUR TURN")
            return
        self.card_count -= 1
        sel_card = self.deck[self.card_count]
        print("CARD TOUCHED", str(sel_card), str(self.card_count))
        move = "MOVE@"+str(sel_card)
        self.pos_update(move)
        return

    def ft_UPDATER(self, inst):
        server_data = str(self.FM.read_file("SOCKET_DATA/SERVER.txt"))
        my_data = str(self.FM.read_file("SOCKET_DATA/Player.txt"))
        if "1" in my_data:
            print("PLAYER_1")
            self.TURN = True
            self.ids['LOBBY_G'].text = "YOUR_*_TURN"
            self.FM.write_file("SOCKET_DATA/Player.txt", "", "w")
        if '2' in my_data:
            print("PLAYER_2")
            self.TURN = False
            self.ids['LOBBY_G'].text = "OPPs_*_TURN"
            self.FM.write_file("SOCKET_DATA/Player.txt", "", "w")
        if 'PL' not in my_data:
            pass

        try:
            if "MATCH" in server_data:
                print("SETTING DECK")
            cards = str(server_data).split("@")

            for i, _ in enumerate(cards):
                if 'MATCH1' in str(_):
                    self.TURN = True
                    self.ids['LOBBY_G'].text = "YOUR_*_TURN"
                if 'MATCH2' in str(_):
                    self.TURN = False
                    self.ids['LOBBY_G'].text = "OPPs_*_TURN"

                # BUILD DECK HERE

                if "C" in str(_):
                    try:
                        self.deck.append(str(cards[i]))
                        print("CARD::: ", str(cards[i]))
                        self.card_count += 1
                        print("CARD_COUNT:: ", str(self.card_count))
                    except:
                        print("CARDS NOT SET")
            self.FM.write_file("SOCKET_DATA/SERVER.txt", "", "w")
            return
        except Exception as e:
            print("LAYING_DECK:ERROR:: ", str(e))

        try:
            server_data = str(self.FM.read_file("SOCKET_DATA/SERVER.txt"))
            if "MOVE" in server_data:
                print("OPP_HAS_MOVED")
                self.ids['LOBBY_G'].text = "YOUR_TURN"
                self.TURN = True
                self.FM.write_file("SOCKET_DATA/SERVER.txt", "", "w")
                print(self.deck[self.card_count])
                self.card_count -= 1
                return
        except Exception as e:
            print("MOVE:ERROR::",str(e))

        try:
            turn = str(self.FM.read_file("SOCKET_DATA/Player.txt"))
            if "PL1" in turn:
                self.TURN = True
                print("YOUR TURN****")
                self.ids['LOBBY_G'].text = "YOUR_TURN"
                self.FM.write_file("SOCKET_DATA/Player.txt", "", "w")
            elif "PL2" in turn:
                self.ids['LOBBY_G'].text = "OPP_TURN"
                self.FM.write_file("SOCKET_DATA/Player.txt", "", "w")
                self.TURN = False
        except Exception as e:
            print("TURN:BASE:UPDATER_:ERROR:: ", str(e))

        # ASSIGN CARDS TO WIDGETS -> DECK (230, 250)
        # ON CLICK -> MOVE CARD TO RESPECTIVE TAB SLOT

        try:
            # print("UPDATING OPP DATA")
            OppData = str(self.FM.read_file("SOCKET_DATA/OppData.txt"))
            if len(OppData) <= 5:
                return
            else:
                print("LEN_OPP_DATA:: ", str(len(OppData)))
                Opp_Data = OppData.split("@")
                self.ids['oppName'].text = str(Opp_Data[1])
                self.ids['oppIcon'].text = str(Opp_Data[2])
                return
        except Exception as e:
            print("OPP_DATA:ERROR:ft_UPDATER:: ", str(e))

    def details(self):
        my_data = str(self.FM.read_file("SOCKET_DATA/Profile.txt"))
        print("MY_DETAILS:: ", str(my_data))
        mdata = my_data.split("@")
        try:
            # ICON IMAGE HERE
            self.ids['myIcon'].text = str(mdata[6])
            #ToDo::: DISPLAY THE ACTUAL ICON...
                            # ^^^^^^^^^^    ^^^
            self.ids['myName'].text = str(mdata[1]).translate(str.maketrans('','',string.punctuation))
        except Exception as e:
            print("myIcon:Loading:Error: ", str(e))

    def home_it(self):
        self.FM.write_file("SOCKET_DATA/GAME.txt", "QUIT", "w")
        self.pos_update("QUIT")
        time.sleep(1.5)
        self.FM.write_file("SOCKET_DATA/SERVER.txt", "", "w")
        self.FM.write_file("SOCKET_DATA/game_over.txt", "", "w")
        self.FM.write_file("SOCKET_DATA/GAME.txt", "", "w")
        MDApp.get_running_app().root.current = 'Home'


class Lobby(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()


    def Back(self):
        print("BACK_TO_LOADING")
        MDApp.get_running_app().root.current = 'Home'


    def set_up(self):
        me = str(self.FM.read_file("SOCKET_DATA/Profile.txt"))
        mi = me.split("@")
        try:
            print("SENDING PROFILE:: ")
            for _ in mi:
                print("P:: ", str(_))
            name = str(mi[0]).translate(str.maketrans('','',string.punctuation))
            icon = str(mi[3]).translate(str.maketrans('','',string.punctuation))
            data = "START@"+name+"@"+icon
            self.FM.write_file("SOCKET_DATA/GAME.txt", data, "w")
            return "SENT"

        except Exception as e:
            print(str(e))



    def Ready(self):
        print("READY..")
        print(str(self.set_up()))
        ready = str(self.FM.read_file("SOCKET_DATA/SERVER.txt"))
        print("READY")
        if "MATCH" in ready:
            print("MATCHED!!")
            if "MATCH1" in ready:
                self.FM.write_file("SOCKET_DATA/Player.txt", "PL1", "w")
            elif "MATCH2" in ready:
                self.FM.write_file("SOCKET_DATA/Player.txt", "PL2", "w")
            MDApp.get_running_app().root.current = "Game"
            return

        else:
            self.ids['Lobby'].text = "WAITING FOR MATCH"
            steady = self.steady()
            if steady == True:
                print("STEADY")
                MDApp.get_running_app().root.current = "Game"
                return


    def steady(self):
        print("...STEADY")
        while True:
            
#            print("WAITING...")
            ready = str(self.FM.read_file("SERVER.txt"))
            if "MATCH" in ready:
                print("MATCHED!")
                if "MATCH1" in ready:
                    self.FM.write_file("SOCKET_DATA/Player.txt", "PL1", "w")
                elif "MATCH2" in ready:
                    self.FM.write_file("SOCKET_DATA/Player.txt", "PL2", "w")
                return True
            else:
                time.sleep(0.0003)
                self.ids['Lobby'].text = "WAITING FOR MATCH"
                pass


class TABS(TabbedPanel):
    pass


class Recycle(ScrollView):
    def __init__(self, **kw):
        super().__init__(**kw)
        pass

    def card(self):
        print("TOUCHED")


class RecycleOne(ScrollView):
    def __init__(self, **kw):
        super().__init__(**kw)
        pass

    def card(self):
        print("TOUCHED")


class RecycleTwo(ScrollView):
    def __init__(self, **kw):
        super().__init__(**kw)
        pass
    def card(self):
        print("TOUCHED")


class Score(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()
        win = str(self.FM.read_file("SOCKET_DATA/game_over.txt"))
        # print("WIN:?0", win)
        self.ids['back'].text = str(win)
        # print("DONE")

    def home(self):
        self.FM.write_file("SOCKET_DATA/GAME.txt", "END", "w")
        time.sleep(5)
        self.FM.write_file("SOCKET_DATA/SERVER.txt", "", "w")
        self.FM.write_file("SOCKET_DATA/GAME.txt", "", "w")
        self.FM.write_file("SOCKET_DATA/game_over.txt", "", "w")
        MDApp.get_running_app().root.current = "Home"

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# HOME_
# ********************************************************


class Home(BoxLayout):
    def __init__(self, **kw):
        super(Home, self).__init__(**kw)
        self.FM = File_man()
        self.sp_cards = ["0","1","2","3"]
        self.ads_bank = ""
        self.ads_count = 0
        self.on_start()

    def test_recyle(self):
        MDApp.get_running_app().root.current = 'Game'

    def on_start(self):
        self.NAME = str(self.FM.read_file("SOCKET_DATA/Profile.txt"))
        name = self.NAME.split("@")
        try:
            user = str(name[1]).translate(str.maketrans('','',string.punctuation))
            icon = str(name[7]).translate(str.maketrans('','',string.punctuation))
            gender = str(name[6]).translate(str.maketrans('','',string.punctuation))


            print("NAME:: ", str(user))
            print("ICON:: ", str(icon))

            Icon = "ASSETS/PlayerIcon/"+str(icon)+str(gender[0])+".png"
            print("IMAGE::: ", str(Icon))

            self.ids['Player'].text = str(user)
            self.ids['Icon_'].source = str(Icon)
        except Exception as e:
            print("PROFILE_ERROR:HOME_SCREEN: ", str(e))

    def move(self):
        MDApp.get_running_app().root.current = 'Lobby'


    #GRAPHIC THINGS

    def store_on(self):
        self.ids.store_image.source = 'ASSETS/Buttons/OffStore.png'

    def store_off(self):
        self.ids.store_image.source = 'ASSETS/Buttons/OnStore.png'
        MDApp.get_running_app().root.current = "Store"

    def PlayG_on(self):
        self.ids.PlayG_image.source = 'ASSETS/Buttons/OffPlayG.png'

    def PlayG_off(self):
        self.ids.PlayG_image.source = 'ASSETS/Buttons/OnPlayG.png'

    def rank_on(self):
        self.ids.rank_image.source = 'ASSETS/Buttons/OffRank.png'

    def rank_off(self):
        self.ids.rank_image.source = 'ASSETS/Buttons/OnRank.png'
        MDApp.get_running_app().root.current = "RankG"

    def settings_on(self):
        self.ids.settings_image.source = 'ASSETS/Buttons/OffSettings.png'

    def settings_off(self):
        self.ids.settings_image.source = 'ASSETS/Buttons/OnSettings.png'
        Settings().open()


class Settings(Popup):
    def __init__(self, **kw):
        super().__init__(**kw)
        pass

    # GRAPHIC THINGS

    def sound_on(self):
        self.ids.Sound_image.source = 'ASSETS/Buttons/OffSound.png'

    def sound_off(self):
        self.ids.Sound_image.source = 'ASSETS/Buttons/OnSound.png'

    def music_on(self):
        self.ids.Music_image.source = 'ASSETS/Buttons/OffSound.png'

    def music_off(self):
        self.ids.Music_image.source = 'ASSETS/Buttons/OnSound.png'

    def report_on(self):
        self.ids.Report_image.source = 'ASSETS/Buttons/OffReport.png'

    def report_off(self):
        self.ids.Report_image.source = 'ASSETS/Buttons/OnReport.png'

    def logout_on(self):
        self.ids.Logout_image.source = 'ASSETS/Buttons/OffLogout.png'

    def logout_off(self):
        self.ids.Logout_image.source = 'ASSETS/Buttons/OnLogout.png'

    def back_on(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OffBack.png'

    def back_off(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OnBack.png'
        MDApp.get_running_app().root.current = "Home"

class Store(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        pass

    def play(self):
        print("PLAYING_ADD")

    # Video go's Here

    # GRAPHIC THINGS

    def back_on(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OffBack.png'

    def back_off(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OnBack.png'
        MDApp.get_running_app().root.current = "Home"

    def play_on(self):
        self.ids.play_image.source = 'ASSETS/Buttons/OffPlay.png'

    def play_off(self):
        self.ids.play_image.source = 'ASSETS/Buttons/OnPlay.png'


class RankG(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        pass

    # GRAPHIC THINGS

    def back_on(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OffBack.png'

    def back_off(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OnBack.png'
        MDApp.get_running_app().root.current = "Home"

    def rankl_on(self):
        self.ids.rankl_image.source = 'ASSETS/Buttons/OffRankL.png'

    def rankl_off(self):
        self.ids.rankl_image.source = 'ASSETS/Buttons/OnRankL.png'
        MDApp.get_running_app().root.current = "RankL"


class RankL(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        pass

    # GRAPHIC THINGS

    def back_on(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OffBack.png'

    def back_off(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OnBack.png'
        MDApp.get_running_app().root.current = "Home"

    def rankg_on(self):
        self.ids.rankg_image.source = 'ASSETS/Buttons/OffRankG.png'

    def rankg_off(self):
        self.ids.rankg_image.source = 'ASSETS/Buttons/OnRankG.png'
        MDApp.get_running_app().root.current = "RankG"


class Register(Popup):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()
        self.gender = ""
        self.selected = False

    def gender_select(self, inst):
        if self.selected is True:
            self.selected = False
            self.ids['Male'].disabled = False
            self.ids['Female'].disabled = False
            return
        if "Male" in inst and self.selected is False:
            self.gender = "Male" 
            print(":SET:ID:icon:", str(self.gender))
            self.ids['Female'].disabled = True
            self.selected = True
            return
        if "Female" in inst and self.selected is False:
            self.gender = "Female" 
            print(":SET:ID:icon:", str(self.gender))
            self.ids['Male'].disabled = True
            self.selected = True
            return

    def name_to_num(self, name):
        print("MONTH_NAME:: ", str(name))
        m_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        for i, m in enumerate(m_names):
            if m == name:
                print("MONTH_NUMBER:: ", str(i+1))
                return int(i+1)

    def select_icon(self, day, month_name):
        month = int(self.name_to_num(month_name))
        try:
            day = int(day)
            month = int(month)
            if day>=21 and month >=3 and month <= 4:
                print("WHAT DA>>?")
#            print(f"\n\n\nVALS --{day}:{month}--", "\n\n*************************************")

            if month >= 3 and month <=4:  # MARCH
                if day <= 19 or day >= 21:  # APRIL
                    return "Aries"
            elif month >=4 and month <=5:  # APRIL
                if  day >= 20 or day <=20:  # MAY
                    return "Taurus"
            elif month >= 5 and month <= 6:  # MAY
                if  day >= 21 or day <= 20:  # JUNE
                    return "Gemini"
            elif month >=6 and month <=7 :  # JUNE
                if day >=21 or day <=22:  # July
                    return "Cancer"
            elif month >= 7 and month <= 8:  # JULY
                if day >= 23 or day <= 22:  # AUGUST
                    return "Leo"
            elif month >=8 and month <=9:  # AUGUST
                if day >= 23 or day <=22:  # SEPTEMBER
                    return "Virgo"
            elif month >=9 and month <= 10:  # SEPTEMBER
                if day >= 23 or day <= 22:  # OCTOBER
                    return "Libra"
            elif month >= 10 and month <= 11:  # OCTOBER
                if day >=23 and day <= 21:  # NOVEMBER
                    return "Scorpio"
            elif month >= 11 and month <= 12:  # NOVEMBER
                if day >= 22 or day <= 21:  # DECEMBER
                    return "Sagittarius"
            elif month >= 12 and month <= 1:  # DECEMBER
                if day >= 20 or day <= 18:  # JANUARY
                    return "Capricorn"
            elif month >= 1 and month <= 2:  # JANUARY
                if day >= 19 or day <= 18:  # FEBRUARY
                    return "Aquarius"
            elif month >= 2 and month <= 3:  # FEBRUARY
                if day >= 19 or day <= 20:  # MARCH
                    return "Pisces"
        except Exception as e:
            print("ICON:SELECTION::ERROR:: ", str(e))

    def Register(self):
        print("REGISTER_ED: NOT_YET_UPDATED")
        name = str(self.ids['Name'].text)+"@"
        print("NAME", str(name))

        day = str(self.ids['Day_Date'].text)
        month = str(self.ids['Month_Date'].text)
        year = str(self.ids['Year_Date'].text)+"@"
        print("DATE:: ", day, ":", month, ":", year)

        Icon = str(self.select_icon(day, month))
        print("ICON MADE:: ", str(Icon))

        Country = str(self.ids['Country'].text)+"@"
        print("COUNTRY:: ", Country)

        Gender = str(self.gender)+"@"
        print("GENDER:: ", Gender)

        E_mail = str(self.ids['input_RegMail'].text)+"@"
        print("EMAIL:: ", str(E_mail))


        player_data = "_REG@"+name+day+"#"+month+"#"+year+Country+E_mail+Gender+Icon
        player_profile = "PROFILE@"+name+day+"#"+month+"#"+year+Country+E_mail+Gender+Icon
        self.FM.write_file("SOCKET_DATA/Player.txt", player_data, "w")
        self.FM.write_file("SOCKET_DATA/Profile.txt", player_profile, "w")
        time.sleep(0.5)
        feddBack = str(self.FM.read_file("SOCKET_DATA/LOGIN.txt"))
        print("FEDBACK:: ", feddBack)
        if "LOGIN" in feddBack:
            MDApp.get_running_app().root.current ="Home"
        if "WELCOME_NEW" in feddBack:
            Login().open()

    # GRAPHIC THINGS

    def back_on(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OffBack.png'

    def back_off(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OnBack.png'

    def submit_on(self):
        self.ids.submit_image.source = 'ASSETS/Buttons/OffSubmit.png'

    def submit_off(self):
        self.ids.submit_image.source = 'ASSETS/Buttons/OnSubmit.png'


class Login(Popup):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()

    def go(self):
        name = str(self.ids['Name'].text)+"@"
        day = str(self.ids['Birth_DAY'].text)
        month = str(self.ids['Birth_MONTH'].text)
        year = str(self.ids['Birth_YEAR'].text)
        country = str(self.ids['Country'].text)

        player_data = "LOGIN@"+name+country
        self.FM.write_file("SOCKET_DATA/Player.txt", player_data, "w")
        time.sleep(0.5)
        feed_back = str(self.FM.read_file("SOCKET_DATA/LOGIN.txt"))
        # print("FEEDBACK:: ", feed_back)
        try:
            if "LOGIN" in feed_back:
                print("LOGIN:SUCCESSFUL")
                Welcome().open()
            if "REGISTER_PLEASE" in feed_back:
                print("PLEASE_REGISTER")
                Register().open()
        except Exception as e:
            print("LOGIN_ERROR:: ", str(e))

    # GRAPHIC THINGS

    def submit_on(self):
        self.ids.submit_image.source = 'ASSETS/Buttons/OffSubmit.png'

    def submit_off(self):
        self.ids.submit_image.source = 'ASSETS/Buttons/OnSubmit.png'

    def register_on(self):
        self.ids.register_image.source = 'ASSETS/Buttons/OffRegister.png'

    def register_off(self):
        self.ids.register_image.source = 'ASSETS/Buttons/OnRegister.png'


class Welcome(Popup):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()
        self.NAME = str(self.FM.read_file("SOCKET_DATA/Profile.txt"))

        name = self.NAME.split("@")

        if len(name) > 1:
            # print("PLAYER_DATA:: ", str(name))
            user = str(name[1]).translate(str.maketrans('', '', string.punctuation))
            # print("NAME:: ", str(user))

            self.ids['WelcomeName'].text = str(user)

        else:
            Login().open()

    def home(self):
        MDApp.get_running_app().root.current = "Home"

    # GRAPHIC THINGS

    def continue_on(self):
        self.ids.continue_image.source = 'ASSETS/Buttons/OffContinue.png'

    def continue_off(self):
        self.ids.continue_image.source = 'ASSETS/Buttons/OnContinue.png'


class Loading(BoxLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()

        try:
            self.conn = connections()
        except sock_error as se:
            print("??CON_ERROR??(MAIN.py)", str(se))
        
        try:
            self.recv = threading.Thread(target=self.conn.get_msg)
            print("STARTING_CONNECTION(s)::RECV")
            self.recv.start()
        except Exception as e:
            print("\n\n!!INIT_CONNECTION_ERROR!!\n\n", str(e))
            raise SystemExit(1)

        try:
            self.send = threading.Thread(target=self.conn.send_msg)
            print("STARTING_CONNECTION(s)::SEND")
            self.send.start()

        except Exception as e:
            print("\n\n!!INIT_CONNECTION_ERROR!!\n\n", str(e))
            raise SystemExit(1)

        self.sec = 0
        Clock.schedule_interval(self.update_time, 1)

    # AUTO_LOGIN
    def just_check(self):
        try:
            self.NAME = str(self.FM.read_file("SOCKET_DATA/Profile.txt"))
            name = self.NAME.split("@")
            if len(name) < 2:
                return False
            if len(name) > 0:
                print("ATTEMPTING_AUTO_LOGIN..")
                print("PLAYER_DATA:: ", str(name))        
                user = str(name[1]).translate(str.maketrans('', '', string.punctuation))
                country = str(name[3]).translate(str.maketrans('', '', string.punctuation))
                player_data = "LOGIN@"+user+country
                self.FM.write_file("SOCKET_DATA/Player.txt", player_data, "w")
                time.sleep(0.5)
                feed_back = str(self.FM.read_file("SOCKET_DATA/LOGIN.txt"))

                try:
                    if "LOGIN" in feed_back:
                        print("LOGIN:SUCCESSFUL")
                        return True
                    if "REGISTER_PLEASE" in feed_back:
                        print("PLEASE_REGISTER")
                        return False
                except Exception as e:
                    print("LOGIN_ERROR:: ", str(e))

        except Exception as E:
            print("AUTO_LOGIN_ERROR: ", str(E))

    def update_time(self, sec):
        print("LOADING... ", str(self.sec))
        self.sec = self.sec + 1
        if self.sec >= 9:  # 9 SEC FOR GIF TO FINISH

            # pl = self.FM.read_file("SOCKET_DATA/Profile.txt")
            # if len(str(pl)) >= 4:
            #                 Welcome().open()
            # else:
            #     Login().open()

            auto_log = self.just_check()
            if auto_log is True:
                Welcome().open()
            else:
                Login().open()

            Clock.unschedule(self.update_time)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# MAIN_
# ********************************************************

class MyMDApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #IMPORT CONTROL
        self.FM = File_man()
        self.FM.write_file("SOCKET_DATA/GAME.txt", "", "w")
        self.FM.write_file("SOCKET_DATA/SERVER.txt", "", "w")
        self.FM.write_file("SOCKET_DATA/ADS_BANK.txt", "", "w")
        self.FM.write_file("SOCKET_DATA/OppData.txt", "", "w")
        self.FM.write_file("SOCKET_DATA/game_over.txt", "", "w")
        self.FM.write_file("SOCKET_DATA/Player.txt", "", "w")
 
    def build(self):
        #REMEMBER TO UPDATE ALL FILES ON STARTUP
        Builder.load_file("main.kv")

        self.screenM = ScreenManager()

        self.SC = Score()#END OF GAME SCREEN
        screen = Screen(name="Score")
        screen.add_widget(self.SC)
        self.screenM.add_widget(screen)

        self.Re = Recycle() #MATCH_SCREEN...
        screen = Screen(name="Recycle")
        screen.add_widget(self.Re)
        self.screenM.add_widget(screen)

        self.G = Game() #MATCH_SCREEN...
        screen = Screen(name="Game")
        screen.add_widget(self.G)
        self.screenM.add_widget(screen)

        self.Lob = Lobby()
        screen = Screen(name="Lobby")
        screen.add_widget(self.Lob)
        self.screenM.add_widget(screen)

        self.AB = Store()
        screen = Screen(name="Store")
        screen.add_widget(self.AB)
        self.screenM.add_widget(screen)

        self.S = Settings()
        screen = Screen(name="Settings")
        screen.add_widget(self.S)
        self.screenM.add_widget(screen)

        self.RG = RankG()
        screen = Screen(name="RankG")
        screen.add_widget(self.RG)
        self.screenM.add_widget(screen)

        self.RL = RankL()
        screen = Screen(name="RankL")
        screen.add_widget(self.RL)
        self.screenM.add_widget(screen)

        self.W = Welcome()
        screen = Screen(name="Welcome")
        screen.add_widget(self.W)
        self.screenM.add_widget(screen)

        self.R = Register()
        screen = Screen(name="Register")
        screen.add_widget(self.R)
        self.screenM.add_widget(screen)

        self.P = Login()
        screen = Screen(name="Login")
        screen.add_widget(self.P)
        self.screenM.add_widget(screen)

        self.H = Home()
        screen = Screen(name="Home")
        screen.add_widget(self.H)
        self.screenM.add_widget(screen)
        
        self.L = Loading()
        screen = Screen(name="Loading")
        screen.add_widget(self.L)
        self.screenM.add_widget(screen)


        self.screenM.current="Loading"

        return self.screenM


if __name__=="__main__":
    M = MyMDApp()
    M.run()
