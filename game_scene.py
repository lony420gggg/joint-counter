from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button as KivyButton
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
import random
import time

from settings import *
from button import Button  # kept for compatibility if converted later

class GameScene(Screen):
    def __init__(self, counter=0, **kwargs):
        super().__init__(**kwargs)
        self.counter = counter
        self.next_scene = None

        # Player image (Kivy Image widget used as texture)
        try:
            self.player_img = Image(source="assets/player.png").texture
        except Exception:
            self.player_img = None

        win_w, win_h = Window.size
        self.player_w = dp(40); self.player_h = dp(40)
        self.player_x = dp(200)
        self.player_y = win_h / 2
        self.player_rect = [self.player_x, self.player_y, self.player_w, self.player_h]

        self.y_speed = 0
        self.gravity = 0.5
        self.jump = -10

        # Pipes & Background
        try:
            from kivy.core.image import Image as CoreImage
            self.pipe_top_tex = CoreImage("assets/pipe_top.png").texture
            self.pipe_bottom_tex = CoreImage("assets/bong_bottom.png").texture
        except Exception:
            self.pipe_top_tex = None
            self.pipe_bottom_tex = None

        try:
            self.bg_tex = Image(source="assets/bg_loop.png").texture
            # note: we'll tile the bg manually in canvas
            self.bg_x = 0
            self.bg_speed = 2
        except Exception:
            self.bg_tex = None

        self.pipe_width = dp(80)
        self.pipe_gap = dp(140)
        self.pipe_speed = 4
        self.spawn_timer = 0
        self.pipes = []
        self.score = 0

        # Load highscore
        try:
            _, self.highscore, _, _, _, _ = load_save_data()
        except Exception:
            self.highscore = 0

        # Layout and canvas
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Back button
        self.back_btn = KivyButton(text='Zurück', size_hint=(None,None), size=(dp(160), dp(60)), pos=(dp(20), Window.height - dp(80)))
        self.back_btn.bind(on_release=self._on_back)
        self.layout.add_widget(self.back_btn)

        # Score labels
        self.score_label = Label(text=f"Score: {self.score}", size_hint=(None,None), pos=(dp(20), Window.height - dp(140)), font_size=dp(18))
        self.hs_label = Label(text=f"Highscore: {self.highscore}", size_hint=(None,None), pos=(dp(20), Window.height - dp(180)), font_size=dp(18))
        self.layout.add_widget(self.score_label)
        self.layout.add_widget(self.hs_label)

        # Create initial pipe(s)
        self.create_pipe()

        # Schedule updates
        Clock.schedule_interval(self._tick, 1.0 / (FPS if 'FPS' in globals() else 60))

        # Bind input for jump (touch and keyboard)
        Window.bind(on_key_down=self._on_key_down)
        self._touch_bind = None
        self.bind(on_touch_down=self._on_touch_down)

    def _on_back(self, *args):
        self.next_scene = "counter_screen"

    def _on_key_down(self, window, key, scancode, codepoint, modifier):
        # space key = 32 on many systems, Kivy keycodes differ; check codepoint
        if codepoint == ' ' or key == 32:
            self.y_speed = self.jump

    def _on_touch_down(self, touch):
        # treat any touch as jump unless it's on back button
        if self.back_btn.collide_point(*touch.pos):
            return False
        self.y_speed = self.jump
        return True

    def create_pipe(self):
        win_w, win_h = Window.size
        gap_y = random.randint(int(dp(150)), int(win_h - dp(150) - self.pipe_gap))
        top_height = max(int(dp(50)), int(gap_y - self.pipe_gap // 2))
        bottom_y = gap_y + self.pipe_gap // 2
        bottom_height = max(int(dp(50)), int(win_h - bottom_y))

        top_rect = [win_w, win_h - top_height, self.pipe_width, top_height]  # x, y, w, h (y = bottom of rect)
        bottom_rect = [win_w, 0, self.pipe_width, bottom_height]

        top_tex = self.pipe_top_tex
        bottom_tex = self.pipe_bottom_tex

        self.pipes.append({
            "top_rect": top_rect,
            "bottom_rect": bottom_rect,
            "top_tex": top_tex,
            "bottom_tex": bottom_tex,
            "scored": False
        })

    def game_over(self):
        try:
            if self.score > self.highscore:
                self.highscore = self.score
                c, _, a, lt, tt, s = load_save_data()
                save_save_data(c, self.highscore, a, lt, tt, s)
        except Exception:
            pass
        self.next_scene = "game_over"

    def _tick(self, dt):
        # physics
        self.y_speed += self.gravity
        self.player_y += self.y_speed
        self.player_rect[1] = self.player_y

        # background scroll
        if self.bg_tex:
            self.bg_x -= self.bg_speed
            if self.bg_x <= -Window.width:
                self.bg_x = 0

        # spawn pipes
        self.spawn_timer += 1
        if self.spawn_timer > 100:
            self.create_pipe()
            self.spawn_timer = 0

        # update pipes
        for pipe in list(self.pipes):
            pipe["top_rect"][0] -= self.pipe_speed
            pipe["bottom_rect"][0] -= self.pipe_speed

            # collision detection (approximate using rects)
            p_left = self.player_rect[0]; p_right = p_left + self.player_rect[2]
            p_top = self.player_rect[1] + self.player_rect[3]; p_bottom = self.player_rect[1]

            # top rect: x..x+w, y..y+h (y is bottom)
            tr = pipe["top_rect"]
            br = pipe["bottom_rect"]

            # convert top rect to bottom-based y for collision: top_rect y is bottom coordinate (top pipe sits at top of screen)
            tr_left, tr_x, tr_w, tr_h = tr[0], tr[0], tr[2], tr[3]  # use x,w,h
            tr_bottom = Window.height - tr_h
            tr_top = Window.height

            tr_left = tr[0]; tr_right = tr[0] + tr[2]

            br_left = br[0]; br_right = br[0] + br[2]
            br_bottom = br[1]; br_top = br[1] + br[3]

            # player vs top pipe
            if not (p_right < tr_left or p_left > tr_right or p_bottom > tr_top or p_top < tr_bottom):
                self.game_over()
                return

            # player vs bottom pipe
            if not (p_right < br_left or p_left > br_right or p_top < br_bottom or p_bottom > br_top):
                self.game_over()
                return

            # scoring
            if not pipe["scored"] and (pipe["top_rect"][0] + pipe["top_rect"][2]) < self.player_x:
                self.score += 1
                pipe["scored"] = True

        # remove off-screen pipes
        self.pipes = [p for p in self.pipes if p["top_rect"][0] + p["top_rect"][2] > 0]

        # bounds check
        if self.player_y < 0 or (self.player_y + self.player_h) > Window.height:
            self.game_over()

        # update labels
        self.score_label.text = f"Score: {self.score}"
        self.hs_label.text = f"Highscore: {self.highscore}"

        # trigger canvas redraw
        self.canvas.ask_update()

    def on_size(self, *args):
        # reposition UI if window resized
        self.back_btn.pos = (dp(20), Window.height - dp(80))
        self.score_label.pos = (dp(20), Window.height - dp(140))
        self.hs_label.pos = (dp(20), Window.height - dp(180))

    def on_enter(self):
        # ensure canvas is drawn when screen enters
        self.bind(size=self.on_size)
        with self.canvas.before:
            Color(0.12, 0.12, 0.12, 1)
            Rectangle(size=Window.size, pos=self.pos)
        # draw dynamic items in on_draw by binding
        self.canvas.clear()

    def on_leave(self):
        self.unbind(size=self.on_size)

    def on_touch_up(self, touch):
        # consume touch so parent screens don't get it
        return True

    def draw(self):
        # Not used; Kivy uses canvas. But we implement canvas drawing here each tick.
        self.canvas.clear()
        with self.canvas:
            # background
            if self.bg_tex:
                # tile two backgrounds
                Rectangle(texture=self.bg_tex, pos=(self.bg_x, 0), size=(Window.width, Window.height))
                Rectangle(texture=self.bg_tex, pos=(self.bg_x + Window.width, 0), size=(Window.width, Window.height))
            else:
                Color(0.12, 0.12, 0.12, 1)
                Rectangle(pos=(0,0), size=Window.size)

            # pipes
            for pipe in self.pipes:
                tr = pipe["top_rect"]
                br = pipe["bottom_rect"]
                if pipe["top_tex"]:
                    Rectangle(texture=pipe["top_tex"], pos=(tr[0], Window.height - tr[3]), size=(tr[2], tr[3]))
                else:
                    Color(0, 0.78, 0, 1)
                    Rectangle(pos=(tr[0], Window.height - tr[3]), size=(tr[2], tr[3]))
                if pipe["bottom_tex"]:
                    Rectangle(texture=pipe["bottom_tex"], pos=(br[0], br[1]), size=(br[2], br[3]))
                else:
                    Color(0, 0.78, 0, 1)
                    Rectangle(pos=(br[0], br[1]), size=(br[2], br[3]))

            # player
            if self.player_img:
                Rectangle(texture=self.player_img, pos=(self.player_x, self.player_y), size=(self.player_w, self.player_h))
            else:
                Color(1, 1, 0, 1)
                Rectangle(pos=(self.player_x, self.player_y), size=(self.player_w, self.player_h))

    # Provide compatibility with main.py's expectation of update() method
    def update(self, dt=None):
        # call tick and redraw
        self._tick(dt if dt is not None else 0)
        self.draw()

