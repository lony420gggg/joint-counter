import datetime
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button as KivyButton
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.clock import Clock

from settings import *


class StatsScene(Screen):
    def __init__(self, **kwargs):
        super().__init__(name="stats_scene", **kwargs)
        self.next_scene = None

        self.mode = "7days"
        self.data = []
        self.anim_progress = 0.0
        self.anim_speed = 0.02

        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Title
        self.title_label = Label(
            text="",
            font_size=32,
            size_hint=(None, None),
            size=(SCREEN_WIDTH, 80),
            pos=(0, SCREEN_HEIGHT - 100),
            color=(1, 1, 1, 1),
        )
        self.layout.add_widget(self.title_label)

        # Buttons
        self.back_button = KivyButton(
            text="Zurück",
            size_hint=(None, None),
            size=(160, 60),
            pos=(20, SCREEN_HEIGHT - 80),
            background_color=(*RED, 1),
        )
        self.back_button.bind(on_release=self.on_back)
        self.layout.add_widget(self.back_button)

        self.btn_7days = self._make_mode_button("7 Tage", "7days", 200)
        self.btn_month = self._make_mode_button("Monat", "month", 330)
        self.btn_year = self._make_mode_button("Jahr", "year", 460)

        self.data = self.load_data(self.mode)

        Clock.schedule_interval(self.update, 1.0 / FPS)

    def _make_mode_button(self, text, mode, x):
        btn = KivyButton(
            text=text,
            size_hint=(None, None),
            size=(120, 50),
            pos=(x, SCREEN_HEIGHT - 70),
        )
        btn.bind(on_release=lambda *_: self.set_mode(mode))
        self.layout.add_widget(btn)
        return btn

    def set_mode(self, mode):
        self.mode = mode
        self.data = self.load_data(mode)
        self.anim_progress = 0.0

    def on_back(self, *_):
        self.next_scene = "counter_screen"

    def load_data(self, mode="7days"):
        today = datetime.date.today()
        counts = {}

        if mode == "7days":
            days = [(today - datetime.timedelta(days=i)) for i in range(6, -1, -1)]
            counts = {day: 0 for day in days}

        elif mode == "month":
            days = [(today - datetime.timedelta(days=i)) for i in range(29, -1, -1)]
            counts = {day: 0 for day in days}

        elif mode == "year":
            months = [(today.replace(day=1) - datetime.timedelta(days=i * 30)) for i in range(11, -1, -1)]
            counts = {m.replace(day=1): 0 for m in months}

        try:
            with open("smoke_log.txt", "r") as f:
                for line in f:
                    ts = float(line.strip())
                    day = datetime.date.fromtimestamp(ts)

                    if mode in ["7days", "month"]:
                        if day in counts:
                            counts[day] += 1
                    else:
                        month = day.replace(day=1)
                        if month in counts:
                            counts[month] += 1
        except:
            pass

        if mode == "year":
            return [(d.strftime("%m.%Y"), counts[d]) for d in sorted(counts)]
        return [(d.strftime("%d.%m"), counts[d]) for d in sorted(counts)]

    def update(self, dt=0):
        if self.anim_progress < 1.0:
            self.anim_progress += self.anim_speed
            self.anim_progress = min(self.anim_progress, 1.0)

        self.draw(None)

    def draw(self, screen):
        self.canvas.clear()

        title_text = {
            "7days": "Statistik – letzte 7 Tage",
            "month": "Statistik – letzter Monat",
            "year": "Statistik – letztes Jahr",
        }
        self.title_label.text = title_text[self.mode]

        self.btn_7days.background_color = (*GREEN, 1) if self.mode == "7days" else (*GRAY, 1)
        self.btn_month.background_color = (*GREEN, 1) if self.mode == "month" else (*GRAY, 1)
        self.btn_year.background_color = (*GREEN, 1) if self.mode == "year" else (*GRAY, 1)

        graph_x = 100
        graph_y = 120
        graph_w = SCREEN_WIDTH - 200
        graph_h = SCREEN_HEIGHT - 250

        with self.canvas:
            Color(45 / 255, 45 / 255, 45 / 255, 1)
            Rectangle(pos=(graph_x, graph_y), size=(graph_w, graph_h))

            if not self.data:
                return

            values = [v for _, v in self.data]
            max_value = max(values) if max(values) > 0 else 1

            points = []
            for i, (_, value) in enumerate(self.data):
                x = graph_x + int(i * graph_w / max(len(self.data) - 1, 1))
                y = graph_y + graph_h - int((value / max_value) * (graph_h - 40))
                points.append((x, y))

            total_segments = len(points) - 1
            visible_segments = int(self.anim_progress * total_segments)

            Color(*GREEN, 1)
            if visible_segments > 0:
                Line(points=points[: visible_segments + 1], width=3)

            if points:
                px, py = points[min(visible_segments, len(points) - 1)]
                Ellipse(pos=(px - 4, py - 4), size=(8, 8))

