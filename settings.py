import time
import os

# 🔥 ANDROID SAVE PATH
try:
    from kivy.utils import platform
    if platform == "android":
        from android.storage import app_storage_path
        BASE_PATH = app_storage_path()
    else:
        BASE_PATH = os.getcwd()
except:
    BASE_PATH = os.getcwd()

SAVE_FILE = os.path.join(BASE_PATH, "save_data.txt")
SMOKE_LOG_FILE = os.path.join(BASE_PATH, "smoke_log.txt")

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
PURPLE = (128, 0, 128)
GRAY = (100, 100, 100)
BG_COLOR = (25, 25, 25)


def load_save_data():
    try:
        with open(SAVE_FILE, "r") as f:
            parts = f.read().strip().split(",")
            counter = int(parts[0])
            highscore = int(parts[1])
            adblock = int(parts[2])
            last_ts = float(parts[3])
            total_time = float(parts[4])
            sessions = int(parts[5])
            return counter, highscore, adblock, last_ts, total_time, sessions
    except:
        return 0, 0, 0, time.time(), 0.0, 0


def save_save_data(counter, highscore, adblock, last_ts, total_time, sessions):
    try:
        with open(SAVE_FILE, "w") as f:
            f.write(f"{counter},{highscore},{adblock},{last_ts},{total_time},{sessions}")
    except:
        pass


def log_smoke():
    try:
        with open(SMOKE_LOG_FILE, "a") as f:
            f.write(f"{time.time()}\n")
    except:
        pass

