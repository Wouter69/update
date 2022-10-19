
##ToDo:
    # PROFILE UPDATER ->   {
    #                       LOGIN <<- LOAD FULL PROFILE:: SERVER<<
    #                       WELCOME_POPUP: REFRESH UPDATE
    #                       HOME_SCREEN: REFRESH UPDATE
    #                       RANKED_LIST: CURRENT_LEVEL
    #                       }
    # AUDIO CONTROLS
    # REPORT LOGGING
    # RANKED LISTS ->      {
    #                       USE SAND_BOX_METHOD
    #                       UPDATE: 
    #                           *GLOBAL->(MAKE LIST ON SERVER)  
    #                           *LOCAL ->(CHECK FOR MATCHING COUNTRIES)
    #                       }
    # 
    #       THEN::
    # 
    # LOBBY -> 
    # GAME_SCREEN -> "FUCKTONS_ToDo"


# LIB REQUIRED IMPORTS
from functools import partial
import time
import string
import threading
from socket import error as sock_error


# KIVY IMPORTS
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.audio import SoundLoader
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.scrollview import ScrollView
from kivymd.material_resources import dp
from kivy.uix.image import Image
from kivy import Config

# MY IMPORTS
from file_handle_C import File_man
from conns import connections

# Loading ScreenS.kv Files
Builder.load_file('KivyScreen/Loading.kv')
Builder.load_file('KivyScreen/Home.kv')
Builder.load_file('KivyScreen/Store.kv')
Builder.load_file('KivyScreen/RankG.kv')
Builder.load_file('KivyScreen/RankL.kv')
Builder.load_file('KivyScreen/Lobby.kv')
Builder.load_file('KivyScreen/Game.kv')

# Loading PopupS.kv Files
Builder.load_file('KivyPopup/Welcome.kv')
Builder.load_file('KivyPopup/Login.kv')
Builder.load_file('KivyPopup/Register.kv')
Builder.load_file('KivyPopup/Setting.kv')
Builder.load_file('KivyPopup/Report.kv')
Builder.load_file('KivyPopup/ReportC.kv')

Window.size = (300, 550)

Config.set('graphics', 'resizable', True)

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# POPUPS
# ********************************************************


lobb = False


class ReportC(Popup):
    pass


class Report(Popup):
    pass
    #  SEND DATA TO SERVER TO BE SAVED AND SENT TO ADMIN


class Setting(Popup):
    def __init__(self, **kw):
        super(Setting, self).__init__(**kw)
        self.FM = File_man()

    def open_report(self):
        print("OPEN_REPORT")
        Report().open()
        Setting().dismiss()

    def open_Logout(self):
        print("LOGOUT_BUTTON:: ")
        File_man().write_file("SOCKET_DATA/Profile.txt", "", "*", "w")
        Login().open()
        Setting().dismiss()

    def sound_state_off(self):
        #GET FILE DATA [SETTING.txt]
        #UPDATE
        audio_state = self.FM.read_file("SETTINGS_STATE/SETTINGS.txt", "*")
        for _ in audio_state:
            print(str(_))


        pass

    def sound_state_on(self):
        #GET FILE DATA [SETTING.txt]
        #UPDATE
        pass

    def music_state_off(self):
        #GET FILE DATA [SETTING.txt]
        #UPDATE
        pass

    def music_state_on(self):
        #GET FILE DATA [SETTING.txt]
        #UPDATE
        pass


    # GRAPHIC THINGS
    def on_sound_toggle_button_state(self, widget):
        #WRITE TO SETTINGS FILE AND UPDATE ON ALL SCREENS AND POPUPS
        if widget.state == "normal":
            widget.text = 'on'
            self.sound_state_on()
        else:
            widget.text = 'off'
            self.sound_state_off()

    def on_music_toggle_button_state(self, widget):
        #WRITE TO SETTINGS FILE AND UPDATE ON ALL SCREENS AND POPUPS
        if widget.state == "normal":
            widget.text = 'on'
        else:
            widget.text = 'off'


