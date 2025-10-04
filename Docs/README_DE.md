[Main README](../README.md)
---

# MiniPyEngine 1.0.1-S Sprachpaket

---

## Funktionen

- Verwendet `.obj`- und `.mtl`-Dateien für Modelle und Texturen. (Unterstützt **nicht** das `.glb`-Format.)
- Unterstützt eine Vielzahl von Auflösungen:
  - HD (`1280×720`)
  - Full HD (`1920×1080`)
  - 2K / QHD (`2560×1440`)
  - 4K / UHD (`3840×2160`)
  - 8K (`7680×4320`)
  - 16K (`15360×8640`) 

---

## Neuigkeiten in MiniPyEngine 1.0.1-S

- **Game Maker App**-Button hinzugefügt, **NICHT** die App (kommt in v1.0.3)
- Multiplayer entfernt (benötigt aber immer noch shortuuid)
- Unterstützung für **8K** zum Spaß hinzugefügt, zusätzlich **16K**-Auflösung!
- Fehler beim Ducken-Springen behoben  
- Verschiedene Fehlerbehebungen und interne Verbesserungen  
- VGA- und SVGA-Auflösungsunterstützung aus Stabilitätsgründen entfernt
- Konsolenmenü hinzugefügt
- `modulechk`-System hinzugefügt

---

## Bekannte Fehler

- Keine gemeldet.

---

## Steuerung (Standard `Player.py`)

- Bewegen: `W`, `A`, `S`, `D`  
- Rennen: `Shift` gedrückt halten  
- Springen: `Leertaste`  
- Ducken: `Strg`  
- Umschauen: Maus bewegen  
- Schießen / Interagieren: Linksklick  
- Pause-Menü: `Esc`
- Drücke `F3`, um die Konsole zu öffnen.

---

## Startanleitung

1. `main.py` doppelklicken.
2. Im Menü den **Einstellungen**-Button klicken, um Auflösung und andere Optionen zu konfigurieren.
3. Falls das Spiel nicht startet:
   - Öffne die `config`-Datei mit einem Texteditor (z. B. Notepad).
   - Überprüfe die Konfigurationseinstellungen.
4. Schließlich `StartGame.py` ausführen, um das Spiel zu starten.

---

##   Screenshots:

## Hauptmenü:  

<img width="1919" height="929" alt="main" src="https://github.com/user-attachments/assets/8948a77d-fa41-483a-8725-4326b7e846bf" />

## Konsolenmenü:   

<img width="845" height="582" alt="console" src="https://github.com/user-attachments/assets/f1d4bf1a-04ab-419e-8f93-15a3238a2c33" />

## Modul-Überprüfungssystem:  

<img width="661" height="252" alt="modulechk" src="https://github.com/user-attachments/assets/a1885e07-20fa-4224-b8fa-ffa2f21b89ec" />

---

## Systemanforderungen

### Minimum:

- **OS:** Windows 10 / Linux (Ubuntu 18.04+)  
- **Python:** 3.8+  
- **CPU:** Dual-Core 2,0 GHz  
- **RAM:** 80 MB (nur Spielnutzung)  
- **GPU:** Integrierte Grafik mit OpenGL 3.3-Unterstützung  
- **Speicherplatz:** 20 MB freier Speicher  
- **Abhängigkeiten:**  
  `pygame`, `PyOpenGL`, `numpy`, `***shortuuid***`, `psutil`

> HINWEIS: Man könnte denken, dass shortuuid nur bei Multiplayer benötigt wird, aber da wir es schrittweise entfernt haben, ist es immer noch notwendig, um Datenkorruption zu verhindern.

---

## Technischer Überblick

MiniPyEngine verwendet **modernes OpenGL** mit benutzerdefinierten GLSL-Shadern für fortgeschrittene Grafik, über die Fixed-Function-Pipeline hinaus.  
Shader werden zur Laufzeit aus dem `shaders/`-Verzeichnis kompiliert.

So erstellst du dein eigenes Spiel:

- `Player.py` anpassen  
- `.obj`-, `.mtl`- und Texturdateien hinzufügen  
- Deine Objekte im `objects/`-Ordner registrieren  
- Du kannst deine eigene Karte erstellen, indem du die Datei `level1.py` bearbeitest.  
> HINWEIS: Für eine extrem witzige Karte voller Kisten ersetze die Datei `level1` im maps-Ordner durch die originale `level1`.
### Das Soundsystem enthält nur Beispielsounds!
---

## Konsolenbefehle

- Tippe `god`, um den God Mode zu aktivieren (Gesundheit auf 9999).
- Tippe `noclip`, um durch Wände zu gehen.
- Tippe `nocrouch`, um Ducken zu deaktivieren/aktivieren.
- Tippe `nojump`, um Springen zu deaktivieren/aktivieren.
- Tippe `exit`, um die Konsole zu schließen.
### ProTipp: Wenn du in der Config-Datei `console("*consolecommand*")` einträgst, wird *consolecommand* ausgeführt.

---

## Lizenz

MIT License

Copyright (c) 2023 Alexander Freyr Lúðvíksson  
Modified into MiniPyEngine by Ege Önder, 2025  

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

ADDITIONAL NOTICE:  
THIS SOFTWARE MAY INCLUDE MODIFIED CODE ORIGINALLY WRITTEN BY ALEXANDER FREYR LÚÐVÍKSSON.  
HOWEVER, SIGNIFICANT PARTS OF MINIPYENGINE WERE WRITTEN ENTIRELY FROM SCRATCH  
BY EGE ÖNDER. IT IS INCORRECT TO ASSUME THAT ALL OF THE CODE BELONGS TO  
ALEXANDER FREYR LÚÐVÍKSSON. PLEASE REFER TO THE README FILE FOR FURTHER DETAILS.  

ANY CODE AND/OR SEGMENT WRITTEN BY EGE ÖNDER IS DISTRIBUTED UNDER THE MIT  
LICENSE IN THE NAME OF EGE ÖNDER. SUCH CODE SEGMENTS ARE INDEPENDENT AND HAVE  
NO CONNECTION WITH CODE ORIGINALLY WRITTEN BY ALEXANDER FREYR LÚÐVÍKSSON.

---

## Mitwirkende:
- @OwnderDuck

---

## Geplante Funktionen für zukünftige Versionen

- Bessere Leistung und Optimierungen  
- Verbesserte Grafik-/Rendering-Pipeline  
- Zusätzliche Plattformunterstützung  
- Vollständiges Karten-Dateisystem  
- NPC-System  
- Erweiterte Dokumentation und Tutorials  

---

Falls du dieses Projekt heruntergeladen oder verwendet hast, danke, dass du **MiniPyEngine** ausprobiert hast!
