from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button as KivyButton
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
import time

from settings import *
from button import Button  # kept for compatibility if you convert it later

class GameOverScene(Screen):
    def __init__(self, score=0, highscore=0, counter=0, **kwargs):
        super().__init__(**kwargs)
        self.score = score
        self.highscore = highscore
        self.counter = counter
        self.next_scene = None

        # Update and save highscore if needed
        try:
            if self.score > self.highscore:
                self.highscore = self.score
                c, _, a, lt, tt, s = load_save_data()
                save_save_data(c, self.highscore, a, lt, tt, s)
        except Exception:
            pass

        # Layout
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        win_w, win_h = Window.size

        # Title label
        self.title_label = Label(text="GAME OVER", font_size=dp(40), size_hint=(None,None),
                                 pos=(win_w/2 - dp(150), win_h - dp(160)))
        self.layout.add_widget(self.title_label)

        # Score / Highscore / Counter labels
        self.score_label = Label(text=f"Score: {self.score}", font_size=dp(20), size_hint=(None,None),
                                 pos=(win_w/2 - dp(100), win_h - dp(260)))
        self.hs_label = Label(text=f"Highscore: {self.highscore}", font_size=dp(20), size_hint=(None,None),
                              pos=(win_w/2 - dp(100), win_h - dp(300)))
        self.counter_label = Label(text=f"Puffs: {self.counter}", font_size=dp(20), size_hint=(None,None),
                                   pos=(win_w/2 - dp(100), win_h - dp(340)))
        self.layout.add_widget(self.score_label)
        self.layout.add_widget(self.hs_label)
        self.layout.add_widget(self.counter_label)

        # Buttons
        btn_w, btn_h = dp(300), dp(80)
        btn_x = win_w/2 - btn_w/2
        retry_y = win_h/2 - dp(20)
        back_y = retry_y - dp(110)

        self.retry_button = KivyButton(text="Nochmal", size_hint=(None,None), size=(btn_w, btn_h), pos=(btn_x, retry_y))
        self.back_button = KivyButton(text="Zurück", size_hint=(None,None), size=(btn_w, btn_h), pos=(btn_x, back_y))
        self.retry_button.bind(on_release=self._on_retry)
        self.back_button.bind(on_release=self._on_back)
        self.layout.add_widget(self.retry_button)
        self.layout.add_widget(self.back_button)

        # Keep labels updated if somebody changes values; schedule small tick
        Clock.schedule_interval(self._tick, 1.0 / (FPS if 'FPS' in globals() else 60))

    def _on_retry(self, *args):
        self.next_scene = "game_scene"

    def _on_back(self, *args):
        self.next_scene = "counter_screen"

    def _tick(self, dt):
        # update displayed texts in case values changed
        self.score_label.text = f"Score: {self.score}"
        self.hs_label.text = f"Highscore: {self.highscore}"
        self.counter_label.text = f"Puffs: {self.counter}"

    # Compatibility with main.py expecting update() and draw() methods
    def update(self, dt=None):
        return

    def draw(self, screen=None):
        return