class Register(Popup):
    def __init__(self, **kw):
        super(Register, self).__init__(**kw)
        self.FM = File_man()
        self.gender = ""
        self.selected = False

    def gender_select(self, inst):
        if self.selected == True:
            self.selected = False
            self.ids['Male'].disabled = False
            self.ids['Female'].disabled = False
            return
        elif "Male" in inst and self.selected == False:
            self.gender = "Male"
            print(":SET:ID:icon:", str(self.gender))
            self.ids['Female'].disabled = True
            self.selected = True
            return
        elif "Female" in inst and self.selected == False:
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
                print("MONTH_NUMBER:: ", str(i + 1))
                return int(i + 1)

    def select_Icon(self, day, month_name):
        month = int(self.name_to_num(month_name))
        try:
            day = int(day)
            month = int(month)
            if 3 <= month <= 4:  # MARCH
                if day <= 19 or day >= 21:  # APRIL
                    return "Aries"
            elif 4 <= month <= 5:  # APRIL
                if day >= 20 or day <= 20:  # MAY
                    return "Taurus"
            elif 5 <= month <= 6:  # MAY
                if day >= 21 or day <= 20:  # JUNE
                    return "Gemini"
            elif 6 <= month <= 7:  # JUNE
                if day >= 21 or day <= 22:  # July
                    return "Cancer"
            elif 7 <= month <= 8:  # JULY
                if day >= 23 or day <= 22:  # AUGUST
                    return "Leo"
            elif 8 <= month <= 9:  # AUGUST
                if day >= 23 or day <= 22:  # SEPTEMBER
                    return "Virgo"
            elif 9 <= month <= 10:  # SEPTEMBER
                if day >= 23 or day <= 22:  # OCTOBER
                    return "Libra"
            elif 10 <= month <= 11:  # OCTOBER
                if day >= 23 and day <= 21:  # NOVEMBER
                    return "Scorpio"
            elif month <= 11 and month <= 12:  # NOVEMBER
                if day >= 22 or day <= 21:  # DECEMBER
                    return "Sagittarius"
            elif 12 <= month <= 1:  # DECEMBER
                if day >= 20 or day <= 18:  # JANUARY
                    return "Capricorn"
            elif 1 <= month <= 2:  # JANUARY
                if day >= 19 or day <= 18:  # FEBUARY
                    return "Aquarius"
            elif 2 <= month <= 3:  # FEBUARY
                if day >= 19 or day <= 20:  # MARCH
                    return "Pisces"
        except Exception as e:
            print("ICON:SELECTION::ERROR:: ", str(e))

    def record_(self):
        
        print("REGISTER_ATTEMPT")
        self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", "", "*", "w")
        print("REGISTER_ED: \n  >>WORKING_CORRECTLY_??")
        name = str(self.ids['Name'].text)
        print("NAME", str(name))

        #DATA_CAPTURE
        day = str(self.ids['Birth_DAY'].text)
        month = str(self.ids['Birth_MONTH'].text)
        year = str(self.ids['Birth_YEAR'].text)
        print("DATE:: ", day, ":", month, ":", year)
        date =  "#"+day+"#"+month+"#"+year+"#"
        icon = str(self.select_Icon(day, month))
        print("ICON MADE:: ", str(icon))
        country = str(self.ids['Country'].text)
        print("COUNTRY:: ", country)
        gender = str(self.gender)
        print("GENDER:: ", gender)
        e_mail = str(self.ids['input_RegMail'].text)
        print("EMAIL:: ", str(e_mail))

        #DATA_ENCAP >> REGISTERATION
        player_data = "REG*"+name+"*"+date+"*"+country+"*"+e_mail+"*"+gender+"*"+icon
        player_profile = "PROFILE*"+name+"*"+date+"*"+country+"*"+e_mail+"*"+gender+"*"+icon
        self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", player_data, "*", "w")
        self.FM.write_file("SOCKET_DATA/Profile.txt", player_profile, "*", "w")
        time.sleep(1)
        feddBack = str(self.FM.read_file("SOCKET_DATA/IN_BOUND.txt", "*"))
        print("FEDBACK:: ", feddBack)
        if "REG_ED" in feddBack:
            Login().open()
            Register().dismiss()
        elif len(feddBack) == 0:
            print("REGISTERATION_TIME_OUT_ERROR")

    def to_login(self):
        Login().open()
        Register().dismiss()


class Login(Popup):
    def __init__(self, **kw):
        super(Login, self).__init__(**kw)
        self.FM = File_man()

    def on_open(self):
        print("LOGIN_POPUP_OPENED")

    def go(self):
        try:
            print("LOGIN_ATTEMPT")
            self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", "", "*", "w")
            name = str(self.ids['Name'].text)
            day = str(self.ids['Birth_DAY'].text)
            month = str(self.ids['Birth_MONTH'].text)
            year = str(self.ids['Birth_YEAR'].text)
            country = str(self.ids['Country'].text)
            date = "#"+day+"#"+month+"#"+year+"#"

            player_data = "LOGIN*"+name+"*"+date+"*"+country
            self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", player_data, "*", "w")
            time.sleep(1)
            feddBack = str(self.FM.read_file("SOCKET_DATA/IN_BOUND.txt", "*"))
        except Exception as G:
            print("LOGIN_GO_ERROR:: ",str(G))

        try:
            if "LOGIN" in feddBack:
                print("LOGIN:SUCCESSFUL")

                Welcome().open()
                Login().dismiss()
                self.dismiss()

            elif "PLEASE_REGISTER" in feddBack:
                print("PLEASE_REGISTER")
                try:
                    Register().open()
                    self.dismiss()
                except Exception as r:
                    print("Reg(PopUp)_[ERROR]: ", str(r))

        except Exception as e:
            print("LOGIN_ERROR:: ", str(e))

    def to_reg(self):
        print("OPENING::REGISTER(POPUP)")
        Register().open()
        self.dismiss()


class Welcome(Popup):
    def __init__(self, **kw):
        super(Welcome, self).__init__(**kw)        
        self.FM = File_man()
    
    def on_open(self):
        Login().dismiss()
        self.NAME = ""
        self.NAME = self.FM.read_file("SOCKET_DATA/Profile.txt", "*")
        if len(self.NAME) > 0:
            user = str(self.NAME[1]).translate(str.maketrans('', '', string.punctuation))
            self.ids['WelcomeName'].text = str(user)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# SCREENS
# ********************************************************


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


