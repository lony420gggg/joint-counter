import pygame
from settings import *
from button import Button
from counter_screen import CounterScreen

class ShopScene:
    def __init__(self, counter):
        self.counter = counter
        self.next_scene = None
        self.font = pygame.font.Font(None, 70)
        
        _, self.highscore, adblock, self.last_ts, self.total_time, self.sessions = load_save_data()
        self.adblock_purchased = bool(adblock)
        
        self.adblock_cost = 420000
        
        self.buy_button = Button(
            SCREEN_WIDTH // 2 - 200,
            SCREEN_HEIGHT // 2 - 50,
            400, 100,
            "AdBlock kaufen (420k)" if not self.adblock_purchased else "Bereits gekauft!",
            GREEN if not self.adblock_purchased else GRAY
        )
        
        self.back_button = Button(
            SCREEN_WIDTH // 2 - 200,
            SCREEN_HEIGHT // 2 + 150,
            400, 100,
            "Zurück",
            RED
        )
        
        self.message = ""
        self.message_timer = 0

    def handle_event(self, event):
        if self.buy_button.is_clicked(event) and not self.adblock_purchased:
            if self.counter >= self.adblock_cost:
                self.counter -= self.adblock_cost
                self.adblock_purchased = True
                self.message = "AdBlock gekauft! Keine Werbung mehr... oder so ;)"
                self.message_timer = 180  # 3 Sekunden anzeigen
                save_save_data(self.counter, self.highscore, 1, self.last_ts, self.total_time, self.sessions)
            else:
                self.message = "Nicht genug Puffs! Spiel mehr Minigame!"
                self.message_timer = 180

        if self.back_button.is_clicked(event):
            save_save_data(self.counter, self.highscore, 1 if self.adblock_purchased else 0, self.last_ts, self.total_time, self.sessions)
            self.next_scene = "counter_screen"

    def update(self):
        if self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer == 0:
                self.message = ""

    def draw(self, screen):
        screen.fill(BG_COLOR)
        
        title = self.font.render("Shop", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        
        counter_text = self.font.render(f"Dein Counter: {self.counter}", True, WHITE)
        screen.blit(counter_text, (20, 20))
        
        self.buy_button.draw(screen)
        self.back_button.draw(screen)
        
        if self.message:
            color = RED if "Nicht genug" in self.message else GREEN
            msg_text = self.font.render(self.message, True, color)
            screen.blit(msg_text, (SCREEN_WIDTH // 2 - msg_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))