from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button as KivyButton
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window

from settings import *
from button import Button  # kept for compatibility if converted later

class ShopScene(Screen):
    def __init__(self, counter=0, **kwargs):
        super().__init__(**kwargs)
        self.counter = counter
        self.next_scene = None

        # Load saved data
        try:
            _, self.highscore, adblock, self.last_ts, self.total_time, self.sessions = load_save_data()
            self.adblock_purchased = bool(adblock)
        except Exception:
            self.highscore = 0
            self.adblock_purchased = False
            self.last_ts = 0
            self.total_time = 0
            self.sessions = 0

        self.adblock_cost = 420000

        # Layout
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        win_w, win_h = Window.size

        # Title and counter labels
        self.title_label = Label(text="Shop", font_size=dp(36), size_hint=(None,None),
                                 pos=(win_w/2 - dp(60), win_h - dp(120)))
        self.counter_label = Label(text=f"Dein Counter: {self.counter}", font_size=dp(18), size_hint=(None,None),
                                   pos=(dp(20), win_h - dp(40)))
        self.layout.add_widget(self.title_label)
        self.layout.add_widget(self.counter_label)

        # Buy button
        btn_w, btn_h = dp(400), dp(100)
        btn_x = win_w/2 - btn_w/2
        buy_y = win_h/2 - dp(50)
        buy_text = "AdBlock kaufen (420k)" if not self.adblock_purchased else "Bereits gekauft!"
        buy_bg = (0,1,0,1) if not self.adblock_purchased else (0.5,0.5,0.5,1)
        self.buy_button = KivyButton(text=buy_text, size_hint=(None,None), size=(btn_w, btn_h), pos=(btn_x, buy_y))
        self.buy_button.background_color = buy_bg
        self.buy_button.bind(on_release=self._on_buy)
        self.layout.add_widget(self.buy_button)

        # Back button
        back_y = win_h/2 + dp(150)
        self.back_button = KivyButton(text="Zurück", size_hint=(None,None), size=(btn_w, btn_h), pos=(btn_x, back_y))
        self.back_button.bind(on_release=self._on_back)
        self.layout.add_widget(self.back_button)

        # Message label
        self.message = ""
        self.message_timer = 0
        self.message_label = Label(text="", font_size=dp(18), size_hint=(None,None),
                                   pos=(win_w/2 - dp(200), win_h/2 + dp(50)))
        self.layout.add_widget(self.message_label)

        Clock.schedule_interval(self._tick, 1.0 / (FPS if 'FPS' in globals() else 60))

    def _on_buy(self, *args):
        if not self.adblock_purchased:
            if self.counter >= self.adblock_cost:
                self.counter -= self.adblock_cost
                self.adblock_purchased = True
                self.message = "AdBlock gekauft! Keine Werbung mehr... oder so ;)"
                self.message_timer = 180  # ticks (approx 3s at 60fps)
                try:
                    save_save_data(self.counter, self.highscore, 1, self.last_ts, self.total_time, self.sessions)
                except Exception:
                    pass
                # update button state
                self.buy_button.text = "Bereits gekauft!"
                self.buy_button.background_color = (0.5,0.5,0.5,1)
            else:
                self.message = "Nicht genug Puffs! Spiel mehr Minigame!"
                self.message_timer = 180

    def _on_back(self, *args):
        try:
            save_save_data(self.counter, self.highscore, 1 if self.adblock_purchased else 0, self.last_ts, self.total_time, self.sessions)
        except Exception:
            pass
        self.next_scene = "counter_screen"

    def _tick(self, dt):
        # message timer handling
        if self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer <= 0:
                self.message = ""
        self.message_label.text = self.message
        # update counter label
        self.counter_label.text = f"Dein Counter: {self.counter}"

    # Compatibility with main.py expected methods
    def update(self, dt=None):
        return

    def draw(self, screen=None):
        return