class GameScreen(Screen):
    myIcon = ObjectProperty()
    myName = StringProperty()

    oppIcon = ObjectProperty()
    oppName = StringProperty()

    def __init__(self, **kw):
        super(GameScreen, self).__init__(**kw)
        self.FM = File_man()

    #GAME_LOOP:: 
    def on_enter(self):
        print("%%%%%%%%%%%%%%%%%%\n\nG_S:::RESIZING\n")
        Clock.schedule_interval(self.updateAll, 1)

    def updateAll(self, inst):
        #print("UPDATE_ALL..")
        self.profiles()


    # -----------------------------------------------------------
    # Prayer Profiles
    # -----------------------------------------------------------
    
    def profiles(self):
        #MY_PROFILE
        u_data = self.FM.read_file("SOCKET_DATA/Profile.txt", "*")
        #print("ON_OPEN:HOME")
        if len(u_data) > 5:
            #for _ in u_data:
            #    print("U_DATA: ", str(_))
            try:
                self.myName = str(u_data[1])
                icon = str(u_data[6]) + str(u_data[5][0])
                icon_img = "ASSETS/PlayerIcon/"+icon+".png"
                self.myIcon = str(icon_img)
            except Exception as e:
                print("LOADING PLAYER ICON ERROR ::", str(e))
                pass
            pass

        
        #OPP_PROFILE
        opp_data = self.FM.read_file("SOCKET_DATA/OppData.txt", "*")
        if len(opp_data) > 2:
            try:
                self.oppName = str(opp_data[2])
                opp_icon = str(opp_data[3])
                opp_icon_img = "ASSETS/Opponent/"+opp_icon+".png"
                self.oppIcon = str(opp_icon_img)
            except Exception as e:
                print("LOADING PLAYER ICON ERROR ::", str(e))

    # -----------------------------------------------------------
    # Player Turn
    # -----------------------------------------------------------

    def play_turn(self):

        players_turn =  # ends after a move

        if players_turn == True:

            self.ids.Opponent_Unavailable_Icon.opacity = 1
            self.ids.Player_Unavailable_Icon.opacity = 0

            self.ids.Air.disabled = False
            self.ids.Rune.disabled = False
            self.ids.Pocked.disabled = False
            self.ids.Deck_button.disabled = False

        else:

            self.ids.Opponent_Unavailable_Icon.opacity = 0
            self.ids.Player_Unavailable_Icon.opacity = 1

            self.ids.Air.disabled = True
            self.ids.Rune.disabled = True
            self.ids.Pocked.disabled = True
            self.ids.Deck_button.disabled = True

    # -----------------------------------------------------------
    # Deck - to - Hand
    # -----------------------------------------------------------

    def hit_deck(self):
        print("HIT_ME")

    # -----------------------------------------------------------
    # Tree Hand
    # -----------------------------------------------------------

    def ftree1_select(self, widget):
        if widget.state == 'normal':
            self.ids.Select_Background.opacity = 0
            self.ids.FTree1_Image.opacity = 0
        else:
            self.ids.Select_Background.opacity = .75
            self.ids.FTree1_Image.opacity = 1

    def ftree2_select(self, widget):
        if widget.state == 'normal':
            self.ids.Select_Background.opacity = 0
            self.ids.FTree2_Image.opacity = 0
        else:
            self.ids.Select_Background.opacity = .75
            self.ids.FTree2_Image.opacity = 1

    def ftree3_select(self, widget):
        if widget.state == 'normal':
            self.ids.Select_Background.opacity = 0
            self.ids.FTree3_Image.opacity = 0
        else:
            self.ids.Select_Background.opacity = .75
            self.ids.FTree3_Image.opacity = 1

    # Ftree Creation

    def ftree_c_select(self, widget, *args):

        if widget.state == 'normal':
            self.ids.Select_Creation_Card_Button.pos_hint = {'x': 2, 'y': .5}
            self.ids.FTreeC_Select.opacity = 0
            self.ids.Opponent_unavailable.opacity = 0
            self.ids.Pocked.opacity = 1
            self.ids.Rune.opacity = 1

            self.ids.FTree1.disabled = False
            self.ids.FTree2.disabled = False
            self.ids.FTree3.disabled = False
            self.ids.FTreeC.disabled = False
            self.ids.FTreeJ.disabled = False
            self.ids.Rune.disabled = False
            self.ids.Pocked.disabled = False
            self.ids.Deck_button.disabled = False
            self.ids.Player_tokens.disabled = True

        else:
            self.ids.Select_Creation_Card_Button.pos_hint = {'center_x': .5, 'y': .5}
            self.ids.FTreeC_Select.opacity = 1
            self.ids.Pocked.opacity = 0
            self.ids.Rune.opacity = 0

            self.ids.Deck_button.disabled = True



    def select_ftree_creation(self):

        print('FTree Creation')
        self.ids.Select_Creation_Card_Button.pos_hint = {'x': 2, 'y': .5}
        self.ids.FTreeC_Select.opacity = 0
        self.ids.Opponent_unavailable.opacity = 1

        self.ids.FTree1.disabled = True
        self.ids.FTree2.disabled = True
        self.ids.FTree3.disabled = True
        self.ids.FTreeC.disabled = False
        self.ids.FTreeJ.disabled = True
        self.ids.Rune.disabled = True
        self.ids.Pocked.disabled = True
        self.ids.Player_tokens.disabled = False

    # Ftree Joker

    def ftree_j_select(self, widget):

        if widget.state == 'normal':
            self.ids.Select_Jocker_Card_Button.pos_hint = {'x': 2, 'y': .5}
            self.ids.FTreeJ_Select.opacity = 0
            self.ids.Opponent_unavailable.opacity = 0
            self.ids.Pocked.opacity = 1
            self.ids.Rune.opacity = 1

            self.ids.FTree1.disabled = False
            self.ids.FTree2.disabled = False
            self.ids.FTree3.disabled = False
            self.ids.FTreeC.disabled = False
            self.ids.FTreeJ.disabled = False
            self.ids.Rune.disabled = False
            self.ids.Pocked.disabled = False
            self.ids.Deck_button.disabled = False
            self.ids.Player_tokens.disabled = True

        else:
            self.ids.Select_Jocker_Card_Button.pos_hint = {'center_x': .5, 'y': .5}
            self.ids.FTreeJ_Select.opacity = 1
            self.ids.Pocked.opacity = 0
            self.ids.Rune.opacity = 0

            self.ids.Deck_button.disabled = True

    def select_ftree_jocker(self):

        print('FTree Joker')
        self.ids.Select_Jocker_Card_Button.pos_hint = {'x': 2, 'y': .5}
        self.ids.FTreeJ_Select.opacity = 0
        self.ids.Opponent_unavailable.opacity = 1

        self.ids.FTree1.disabled = True
        self.ids.FTree2.disabled = True
        self.ids.FTree3.disabled = True
        self.ids.FTreeC.disabled = True
        self.ids.FTreeJ.disabled = False
        self.ids.Rune.disabled = True
        self.ids.Pocked.disabled = True
        self.ids.Player_tokens.disabled = False

    # -----------------------------------------------------------
    # Rune Hand
    # -----------------------------------------------------------

    # Rune Allgiz

    def ftree_allgiz_select(self, widget):

        if widget.state == 'normal':
            self.ids.Select_Allgiz_Card_Button.pos_hint = {'x': 2, 'y': .5}
            self.ids.FTree_Allgiz_Select.opacity = 0
            self.ids.Opponent_unavailable.opacity = 0
            self.ids.Pocked.opacity = 1
            self.ids.Air.opacity = 1

            self.ids.FTree_Allgiz.disabled = False
            self.ids.FTree_Hargool.disabled = False
            self.ids.FTree_Yharha.disabled = False
            self.ids.Air.disabled = False
            self.ids.Pocked.disabled = False
            self.ids.Deck_button.disabled = False
            self.ids.Player_tokens.disabled = True

        else:
            self.ids.Select_Allgiz_Card_Button.pos_hint = {'center_x': .5, 'y': .5}
            self.ids.FTree_Allgiz_Select.opacity = 1
            self.ids.Pocked.opacity = 0
            self.ids.Air.opacity = 0

            self.ids.Deck_button.disabled = True

    def select_rune_allgiz(self):

        print('Rune Allgiz')
        self.ids.Select_Allgiz_Card_Button.pos_hint = {'x': 2, 'y': .5}
        self.ids.FTree_Allgiz_Select.opacity = 0
        self.ids.Opponent_unavailable.opacity = 1

        self.ids.FTree_Allgiz.disabled = False
        self.ids.FTree_Hargool.disabled = True
        self.ids.FTree_Yharha.disabled = True
        self.ids.Air.disabled = True
        self.ids.Pocked.disabled = True
        self.ids.Player_tokens.disabled = False

    # Rune Hargool

    def ftree_hargool_select(self, widget):

        if widget.state == 'normal':
            self.ids.Select_Hargool_Card_Button.pos_hint = {'x': 2, 'y': .5}
            self.ids.FTree_Hargool_Select.opacity = 0
            self.ids.Player_unavailable.opacity = 0
            self.ids.Pocked.opacity = 1
            self.ids.Air.opacity = 1

            self.ids.FTree_Allgiz.disabled = False
            self.ids.FTree_Hargool.disabled = False
            self.ids.FTree_Yharha.disabled = False
            self.ids.Air.disabled = False
            self.ids.Pocked.disabled = False
            self.ids.Deck_button.disabled = False
            self.ids.Opponent_tokens.disabled = True

        else:
            self.ids.Select_Hargool_Card_Button.pos_hint = {'center_x': .5, 'y': .5}
            self.ids.FTree_Hargool_Select.opacity = 1
            self.ids.Pocked.opacity = 0
            self.ids.Air.opacity = 0

            self.ids.Deck_button.disabled = True

    def select_rune_hargool(self):

        print('Rune Hargool')
        self.ids.Select_Hargool_Card_Button.pos_hint = {'x': 2, 'y': .5}
        self.ids.FTree_Hargool_Select.opacity = 0
        self.ids.Player_unavailable.opacity = 1

        self.ids.FTree_Allgiz.disabled = True
        self.ids.FTree_Hargool.disabled = False
        self.ids.FTree_Yharha.disabled = True
        self.ids.Air.disabled = True
        self.ids.Pocked.disabled = True
        self.ids.Opponent_tokens.disabled = False

    # Rune Yharha

    def ftree_yharha_select(self, widget):

        if widget.state == 'normal':
            self.ids.Select_Yharha_Card_Button.pos_hint = {'x': 2, 'y': .5}
            self.ids.FTree_Yharha_Select.opacity = 0
            self.ids.Player_unavailable.opacity = 0
            self.ids.Pocked.opacity = 1
            self.ids.Air.opacity = 1

            self.ids.FTree_Allgiz.disabled = False
            self.ids.FTree_Hargool.disabled = False
            self.ids.FTree_Yharha.disabled = False
            self.ids.Air.disabled = False
            self.ids.Pocked.disabled = False
            self.ids.Deck_button.disabled = False
            self.ids.Opponent_tokens.disabled = True

        else:
            self.ids.Select_Yharha_Card_Button.pos_hint = {'center_x': .5, 'y': .5}
            self.ids.FTree_Yharha_Select.opacity = 1
            self.ids.Pocked.opacity = 0
            self.ids.Air.opacity = 0

            self.ids.Deck_button.disabled = True

    def select_rune_yharha(self):

        print('Rune Yharha')
        self.ids.Select_Yharha_Card_Button.pos_hint = {'x': 2, 'y': .5}
        self.ids.FTree_Yharha_Select.opacity = 0
        self.ids.Player_unavailable.opacity = 1

        self.ids.FTree_Allgiz.disabled = True
        self.ids.FTree_Hargool.disabled = True
        self.ids.FTree_Yharha.disabled = False
        self.ids.Air.disabled = True
        self.ids.Pocked.disabled = True
        self.ids.Opponent_tokens.disabled = False

    # -----------------------------------------------------------
    # Pocked Hand
    # -----------------------------------------------------------

    # Pocked Allgiz

    def pocked_allgiz_select(self, widget):

        if widget.state == 'normal':
            self.ids.Select_Allgiz_Pocked_Card_Button.pos_hint = {'x': 2, 'y': .5}
            self.ids.Pocked_Allgiz_Select.opacity = 0
            self.ids.Opponent_unavailable.opacity = 0
            self.ids.Rune.opacity = 1
            self.ids.Air.opacity = 1

            self.ids.Pocked_Allgiz.disabled = False
            self.ids.Pocked_Er.disabled = False
            self.ids.Pocked_Fe.disabled = False
            self.ids.Pocked_Hargool.disabled = False
            self.ids.Pocked_Largoo.disabled = False
            self.ids.Pocked_Yharha.disabled = False
            self.ids.Air.disabled = False
            self.ids.Rune.disabled = False
            self.ids.Deck_button.disabled = False
            self.ids.Player_tokens.disabled = True

        else:
            self.ids.Select_Allgiz_Pocked_Card_Button.pos_hint = {'center_x': .5, 'y': .5}
            self.ids.Pocked_Allgiz_Select.opacity = 1
            self.ids.Rune.opacity = 0
            self.ids.Air.opacity = 0

            self.ids.Deck_button.disabled = True

    def select_pocked_allgiz(self):

        print('Pocked Allgiz')
        self.ids.Select_Allgiz_Pocked_Card_Button.pos_hint = {'x': 2, 'y': .5}
        self.ids.Pocked_Allgiz_Select.opacity = 0
        self.ids.Opponent_unavailable.opacity = 1

        self.ids.Pocked_Allgiz.disabled = False
        self.ids.Pocked_Er.disabled = True
        self.ids.Pocked_Fe.disabled = True
        self.ids.Pocked_Hargool.disabled = True
        self.ids.Pocked_Largoo.disabled = True
        self.ids.Pocked_Yharha.disabled = True
        self.ids.Air.disabled = True
        self.ids.Rune.disabled = True
        self.ids.Player_tokens.disabled = False

    # Pocked Er

    def pocked_er_select(self, widget):

        if widget.state == 'normal':
            self.ids.Select_Er_Pocked_Card_Button.pos_hint = {'x': 2, 'y': .5}
            self.ids.Pocked_Er_Select.opacity = 0
            self.ids.Opponent_unavailable.opacity = 0
            self.ids.Rune.opacity = 1
            self.ids.Air.opacity = 1

            self.ids.Pocked_Allgiz.disabled = False
            self.ids.Pocked_Er.disabled = False
            self.ids.Pocked_Fe.disabled = False
            self.ids.Pocked_Hargool.disabled = False
            self.ids.Pocked_Largoo.disabled = False
            self.ids.Pocked_Yharha.disabled = False
            self.ids.Air.disabled = False
            self.ids.Rune.disabled = False
            self.ids.Deck_button.disabled = False
            self.ids.Player_tokens.disabled = True

        else:
            self.ids.Select_Er_Pocked_Card_Button.pos_hint = {'center_x': .5, 'y': .5}
            self.ids.Pocked_Er_Select.opacity = 1
            self.ids.Rune.opacity = 0
            self.ids.Air.opacity = 0

            self.ids.Deck_button.disabled = True

    def select_pocked_er(self):

        print('Pocked Er')
        self.ids.Select_Er_Pocked_Card_Button.pos_hint = {'x': 2, 'y': .5}
        self.ids.Pocked_Er_Select.opacity = 0
        self.ids.Opponent_unavailable.opacity = 1

        self.ids.Pocked_Allgiz.disabled = True
        self.ids.Pocked_Er.disabled = False
        self.ids.Pocked_Fe.disabled = True
        self.ids.Pocked_Hargool.disabled = True
        self.ids.Pocked_Largoo.disabled = True
        self.ids.Pocked_Yharha.disabled = True
        self.ids.Air.disabled = True
        self.ids.Rune.disabled = True
        self.ids.Player_tokens.disabled = False

    # Pocked Fe

    def pocked_fe_select(self, widget):

        if widget.state == 'normal':
            self.ids.Select_Pocked_Fe_Card_Button.pos_hint = {'x': 2, 'y': .5}
            self.ids.Pocked_Fe_Select.opacity = 0
            self.ids.Player_unavailable.opacity = 0
            self.ids.Rune.opacity = 1
            self.ids.Air.opacity = 1

            self.ids.Pocked_Allgiz.disabled = False
            self.ids.Pocked_Er.disabled = False
            self.ids.Pocked_Fe.disabled = False
            self.ids.Pocked_Hargool.disabled = False
            self.ids.Pocked_Largoo.disabled = False
            self.ids.Pocked_Yharha.disabled = False
            self.ids.Air.disabled = False
            self.ids.Rune.disabled = False
            self.ids.Deck_button.disabled = False
            self.ids.Opponent_tokens.disabled = True

        else:
            self.ids.Select_Pocked_Fe_Card_Button.pos_hint = {'center_x': .5, 'y': .5}
            self.ids.Pocked_Fe_Select.opacity = 1
            self.ids.Rune.opacity = 0
            self.ids.Air.opacity = 0

            self.ids.Deck_button.disabled = True

    def select_pocked_fe(self):

        print('Pocked Fe')
        self.ids.Select_Pocked_Fe_Card_Button.pos_hint = {'x': 2, 'y': .5}
        self.ids.Pocked_Fe_Select.opacity = 0
        self.ids.Player_unavailable.opacity = 1

        self.ids.Pocked_Allgiz.disabled = True
        self.ids.Pocked_Er.disabled = True
        self.ids.Pocked_Fe.disabled = False
        self.ids.Pocked_Hargool.disabled = True
        self.ids.Pocked_Largoo.disabled = True
        self.ids.Pocked_Yharha.disabled = True
        self.ids.Air.disabled = True
        self.ids.Rune.disabled = True
        self.ids.Opponent_tokens.disabled = False

    # Pocked Hargool

    def pocked_hargool_select(self, widget):

        if widget.state == 'normal':
            self.ids.Select_Pocked_Hargool_Card_Button.pos_hint = {'x': 2, 'y': .5}
            self.ids.Pocked_Hargool_Select.opacity = 0
            self.ids.Player_unavailable.opacity = 0
            self.ids.Rune.opacity = 1
            self.ids.Air.opacity = 1

            self.ids.Pocked_Allgiz.disabled = False
            self.ids.Pocked_Er.disabled = False
            self.ids.Pocked_Fe.disabled = False
            self.ids.Pocked_Hargool.disabled = False
            self.ids.Pocked_Largoo.disabled = False
            self.ids.Pocked_Yharha.disabled = False
            self.ids.Air.disabled = False
            self.ids.Rune.disabled = False
            self.ids.Deck_button.disabled = False
            self.ids.Opponent_tokens.disabled = True

        else:
            self.ids.Select_Pocked_Hargool_Card_Button.pos_hint = {'center_x': .5, 'y': .5}
            self.ids.Pocked_Hargool_Select.opacity = 1
            self.ids.Rune.opacity = 0
            self.ids.Air.opacity = 0

            self.ids.Deck_button.disabled = True

    def select_pocked_hargool(self):

        print('Pocked Hargool')
        self.ids.Select_Pocked_Hargool_Card_Button.pos_hint = {'x': 2, 'y': .5}
        self.ids.Pocked_Hargool_Select.opacity = 0
        self.ids.Player_unavailable.opacity = 1

        self.ids.Pocked_Allgiz.disabled = True
        self.ids.Pocked_Er.disabled = True
        self.ids.Pocked_Fe.disabled = True
        self.ids.Pocked_Hargool.disabled = False
        self.ids.Pocked_Largoo.disabled = True
        self.ids.Pocked_Yharha.disabled = True
        self.ids.Air.disabled = True
        self.ids.Rune.disabled = True
        self.ids.Opponent_tokens.disabled = False

    # Pocked Largoo

    def pocked_largoo_select(self, widget):

        if widget.state == 'normal':
            self.ids.Select_Pocked_Largoo_Card_Button.pos_hint = {'x': 2, 'y': .5}
            self.ids.Pocked_Largoo_Select.opacity = 0
            self.ids.Opponent_unavailable.opacity = 0
            self.ids.Rune.opacity = 1
            self.ids.Air.opacity = 1

            self.ids.Pocked_Allgiz.disabled = False
            self.ids.Pocked_Er.disabled = False
            self.ids.Pocked_Fe.disabled = False
            self.ids.Pocked_Hargool.disabled = False
            self.ids.Pocked_Largoo.disabled = False
            self.ids.Pocked_Yharha.disabled = False
            self.ids.Air.disabled = False
            self.ids.Rune.disabled = False
            self.ids.Deck_button.disabled = False
            self.ids.Player_tokens.disabled = True

        else:
            self.ids.Select_Pocked_Largoo_Card_Button.pos_hint = {'center_x': .5, 'y': .5}
            self.ids.Pocked_Largoo_Select.opacity = 1
            self.ids.Rune.opacity = 0
            self.ids.Air.opacity = 0

            self.ids.Deck_button.disabled = True

    def select_pocked_largoo(self):

        print('Pocked Largoo')
        self.ids.Select_Pocked_Largoo_Card_Button.pos_hint = {'x': 2, 'y': .5}
        self.ids.Pocked_Largoo_Select.opacity = 0
        self.ids.Opponent_unavailable.opacity = 1

        self.ids.Pocked_Allgiz.disabled = True
        self.ids.Pocked_Er.disabled = True
        self.ids.Pocked_Fe.disabled = True
        self.ids.Pocked_Hargool.disabled = True
        self.ids.Pocked_Largoo.disabled = False
        self.ids.Pocked_Yharha.disabled = True
        self.ids.Air.disabled = True
        self.ids.Rune.disabled = True
        self.ids.Player_tokens.disabled = False

    # Pocked Yharha

    def pocked_yharha_select(self, widget):

        if widget.state == 'normal':
            self.ids.Select_Pocked_Yharha_Card_Button.pos_hint = {'x': 2, 'y': .5}
            self.ids.Pocked_Yharha_Select.opacity = 0
            self.ids.Player_unavailable.opacity = 0
            self.ids.Rune.opacity = 1
            self.ids.Air.opacity = 1

            self.ids.Pocked_Allgiz.disabled = False
            self.ids.Pocked_Er.disabled = False
            self.ids.Pocked_Fe.disabled = False
            self.ids.Pocked_Hargool.disabled = False
            self.ids.Pocked_Largoo.disabled = False
            self.ids.Pocked_Yharha.disabled = False
            self.ids.Air.disabled = False
            self.ids.Rune.disabled = False
            self.ids.Deck_button.disabled = False
            self.ids.Opponent_tokens.disabled = True

        else:
            self.ids.Select_Pocked_Yharha_Card_Button.pos_hint = {'center_x': .5, 'y': .5}
            self.ids.Pocked_Yharha_Select.opacity = 1
            self.ids.Rune.opacity = 0
            self.ids.Air.opacity = 0

            self.ids.Deck_button.disabled = True

    def select_pocked_yharha(self):

        print('Pocked Yharha')
        self.ids.Select_Pocked_Yharha_Card_Button.pos_hint = {'x': 2, 'y': .5}
        self.ids.Pocked_Yharha_Select.opacity = 0
        self.ids.Player_unavailable.opacity = 1

        self.ids.Pocked_Allgiz.disabled = True
        self.ids.Pocked_Er.disabled = True
        self.ids.Pocked_Fe.disabled = True
        self.ids.Pocked_Hargool.disabled = True
        self.ids.Pocked_Largoo.disabled = True
        self.ids.Pocked_Yharha.disabled = False
        self.ids.Air.disabled = True
        self.ids.Rune.disabled = True
        self.ids.Opponent_tokens.disabled = False


