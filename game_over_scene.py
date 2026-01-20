import pygame
from settings import *
from button import Button

class GameOverScene:
    def __init__(self, score, highscore=0, counter=0):
        self.score = score
        self.highscore = highscore
        self.counter = counter
        self.next_scene = None

        # Highscore updaten + speichern, falls besser
        if self.score > self.highscore:
            self.highscore = self.score
            c, _, a, lt, tt, s = load_save_data()
            save_save_data(c, self.highscore, a, lt, tt, s)

        self.font_big = pygame.font.Font(None, 90)
        self.font_medium = pygame.font.Font(None, 50)

        self.retry_button = Button(
            SCREEN_WIDTH // 2 - 150,
            420,
            300,
            80,
            "Nochmal",
            GREEN
        )

        self.back_button = Button(
            SCREEN_WIDTH // 2 - 150,
            520,
            300,
            80,
            "Zurück",
            RED
        )

    def handle_event(self, event):
        if self.retry_button.is_clicked(event):
            self.next_scene = "game_scene"

        if self.back_button.is_clicked(event):
            self.next_scene = "counter_screen"

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((20, 20, 20))

        title = self.font_big.render("GAME OVER", True, RED)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 120))

        score_text = self.font_medium.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 240))

        high_text = self.font_medium.render(f"Highscore: {self.highscore}", True, GREEN)
        screen.blit(high_text, (SCREEN_WIDTH//2 - high_text.get_width()//2, 300))

        counter_text = self.font_medium.render(f"Puffs: {self.counter}", True, WHITE)
        screen.blit(counter_text, (SCREEN_WIDTH//2 - counter_text.get_width()//2, 360))

        self.retry_button.draw(screen)
        self.back_button.draw(screen)