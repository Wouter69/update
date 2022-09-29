
# ---------------------------------------------------------------
# Import
# ---------------------------------------------------------------

from kivy import Config
from kivy.app import App
# from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
# from kivy.graphics import Canvas
# from kivy.uix.anchorlayout import AnchorLayout
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
# from kivy.uix.widget import Widget
# from kivy.uix.textinput import TextInput
# from kivy.uix.label import Label
# from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.tabbedpanel import TabbedPanel


# ---------------------------------------------------------------
# Loading .kv
# ---------------------------------------------------------------

# Loading Screen.kv Files
Builder.load_file('kivyScreen/Game.kv')
Builder.load_file('KivyScreen/Loading.kv')
Builder.load_file('KivyScreen/Home.kv')
Builder.load_file('KivyScreen/Store.kv')
Builder.load_file('KivyScreen/RankG.kv')
Builder.load_file('KivyScreen/RankL.kv')
Builder.load_file('KivyScreen/Lobby.kv')

# Loading Popup.kv Files
Builder.load_file('KivyPopup/Welcome.kv')
Builder.load_file('KivyPopup/Login.kv')
Builder.load_file('KivyPopup/Register.kv')
Builder.load_file('KivyPopup/Setting.kv')
Builder.load_file('KivyPopup/Logout.kv')
Builder.load_file('KivyPopup/Report.kv')
Builder.load_file('KivyPopup/ReportC.kv')

Window.size = (300, 550)


# ---------------------------------------------------------------
# Screens
# ---------------------------------------------------------------

Config.set('graphics', 'resizable', True)


class GameScreen(Screen):
    pass


class LobbyScreen(Screen):

    def back_on(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OffBack.png'

    def back_off(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OnBack.png'


class RankLScreen(Screen):

    def back_on(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OffBack.png'

    def back_off(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OnBack.png'

    def rankg_on(self):
        self.ids.RankG_image.source = 'ASSETS/Buttons/OffRankG.png'

    def rankg_off(self):
        self.ids.RankG_image.source = 'ASSETS/Buttons/OnRankG.png'


class RankGScreen(Screen):

    def back_on(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OffBack.png'

    def back_off(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OnBack.png'

    def rankl_on(self):
        self.ids.RankL_image.source = 'ASSETS/Buttons/OffRankL.png'

    def rankl_off(self):
        self.ids.RankL_image.source = 'ASSETS/Buttons/OnRankL.png'


class StoreScreen(Screen):

    def back_on(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OffBack.png'

    def back_off(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OnBack.png'

    def play_on(self):
        self.ids.play_image.source = 'ASSETS/Buttons/OffPlay.png'

    def play_off(self):
        self.ids.play_image.source = 'ASSETS/Buttons/OnPlay.png'


class HomeScreen(Screen):

    def button_sound(self):
        sound = SoundLoader.load('Sound/Button.wav')
        sound.volume = .1
        if sound:
            sound.play()

    def popup_sound(self):
        sound = SoundLoader.load('Sound/Popup.wav')
        sound.volume = .1
        if sound:
            sound.play()

    def store_on(self):
        self.ids.store_image.source = 'ASSETS/Buttons/OffStore.png'

    def store_off(self):
        self.ids.store_image.source = 'ASSETS/Buttons/OnStore.png'

    def playg_on(self):
        self.ids.PlayG_image.source = 'ASSETS/Buttons/OffPlayG.png'

    def playg_off(self):
        self.ids.PlayG_image.source = 'ASSETS/Buttons/OnPlayG.png'

    def rank_on(self):
        self.ids.rank_image.source = 'ASSETS/Buttons/OffRank.png'

    def rank_off(self):
        self.ids.rank_image.source = 'ASSETS/Buttons/OnRank.png'

    def settings_on(self):
        self.ids.settings_image.source = 'ASSETS/Buttons/OffSettings.png'

    def settings_off(self):
        self.ids.settings_image.source = 'ASSETS/Buttons/OnSettings.png'


class LoadingScreen(Screen):
    pass


# ---------------------------------------------------------------
# Popups
# ---------------------------------------------------------------


class Logout(Popup):

    def logout_on(self):
        self.ids.logout_image.source = 'ASSETS/Buttons/OffLogout.png'

    def logout_off(self):
        self.ids.logout_image.source = 'ASSETS/Buttons/OnLogout.png'

    def back_on(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OffBack.png'

    def back_off(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OnBack.png'


class ReportC(Popup):

    def back_on(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OffBack.png'

    def back_off(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OnBack.png'


class Report(Popup):

    def submit_on(self):
        self.ids.submit_image.source = 'ASSETS/Buttons/OffSubmit.png'

    def submit_off(self):
        self.ids.submit_image.source = 'ASSETS/Buttons/OnSubmit.png'

    def back_on(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OffBack.png'

    def back_off(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OnBack.png'


class Setting(Popup):

    def on_sound_toggle_button_state(self, widget):
        if widget.state == "normal":
            widget.text = 'on'
        else:
            widget.text = 'off'

    def on_music_toggle_button_state(self, widget):
        if widget.state == "normal":
            widget.text = 'on'
        else:
            widget.text = 'off'

    def report_on(self):
        self.ids.report_image.source = 'ASSETS/Buttons/OffReport.png'


    def report_off(self):
        self.ids.report_image.source = 'ASSETS/Buttons/OnReport.png'

    def logout_on(self):
        self.ids.logout_image.source = 'ASSETS/Buttons/OffLogout.png'


    def logout_off(self):
        self.ids.logout_image.source = 'ASSETS/Buttons/OnLogout.png'


    def back_on(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OffBack.png'


    def back_off(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OnBack.png'


class Welcome(Popup):
    pass


class Register(Popup):

    def submit_on(self):
        self.ids.submit_image.source = 'ASSETS/Buttons/OffSubmit.png'

    def submit_off(self):
        self.ids.submit_image.source = 'ASSETS/Buttons/OnSubmit.png'

    def back_on(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OffBack.png'

    def back_off(self):
        self.ids.back_image.source = 'ASSETS/Buttons/OnBack.png'


class Login(Popup):
    pass


# ---------------------------------------------------------------
# Main
# ---------------------------------------------------------------


class WindowManager(ScreenManager):
    pass


class NoSApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.sound_home = SoundLoader.load('Sound/HomeMusic.wav')
        self.sound_home.volume = .1

    def build(self):
        if self.sound_home:
            self.sound_home.play()

        return WindowManager()


NoSApp().run()