class LobbyScreen(Screen):
    myIcon = ObjectProperty()
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()
        self.matched = False


    def on_enter(self):
        print("OPENING_LOBBY")
        try:
            self.profile()
        except Exception as e:
            print("PRO_FILE_LOADING ERROR:: ", str(e))

        ret_val = self.Ready()
        if ret_val == True:
            MDApp.get_running_app().root.current = 'game'
            print("OPENING_GAME_SCREEN")            
        else:
            print("FODIS")

    def profile(self):
        u_data = self.FM.read_file("SOCKET_DATA/Profile.txt", "*")
        if len(u_data) > 5:
            try:
                icon = str(u_data[6]) + str(u_data[5][0])
                icon_img = "ASSETS/PlayerIcon/"+icon+".png"
                self.myIcon = str(icon_img)
            except Exception as e:
                print("LOADING PLAYER ICON ERROR:: ", str(e))



    def Ready(self):
        print("READY..")
        while self.matched != True:
            ready = self.FM.read_file("SOCKET_DATA/GAME.txt", "*")
            if ready:
                print("R:: ", str(ready[0]))
                print("READY")
                if "MATCH" in str(ready[0]):
                    print("MATCHED!!")
                    if "MATCH1" in str(ready[0]):
                        self.FM.write_file("SOCKET_DATA/Player.txt", "PL1", "*", "w")
                        print("PLAYER_1")
                    elif "MATCH2" in str(ready[0]):
                        print("PLAYER_2")
                        self.FM.write_file("SOCKET_DATA/Player.txt", "PL2", "*", "w")
                    time.sleep(0.5)
                    self.matched = True
                    return True
                else:
                    pass

    def back_on(self):
        print("CANCELLED_LOBBY")
        MDApp.get_running_app().root.current = 'home'

    def back_off(self):
        print("BACK_TO_HOME")

