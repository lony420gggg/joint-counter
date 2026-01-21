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
source.include_exts = py,png,jpg,jpeg,ttf,json

# (str) Version der App
version = 1.0

# (list) Abhängigkeiten (Wichtig: pygame muss hier stehen!)
requirements = python3,pygame

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

[buildozer]
# (int) Log-Level (2 ist am besten für Fehlersuche)
log_level = 2

# (str) Pfad zum Build-Verzeichnis
bin_dir = ./bin
