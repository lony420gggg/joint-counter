import pygame
import random
from settings import *
from button import Button

class GameScene:
    def __init__(self, counter):
        self.counter = counter
        self.next_scene = None
        
        # Player
        try:
            self.player_img = pygame.transform.scale(
                pygame.image.load("assets/player.png").convert_alpha(),
                (40, 40)
            )
        except:
            self.player_img = None

        self.player_rect = pygame.Rect(200, SCREEN_HEIGHT // 2, 40, 40)
        self.y_speed = 0
        self.gravity = 0.5
        self.jump = -10
        
        # Pipes & Background (wie vorher)
        try:
            self.pipe_top_original = pygame.image.load("assets/pipe_top.png").convert_alpha()
            self.pipe_bottom_original = pygame.image.load("assets/bong_bottom.png").convert_alpha()
        except:
            self.pipe_top_original = None
            self.pipe_bottom_original = None
        
        try:
            self.bg_img = pygame.image.load("assets/bg_loop.png").convert_alpha()
            self.bg_img = pygame.transform.scale(self.bg_img, (SCREEN_WIDTH * 2, SCREEN_HEIGHT))
            self.bg_x = 0
            self.bg_speed = 2
        except:
            self.bg_img = None
        
        self.pipe_width = 80
        self.pipe_gap = 140
        self.pipe_speed = 4
        self.spawn_timer = 0
        self.pipes = []
        self.score = 0
        
        # Highscore laden (wird später gebraucht für GameOver)
        _, self.highscore, _, _, _, _ = load_save_data()
        
        self.font = pygame.font.Font(None, 50)
        self.back_button = Button(20, 20, 160, 60, "Zurück", RED)  # einheitlich mit anderen
        
        self.create_pipe()

    def handle_event(self, event):
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or \
           (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            self.y_speed = self.jump
        
        if self.back_button.is_clicked(event):
            self.next_scene = "counter_screen"

    def create_pipe(self):
        gap_y = random.randint(150, SCREEN_HEIGHT - 150 - self.pipe_gap)
        top_height = max(50, gap_y - self.pipe_gap // 2)
        bottom_y = gap_y + self.pipe_gap // 2
        bottom_height = max(50, SCREEN_HEIGHT - bottom_y)
        
        top_rect = pygame.Rect(SCREEN_WIDTH, 0, self.pipe_width, top_height)
        bottom_rect = pygame.Rect(SCREEN_WIDTH, bottom_y, self.pipe_width, bottom_height)
        
        top_img = None
        bottom_img = None
        if self.pipe_top_original:
            top_img = pygame.transform.scale(self.pipe_top_original, (self.pipe_width, top_height))
        if self.pipe_bottom_original:
            bottom_img = pygame.transform.scale(self.pipe_bottom_original, (self.pipe_width, bottom_height))
        
        self.pipes.append({
            "top_rect": top_rect,
            "bottom_rect": bottom_rect,
            "top_img": top_img,
            "bottom_img": bottom_img,
            "scored": False
        })

    def game_over(self):
        if self.score > self.highscore:
            self.highscore = self.score
            c, _, a, lt, tt, s = load_save_data()
            save_save_data(c, self.highscore, a, lt, tt, s)
        
        self.next_scene = "game_over"

    def update(self):
        self.y_speed += self.gravity
        self.player_rect.y += self.y_speed
        
        if self.bg_img:
            self.bg_x -= self.bg_speed
            if self.bg_x <= -SCREEN_WIDTH:
                self.bg_x = 0
        
        self.spawn_timer += 1
        if self.spawn_timer > 100:
            self.create_pipe()
            self.spawn_timer = 0
        
        for pipe in self.pipes[:]:
            pipe["top_rect"].x -= self.pipe_speed
            pipe["bottom_rect"].x -= self.pipe_speed
            
            if self.player_rect.colliderect(pipe["top_rect"]) or self.player_rect.colliderect(pipe["bottom_rect"]):
                self.game_over()
                return
            
            if not pipe["scored"] and pipe["top_rect"].right < self.player_rect.left:
                self.score += 1
                pipe["scored"] = True
        
        self.pipes = [p for p in self.pipes if p["top_rect"].right > 0]
        
        if self.player_rect.top < 0 or self.player_rect.bottom > SCREEN_HEIGHT:
            self.game_over()

    def draw(self, screen):
        if self.bg_img:
            screen.blit(self.bg_img, (self.bg_x, 0))
            screen.blit(self.bg_img, (self.bg_x + SCREEN_WIDTH, 0))
        else:
            screen.fill((30, 30, 30))
        
        if self.player_img:
            screen.blit(self.player_img, self.player_rect)
        else:
            pygame.draw.circle(screen, (255, 255, 0), self.player_rect.center, 20)
        
        for pipe in self.pipes:
            if pipe["top_img"]:
                screen.blit(pipe["top_img"], pipe["top_rect"].topleft)
            else:
                pygame.draw.rect(screen, (0, 200, 0), pipe["top_rect"])
            if pipe["bottom_img"]:
                screen.blit(pipe["bottom_img"], pipe["bottom_rect"].topleft)
            else:
                pygame.draw.rect(screen, (0, 200, 0), pipe["bottom_rect"])
        
        # Score Anzeige
        screen.blit(self.font.render(f"Score: {self.score}", True, WHITE), (20, 100))
        screen.blit(self.font.render(f"Highscore: {self.highscore}", True, WHITE), (20, 150))
        
        self.back_button.draw(screen)