class RankLScreen(Screen):
    user_name = StringProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        pro_data = File_man().read_file("SOCKET_DATA/Profile.txt", "*")
        if len(pro_data) > 2:
            self.user_name = str(pro_data[1])
    
    def rankg_on(self):
        print("RANKG_ON")

    def rankg_off(self):
        print("RANKG_OFF")
    
    def back_on(self):
        print("back_on")

    def back_off(self):
        print("back_off")

class RankGScreen(Screen):
    user_name = StringProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        pro_data = File_man().read_file("SOCKET_DATA/Profile.txt", "*")
        if len(pro_data) > 2:
            self.user_name = str(pro_data[1])

    def rankl_on(self):
        print("RANKl_ON")

    def rankl_off(self):
        print("RANKl_OFF")    

    def back_on(self):
        print("back_on")

    def back_off(self):
        print("back_off")

class StoreScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        pass

    def play_on(self):
        print("PLAYING_ADD")

    def play_off(self):
        pass

    def back_on(self):
        print("back_on")

    def back_off(self):
        print("back_off")

class HomeScreen(Screen):
    my_name = StringProperty()
    my_icon = ObjectProperty()

    def __init__(self, **kw):
        super(HomeScreen, self).__init__(**kw)
        self.FM = File_man()
        self.sp_cards = ["0","1","2","3"]
        self.ads_bank = ""
        self.ads_count = 0
        self.init_user = self.FM.read_file("SOCKET_DATA/Profile.txt", "*")

    def store_off(self):
        print("STORE")

    def on_enter(self):
        print("IDS:?|", str(self.ids))
        u_data = self.FM.read_file("SOCKET_DATA/Profile.txt", "*")
        print("ON_OPEN:HOME")
        if u_data:
            for _ in u_data:
                print("U_DATA: ", str(_))
            try:
                self.my_name = str(u_data[1])
                icon = str(u_data[6]) + str(u_data[5][0])
                icon_img = "ASSETS/PlayerIcon/"+icon+".png"
                self.my_icon = str(icon_img)
            except Exception as e:
                print("LOADING PLAYER ICON ERROR ::", str(e))

    def rank_on(self):
        print("RANK_ON")

    def rank_off(self):
        print("RANK_OFF")

    def button_sound(self):
        sound = SoundLoader.load('Sound/Button.wav')
        sound.volume = .1
        if sound:
            sound.play()

    def popup_sound(self):
        sound = SoundLoader.load('Sound/Button.wav')
        sound.volume = .1
        if sound:
            sound.play()

    def open_settings(self):
        Setting().open()

    def test_recyle(self):
        MDApp.get_running_app().root.current = 'Game'

    def on_start(self):
        try:
            name = []
            self.NAME = self.FM.read_file("SOCKET_DATA/Profile.txt", "*")

            if len(self.NAME) == 0:
                print("PLAYER_NOT_YET_LOADED")
                pass
            print("SELF.NAME::: ", str(self.NAME))
            name = self.NAME.split("*")
            print("name::: ", str(name))
            if len(self.NAME) >= 6:
                user = str(name[1]).translate(str.maketrans('','',string.punctuation))
                icon = str(name[6]).translate(str.maketrans('','',string.punctuation))
                gender = str(name[5]).translate(str.maketrans('','',string.punctuation))

                print("NAME:: ", str(user))
                print("ICON:: ", str(icon))

                icon = "ASSETS/PlayerIcon/"+str(icon)+str(gender[0])+".png"
                print("IMAGE::: ", str(icon))

                self.ids['Player_'].text = str(user)
                self.ids['Icon_'].source = str(icon)
            else:
                print("PLAYER_NOT_YET_LOADED")

        except Exception as e:
            print("PROFILE_ERROR:HOME_SCREEN: ", str(e))

    def move(self):
        MDApp.get_running_app().root.current = 'Lobby'

    def playg_on(self):
        print("READY__")
        name = str(self.init_user[1])
        gend = str(self.init_user[5])
        icon = str(self.init_user[6])
        sending = "LOBBY*"+name+"*"+str(gend[0])+icon+"*"
        self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", sending, "*", "w")
        MDApp.get_running_app().root.current = 'lobby'

    def playg_off(self):
        print("READY__??")

class LoadingScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.FM = File_man()
        print("LOADING_SCREEN::")

        self.AUTO_LOG = False
        self.sec = 0
        Clock.schedule_interval(self.update_time, 1)


    # AUTO_LOGIN
    def Just_Check(self):
        try:
            self.USER = self.FM.read_file("SOCKET_DATA/Profile.txt","*")
            user_data = self.USER
            if len(user_data) < 2:
                print("NO_PROFILE_DATA_SAVED")
                return False
            if len(user_data) > 0:
                print("ATTEMPTING_AUTO_LOGIN..")
                print("PLAYER_DATA:: ", str(user_data))
                user = str(user_data[1]).translate(str.maketrans('', '', string.punctuation))
                date = str(user_data[2]).translate(str.maketrans('', '', string.punctuation))
                country = str(user_data[3]).translate(str.maketrans('', '', string.punctuation))
                player_data = "LOGIN*"+user+"*"+date+"*"+country+"*"
                self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", player_data, "*", "w")
                time.sleep(0.5)
                feddBack = str(self.FM.read_file("SOCKET_DATA/IN_BOUND.txt", "*"))

                try:
                    if "LOGIN" in feddBack:
                        print("LOGIN:SUCCESSFUL")
                        return True
                    elif "REGISTER_PLEASE" in feddBack:
                        print("PLEASE_REGISTER")
                        return False
                    else:
                        print("NOT_LOGGED_IN:: ")
                        return False
                except Exception as e:
                    print("LOGIN_ERROR:: ", str(e))

        except Exception as E:
            print("AUTO_LOGIN_ERROR: ", str(E))

    def update_time(self, sec):
        print("LOADING... ", str(self.sec))
        self.sec = self.sec + 1

        if self.sec >= 8 and self.AUTO_LOG == False:  # 8 SEC FOR GIF TO FINISH
            auto_log = self.Just_Check()
            if auto_log == True:
                MDApp.get_running_app().root.current = 'home'
                print("OPENING_[home]...")
                self.AUTO_LOG = True
                Welcome().open()
                Clock.unschedule(self.update_time)
            elif auto_log == False:
                MDApp.get_running_app().root.current = 'home'
                L = Login()
                L.open()
                Clock.unschedule(self.update_time)
    
        elif self.sec >=8:# and self.AUTO_LOG == True:
            print("AUTO_LOGGIN_FAILED")
            #self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", "ONLINE", "w")
            MDApp.get_running_app().root.current = 'home'
            try:
                L = Login()
                L.open()
                Clock.unschedule(self.update_time)
            except Exception as L:
                print("POPUP_ERROR:: ", str(L))


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# MAIN
# ********************************************************


