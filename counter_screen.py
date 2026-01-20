import pygame
import time
from settings import *
from button import Button

class CounterScreen:
    def __init__(self):
        self.next_scene = None

        # Save laden
        self.counter, self.highscore, self.adblock, self.last_ts, self.total_time, self.sessions = load_save_data()

        # Fonts
        self.font_big = pygame.font.Font(None, 80)
        self.font_medium = pygame.font.Font(None, 50)
        self.font_small = pygame.font.Font(None, 40)

        # Buttons
        self.smoke_button = Button(
            SCREEN_WIDTH // 2 - 150,
            320,
            300,
            120,
            "",
            PURPLE,
            "assets/smoke_button.png"
        )

        self.game_button = Button(
            SCREEN_WIDTH // 2 - 250,
            480,
            220,
            80,
            "",
            GREEN,
            "assets/minigame_button.png"
        )

        self.shop_button = Button(
            SCREEN_WIDTH // 2 + 30,
            480,
            220,
            80,
            "",
            RED,
            "assets/shop_button.png"
        )

        self.stats_button = Button(
            SCREEN_WIDTH // 2 - 110,
            580,
            220,
            60,
            "Statistik",
            GRAY
        )

    def handle_event(self, event):
        if self.smoke_button.is_clicked(event):
            now = time.time()
            diff = now - self.last_ts

            self.counter += 1
            self.total_time += diff
            self.sessions += 1
            self.last_ts = now

            log_smoke()  # Zeitstempel speichern

            save_save_data(
                self.counter,
                self.highscore,
                self.adblock,
                self.last_ts,
                self.total_time,
                self.sessions
            )

        if self.game_button.is_clicked(event):
            self.next_scene = "game_scene"

        if self.shop_button.is_clicked(event):
            self.next_scene = "shop_scene"

        if self.stats_button.is_clicked(event):
            self.next_scene = "stats_scene"

    def update(self):
        pass

    def format_time(self, seconds):
        s = int(seconds)
        h = s // 3600
        m = (s % 3600) // 60
        sec = s % 60
        return f"{h:02d}:{m:02d}:{sec:02d}"

    def draw(self, screen):
        screen.fill(BG_COLOR)

        # Counter
        puffs = self.font_big.render(f"Puffs: {self.counter}", True, WHITE)
        screen.blit(puffs, (SCREEN_WIDTH//2 - puffs.get_width()//2, 40))

        # Zeit seit letztem Smoke
        elapsed = time.time() - self.last_ts
        label_last = self.font_small.render("Zeit seit letztem Mal:", True, WHITE)
        screen.blit(label_last, (SCREEN_WIDTH//2 - label_last.get_width()//2, 140))

        value_last = self.font_big.render(self.format_time(elapsed), True, GREEN)
        screen.blit(value_last, (SCREEN_WIDTH//2 - value_last.get_width()//2, 170))

        # Ø Zeit
        avg = self.total_time / self.sessions if self.sessions > 0 else 0
        label_avg = self.font_small.render("Ø Dauer:", True, WHITE)
        screen.blit(label_avg, (SCREEN_WIDTH//2 - label_avg.get_width()//2, 250))

        value_avg = self.font_medium.render(self.format_time(avg), True, WHITE)
        screen.blit(value_avg, (SCREEN_WIDTH//2 - value_avg.get_width()//2, 280))

        # Buttons
        self.smoke_button.draw(screen)
        self.game_button.draw(screen)
        self.shop_button.draw(screen)
        self.stats_button.draw(screen)
