from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button as KivyButton
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
import time

# reuse settings and helper functions from existing repo
from settings import *
from button import Button  # keep for compatibility if you converted it to Kivy later
# If you convert button.py to a Kivy widget, you can replace usage below.

# Helper to create a Kivy button that visually matches original asset button if provided
def _make_image_button(x, y, w, h, image_path=None, on_release=None):
    layout = FloatLayout(size_hint=(None, None), size=(w, h), pos=(x, y))
    if image_path:
        img = Image(source=image_path, allow_stretch=True, keep_ratio=False)
        img.size_hint = (1, 1)
        img.pos = (0, 0)
        layout.add_widget(img)
    btn = KivyButton(text='', background_color=(0,0,0,0), size_hint=(1,1), pos=(0,0))
    if on_release:
        btn.bind(on_release=on_release)
    layout.add_widget(btn)
    return layout, btn

class CounterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_scene = None

        # Load save data (expects load_save_data in settings or another module)
        try:
            self.counter, self.highscore, self.adblock, self.last_ts, self.total_time, self.sessions = load_save_data()
        except Exception:
            # safe defaults
            self.counter = 0
            self.highscore = 0
            self.adblock = False
            self.last_ts = time.time()
            self.total_time = 0.0
            self.sessions = 0

        # Layout
        self.root_layout = FloatLayout()
        self.add_widget(self.root_layout)

        # Labels (will be updated each frame)
        self.label_puffs = Label(text='', font_size=dp(36), size_hint=(None,None))
        self.label_last_caption = Label(text='Zeit seit letztem Mal:', font_size=dp(16), size_hint=(None,None))
        self.label_last_value = Label(text='', font_size=dp(32), color=(0,1,0,1), size_hint=(None,None))
        self.label_avg_caption = Label(text='Ø Dauer:', font_size=dp(16), size_hint=(None,None))
        self.label_avg_value = Label(text='', font_size=dp(20), size_hint=(None,None))

        # Position labels relative to window size
        win_w, win_h = Window.size

        # Center top puffs
        self.label_puffs.pos = (win_w/2 - 150, win_h - dp(120))
        self.label_puffs.size = (dp(300), dp(50))
        self.root_layout.add_widget(self.label_puffs)

        # Last time caption and value
        self.label_last_caption.pos = (win_w/2 - 120, win_h - dp(220))
        self.label_last_value.pos = (win_w/2 - 80, win_h - dp(260))
        self.label_last_caption.size = (dp(240), dp(30))
        self.label_last_value.size = (dp(240), dp(40))
        self.root_layout.add_widget(self.label_last_caption)
        self.root_layout.add_widget(self.label_last_value)

        # Average caption and value
        self.label_avg_caption.pos = (win_w/2 - 60, win_h - dp(360))
        self.label_avg_value.pos = (win_w/2 - 80, win_h - dp(320))
        self.label_avg_caption.size = (dp(120), dp(30))
        self.label_avg_value.size = (dp(240), dp(40))
        self.root_layout.add_widget(self.label_avg_caption)
        self.root_layout.add_widget(self.label_avg_value)

        # Buttons (placed roughly as original)
        # smoke_button: centered
        sb_w, sb_h = dp(300), dp(120)
        sb_x = win_w/2 - sb_w/2
        sb_y = win_h - dp(420)
        smoke_layout, smoke_btn = _make_image_button(sb_x, sb_y, sb_w, sb_h, image_path='assets/smoke_button.png', on_release=self._on_smoke)
        self.root_layout.add_widget(smoke_layout)

        # game_button
        gb_w, gb_h = dp(220), dp(80)
        gb_x = win_w/2 - dp(250)
        gb_y = win_h - dp(540)
        game_layout, game_btn = _make_image_button(gb_x, gb_y, gb_w, gb_h, image_path='assets/minigame_button.png', on_release=self._on_game)
        self.root_layout.add_widget(game_layout)

        # shop_button
        sh_x = win_w/2 + dp(30)
        shop_layout, shop_btn = _make_image_button(sh_x, gb_y, gb_w, gb_h, image_path='assets/shop_button.png', on_release=self._on_shop)
        self.root_layout.add_widget(shop_layout)

        # stats_button (text button)
        stats_w, stats_h = dp(220), dp(60)
        stats_x = win_w/2 - dp(110)
        stats_y = win_h - dp(620)
        stats_btn = KivyButton(text='Statistik', size_hint=(None,None), size=(stats_w, stats_h), pos=(stats_x, stats_y))
        stats_btn.bind(on_release=self._on_stats)
        self.root_layout.add_widget(stats_btn)

        # Schedule updates (mimic update loop)
        Clock.schedule_interval(self._tick, 1.0 / (FPS if 'FPS' in globals() else 60))

    # Event handlers for buttons
    def _on_smoke(self, *args):
        now = time.time()
        diff = now - self.last_ts

        self.counter += 1
        self.total_time += diff
        self.sessions += 1
        self.last_ts = now

        # try to call repo's log/save functions if present
        try:
            log_smoke()
        except Exception:
            pass
        try:
            save_save_data(
                self.counter,
                self.highscore,
                self.adblock,
                self.last_ts,
                self.total_time,
                self.sessions
            )
        except Exception:
            pass

    def _on_game(self, *args):
        self.next_scene = "game_scene"

    def _on_shop(self, *args):
        self.next_scene = "shop_scene"

    def _on_stats(self, *args):
        self.next_scene = "stats_scene"

    def _tick(self, dt):
        # called each frame
        # update labels
        self.label_puffs.text = f"Puffs: {self.counter}"
        elapsed = time.time() - self.last_ts
        self.label_last_value.text = self.format_time(elapsed)
        avg = self.total_time / self.sessions if self.sessions > 0 else 0
        self.label_avg_value.text = self.format_time(avg)

    def format_time(self, seconds):
        s = int(seconds)
        h = s // 3600
        m = (s % 3600) // 60
        sec = s % 60
        return f"{h:02d}:{m:02d}:{sec:02d}"

