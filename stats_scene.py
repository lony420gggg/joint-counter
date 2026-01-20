import pygame
import datetime
from settings import *
from button import Button

class StatsScene:
    def __init__(self):
        self.next_scene = None

        self.font_title = pygame.font.Font(None, 60)
        self.font_small = pygame.font.Font(None, 28)

        # Buttons
        self.back_button = Button(20, 20, 160, 60, "Zurück", RED)
        self.btn_7days = Button(200, 20, 120, 50, "7 Tage", GREEN)
        self.btn_month = Button(330, 20, 120, 50, "Monat", GRAY)
        self.btn_year = Button(460, 20, 120, 50, "Jahr", GRAY)

        self.mode = "7days"  # default

        self.data = self.load_data(mode=self.mode)

        # Animation
        self.anim_progress = 0.0
        self.anim_speed = 0.02

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
            months = [(today.replace(day=1) - datetime.timedelta(days=i*30)) for i in range(11, -1, -1)]
            counts = {m.replace(day=1): 0 for m in months}

        try:
            with open("smoke_log.txt", "r") as f:
                for line in f:
                    ts = float(line.strip())
                    day = datetime.date.fromtimestamp(ts)

                    if mode in ["7days", "month"]:
                        if day in counts:
                            counts[day] += 1
                    else:  # year
                        month = day.replace(day=1)
                        if month in counts:
                            counts[month] += 1
        except:
            pass

        if mode == "year":
            return [(d.strftime("%m.%Y"), counts[d]) for d in sorted(counts.keys())]
        else:
            return [(d.strftime("%d.%m"), counts[d]) for d in sorted(counts.keys())]

    def handle_event(self, event):
        if self.back_button.is_clicked(event):
            self.next_scene = "counter_screen"

        if self.btn_7days.is_clicked(event):
            self.mode = "7days"
            self.data = self.load_data(self.mode)
            self.anim_progress = 0.0

        if self.btn_month.is_clicked(event):
            self.mode = "month"
            self.data = self.load_data(self.mode)
            self.anim_progress = 0.0

        if self.btn_year.is_clicked(event):
            self.mode = "year"
            self.data = self.load_data(self.mode)
            self.anim_progress = 0.0

    def update(self):
        if self.anim_progress < 1.0:
            self.anim_progress += self.anim_speed
            if self.anim_progress > 1.0:
                self.anim_progress = 1.0

    def draw_graph(self, screen):
        graph_x = 100
        graph_y = 120
        graph_w = SCREEN_WIDTH - 200
        graph_h = SCREEN_HEIGHT - 250

        pygame.draw.rect(
            screen,
            (45, 45, 45),
            (graph_x, graph_y, graph_w, graph_h),
            border_radius=12
        )

        values = [v for _, v in self.data]
        max_value = max(values) if max(values) > 0 else 1

        points = []
        for i, (_, value) in enumerate(self.data):
            x = graph_x + int(i * graph_w / max(len(self.data)-1, 1))
            y = graph_y + graph_h - int((value / max_value) * (graph_h - 40))
            points.append((x, y))

        # Animierte Linie
        total_segments = len(points)-1
        visible_segments = int(self.anim_progress * total_segments)

        if visible_segments > 0:
            pygame.draw.lines(screen, GREEN, False, points[:visible_segments+1], 4)

        if visible_segments < len(points):
            pygame.draw.circle(screen, GREEN, points[visible_segments], 6)

        for i, (label, value) in enumerate(self.data):
            x = graph_x + int(i * graph_w / max(len(self.data)-1,1))
            day_text = self.font_small.render(label, True, WHITE)
            screen.blit(day_text, (x - day_text.get_width()//2, graph_y + graph_h + 10))

            if i <= visible_segments:
                val_text = self.font_small.render(str(value), True, WHITE)
                screen.blit(val_text, (x - val_text.get_width()//2, graph_y - 30))

    def draw(self, screen):
        screen.fill(BG_COLOR)

        title_text = {
            "7days": "Statistik – letzte 7 Tage",
            "month": "Statistik – letzter Monat",
            "year": "Statistik – letztes Jahr"
        }
        title = self.font_title.render(title_text[self.mode], True, WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 60))

        # Buttons Farben
        self.btn_7days.color = GREEN if self.mode=="7days" else GRAY
        self.btn_month.color = GREEN if self.mode=="month" else GRAY
        self.btn_year.color = GREEN if self.mode=="year" else GRAY

        self.btn_7days.draw(screen)
        self.btn_month.draw(screen)
        self.btn_year.draw(screen)
        self.back_button.draw(screen)

        self.draw_graph(screen)
