import pygame
from settings import *
from counter_screen import CounterScreen
from game_scene import GameScene
from game_over_scene import GameOverScene
from shop_scene import ShopScene
from stats_scene import StatsScene

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
pygame.display.set_caption("Joint Counter")

current_scene = CounterScreen()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        current_scene.handle_event(event)

    current_scene.update()

    if current_scene.next_scene:
        ns = current_scene.next_scene

        if ns == "counter_screen":
            current_scene = CounterScreen()
        elif ns == "game_scene":
            current_scene = GameScene(current_scene.counter)
        elif ns == "game_over":
            # Jetzt mit allen 3 Werten
            current_scene = GameOverScene(
                current_scene.score,
                current_scene.highscore,
                current_scene.counter
            )
        elif ns == "shop_scene":
            current_scene = ShopScene(current_scene.counter)
        elif ns == "stats_scene":
            current_scene = StatsScene()

    current_scene.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()