[app]

# (str) Titel deiner App
title = Joint Counter

# (str) Paketname (einfach so lassen)
package.name = jointcounter

# (str) Paket-Domain (einfach so lassen)
package.domain = org.lony420

# (str) Quellcode-Verzeichnis (Punkt steht für den aktuellen Ordner)
source.dir = .

# (list) Dateiendungen, die in die App aufgenommen werden sollen
# include save_data.txt and log files and all asset images
source.include_exts = py,png,jpg,jpeg,ttf,json,txt

# (str) Version der App
version = 1.0

# (list) Abhängigkeiten — use Kivy instead of pygame for Android packaging
requirements = python3,kivy

# (str) Orientierung (landscape, portrait oder all)
orientation = portrait

# (bool) Fullscreen oder nicht
fullscreen = 0

# (list) Berechtigungen (Falls du Internet brauchst, sonst leer lassen)
# android.permissions = INTERNET

# (int) Android API Level (Standard für aktuelle Handys)
android.api = 33
android.minapi = 21

# (str) Icon (Wenn du ein Bild namens icon.png hast, sonst auskommentieren)
# icon.filename = %(source.dir)s/icon.png

# (list) Unterstützte Architekturen
android.archs = arm64-v8a, armeabi-v7a

# Ensure save_data.txt and smoke_log.txt are included as assets (adjust paths if needed)
android.add_assets = save_data.txt, smoke_log.txt, assets

[buildozer]
# (int) Log-Level (2 ist am besten für Fehlersuche)
log_level = 2

# (str) Pfad zum Build-Verzeichnis
bin_dir = ./bin

