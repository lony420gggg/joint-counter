from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.config import Config

# Try to read FPS from existing settings.py, fallback to 60
try:
    from settings import FPS
except Exception:
    FPS = 60
Config.set('graphics', 'maxfps', str(FPS))

# Make window fullscreen (mirrors pygame.FULLSCREEN)
Window.fullscreen = True

# Import scene classes using the same module/class names your repo already has.
# You must convert those modules (counter_screen.py, game_scene.py, etc.)
# into Kivy Screen subclasses that provide:
# - next_scene (str or None)
# - constructor signatures used below (e.g., GameScene(counter=...))
# - attributes counter, score, highscore where needed
# - an update(dt) method (or update() without args)
from counter_screen import CounterScreen
from game_scene import GameScene
from game_over_scene import GameOverScene
from shop_scene import ShopScene
from stats_scene import StatsScene

class RootScreenManager(ScreenManager):
    pass

class JointCounterApp(App):
    def build(self):
        self.sm = RootScreenManager(transition=FadeTransition())
        # initial screen
        self.counter_screen = CounterScreen(name='counter_screen')
        self.sm.add_widget(self.counter_screen)
        # schedule update loop to mimic pygame main loop
        Clock.schedule_interval(self._update, 1.0 / FPS)
        return self.sm

    def _update(self, dt):
        current = self.sm.current_screen
        if not current:
            return

        # Call screen.update(dt) if present (support update() no-arg too)
        if hasattr(current, 'update'):
            try:
                current.update(dt)
            except TypeError:
                current.update()

        # Handle scene switching via current.next_scene like original pygame code
        if hasattr(current, 'next_scene') and current.next_scene:
            ns = current.next_scene
            current.next_scene = None  # reset to avoid repeated switches

            if ns == "counter_screen":
                if not self.sm.has_screen('counter_screen'):
                    self.counter_screen = CounterScreen(name='counter_screen')
                    self.sm.add_widget(self.counter_screen)
                self.sm.current = 'counter_screen'

            elif ns == "game_scene":
                counter_val = getattr(current, 'counter', 0)
                gs = GameScene(counter=counter_val, name='game_scene')
                if self.sm.has_screen('game_scene'):
                    try:
                        self.sm.remove_widget(self.sm.get_screen('game_scene'))
                    except Exception:
                        pass
                self.sm.add_widget(gs)
                self.sm.current = 'game_scene'

            elif ns == "game_over":
                score = getattr(current, 'score', 0)
                highscore = getattr(current, 'highscore', 0)
                counter_val = getattr(current, 'counter', 0)
                gos = GameOverScene(score=score, highscore=highscore, counter=counter_val, name='game_over')
                if self.sm.has_screen('game_over'):
                    try:
                        self.sm.remove_widget(self.sm.get_screen('game_over'))
                    except Exception:
                        pass
                self.sm.add_widget(gos)
                self.sm.current = 'game_over'

            elif ns == "shop_scene":
                counter_val = getattr(current, 'counter', 0)
                ss = ShopScene(counter=counter_val, name='shop_scene')
                if self.sm.has_screen('shop_scene'):
                    try:
                        self.sm.remove_widget(self.sm.get_screen('shop_scene'))
                    except Exception:
                        pass
                self.sm.add_widget(ss)
                self.sm.current = 'shop_scene'

            elif ns == "stats_scene":
                sts = StatsScene(name='stats_scene')
                if self.sm.has_screen('stats_scene'):
                    try:
                        self.sm.remove_widget(self.sm.get_screen('stats_scene'))
                    except Exception:
                        pass
                self.sm.add_widget(sts)
                self.sm.current = 'stats_scene'

    # Allow pause on mobile
    def on_pause(self):
        return True

if __name__ == '__main__':
    JointCounterApp().run()
