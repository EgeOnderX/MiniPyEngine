[Main README](Docs/README.md)
###### Du siehst dir die deutsche Version an.

---

# MiniPyEngine

**MiniPyEngine** ist eine stark verbesserte und umstrukturierte Version einer Spiel-Engine, die ursprünglich 2023 von Alexander Freyr Lúðvíksson entwickelt wurde.

Diese Version wurde 2025 von **Ege** unter der MIT-Lizenz weiterentwickelt und erweitert.

---

## Funktionen:
- Verwendet `.obj` und `.mtl` Dateien für Modelle und Texturen. Unterstützt **kein** `.glb` Format.  
- Unterstützt Multiplayer.

**Unterstützt eine breite Palette von Auflösungen, darunter:**  
- VGA (`640×480 Pixel`)  
- SVGA (`800×600 Pixel`)  
- HD (`720p, 1280×720 Pixel`)  
- Full HD (`1080p, 1920×1080 Pixel`)  
- 2K (`QHD / WQHD, 2560×1440 Pixel`)  
- 4K (`UHD, 3840×2160 Pixel`)

---

## Änderungen und Verbesserungen in MiniPyEngine

- Zahlreiche Fehler im Original-Code behoben  
- Vollbildmodus standardmäßig aktiviert  
- Neues, benutzerfreundliches Hauptmenü erstellt  
- Defektes Free-Look (Mausblick) System repariert  
- ...

---

## Bekannte Fehler:
- Keine.

---

## Spielsteuerung (Standard Player.py)

- Bewege deinen Charakter mit `W`, `A`, `S`, `D` vorwärts, links, rückwärts und rechts.  
- Halte `Shift`, um zu rennen.  
- Drücke `Leertaste`, um zu springen.  
- Drücke `Strg`, um dich zu ducken.  
- Benutze die Maus, um dich umzuschauen und zu zielen.  
- Linksklick zum Schießen oder Interagieren.  
- Drücke `Esc`, um das Pausenmenü zu öffnen.

---

## Startanleitung

- Doppelklicke auf `main.py`.  
- Prüfe im Menü den **Einstellungen-Button**.  
- Wenn das Programm nicht startet, öffne die `config`-Datei mit einem Texteditor (z.B. Notepad) und überprüfe die Konfiguration.  
- Starte abschließend `StartGame.py`, um das Spiel zu starten.

---

## Systemanforderungen

### Minimale Systemanforderungen für flüssiges Spielen mit **MiniPyEngine**:

- **OS:** Windows 10, Linux (Ubuntu 18.04 LTS oder neuer empfohlen)  
- **Python:** 3.8  
- **CPU:** Dual-Core 2.0 GHz  
- **RAM:** 80 MB (nur Spiel-RAM, nicht Gesamtsystem-RAM)  
- **GPU:** Integrierte Grafikkarte mit OpenGL 3.3 Unterstützung  
- **Speicher:** 20 MB freier Speicherplatz  
- **Abhängigkeiten:** `pygame`, `PyOpenGL`, `numpy`, `shortuuid`, `psutil`

---

## Technische Details

MiniPyEngine nutzt modernes OpenGL mit eigenen GLSL-Shadern für fortgeschrittene Grafiken jenseits der Fixed-Function-Pipeline.  
Shader werden zur Laufzeit aus dem Verzeichnis `shaders/` geladen und kompiliert.  
Um dein eigenes Spiel zu erstellen, modifiziere `Player.py`, füge deine Objekte (`.obj`, `.mtl` und Texturen) hinzu und definiere sie im `objects`-Ordner.

---

## Mitwirkende

### README ins Chinesische übersetzt von: @OwnderDuck

---

## Lizenz

Dieses Projekt ist unter der `MIT` Lizenz veröffentlicht.

- Original-Engine: Alexander Freyr Lúðvíksson (2023)  
- Modifiziert und erweitert: MiniPyEngine von Ege Onder (2025)

---

## Zukünftige Versionen

MiniPyEngine wird aktiv weiterentwickelt.  
Neue Versionen mit zusätzlichen Features, Performance-Verbesserungen und Tools sind für zukünftige Releases geplant (1.1.0-S (stable)).  
Geplante Features:

- Optimierungen und Performance-Upgrades  
- Verbesserte Grafik- und Rendering-Pipeline  
- Unterstützung weiterer Plattformen und Auflösungen  
- Erweiterte Dokumentation und Lernressourcen  
- Sound-Unterstützung  
- Deutlich verbesserter Multiplayer  
- Map-Datei-Loader  
- NPC-System

---

Wenn du dieses Projekt heruntergeladen oder benutzt hast, danke, dass du MiniPyEngine ausprobiert hast!