class WindowManager(ScreenManager):
    pass


class MyMDApp(MDApp):
    def __init__(self, **kwargs):
        super(MyMDApp, self).__init__(**kwargs)
        # IMPORT CONTROL
        self.FM = File_man()
        self.conn = connections()

        #CLEAR FILES
        self.FM.write_file("SOCKET_DATA/GAME.txt", "", "*", "w")
        self.FM.write_file("SOCKET_DATA/DECK.txt", "", "*", "w")
        self.FM.write_file("SOCKET_DATA/game_over.txt", "", "*", "w")
        self.FM.write_file("SOCKET_DATA/Player.txt", "", "*", "w")

        self.FM.write_file("SOCKET_DATA/SERVER.txt", "", "*", "w")
        self.FM.write_file("SOCKET_DATA/ADS_BANK.txt", "", "*", "w")
        self.FM.write_file("SOCKET_DATA/OppData.txt", "", "*", "w")
        self.FM.write_file("SOCKET_DATA/OUT_BOUND.txt", "", "*", "w")
        self.FM.write_file("SOCKET_DATA/IN_BOUND.txt", "", "*", "w")

        #OPEN CONNS
        self.connections__()


    def connections__(self):
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


        #self.sound_home = SoundLoader.load('Sound/HomeMusic.wav')
        #self.sound_home.volume = .1

    def build(self):
        Builder.load_file("NoS.kv")

        #if self.sound_home:
        #   self.sound_home.play()

        return WindowManager()


if __name__ == "__main__":
    M = MyMDApp()
    M.run()
