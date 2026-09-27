# MiniPyEngine v2.0.0-S

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
![Version](https://img.shields.io/badge/version-2.0.0--S-green.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellow.svg)
![OpenGL](https://img.shields.io/badge/OpenGL-3.3%2B-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)
[![Download](https://img.shields.io/badge/Download-ZIP-success.svg)](https://github.com/EgeOnderX/MiniPyEngine/archive/refs/heads/main.zip)
[![Issues](https://img.shields.io/badge/Report-Issue-critical.svg)](https://github.com/EgeOnderX/MiniPyEngine/issues)

> **Important License & Major Version Update:**
> The license for MiniPyEngine has officially been changed to **Apache License 2.0** under **Ege Önder**.
> Due to complete architectural refactoring and massive performance improvements, the version number has jumped directly from **v1.0.2 / v1.0.3-B** to **v2.0.0-S**.

---

## Overview

MiniPyEngine is a modular, lightweight 3D game engine and real-time rendering framework implemented in Python using Pygame and PyOpenGL. Version 2.0.0-S introduces a completely rewritten core pipeline, introducing global VRAM texture caching, optimized OBJ model batch rendering, multi-language localized menu system, and an interactive developer console with real-time variable tweaking.

---

## Architectural Overhaul

The codebase of MiniPyEngine has been **COMPLETELY rewritten from scratch by Ege Önder**. The engine now features a modular 3D pipeline, optimized texture caching, unified vector math (`Vector3`, `Transform`), and multi-language GUI support.

---

## Comparison: v1.0.2-S vs. v2.0.0-S

| Feature / Aspect | Old Version (v1.0.2-S) | New Version (v2.0.0-S) |
| --- | --- | --- |
| **Code Architecture** | Legacy structure | Completely rewritten from scratch by Ege Önder |
| **License** | MIT License | **Apache License 2.0** |
| **Rendering Modes** | Fixed function only | Dual mode: `fixed_function` & `opengl_shader` |
| **OBJ Model Loading** | Per-polygon state changes | Batched `GL_TRIANGLES` compilation & display lists |
| **Texture Management** | Reloaded per instance | Global VRAM texture caching (`TEXTURE_CACHE`) |
| **GUI & Localization** | Basic single-language GUI | Multi-language menu (English, Turkish, German, Chinese) |
| **Configuration** | Static setup | Dynamic INI/CFG parser with runtime key rebinding |
| **HUD & Font System** | Uncached redraws | High-performance OpenGL texture font caching |

---

## Key Features in v2.0.0-S

* **Complete Codebase Re-architecture:** Clean, modular structure (`Engine.py`, `MapLoader.py`, `Main.py`).
* **Dual Rendering Pipeline:** Support for both legacy fixed-function rendering and programmable OpenGL shaders via configuration.
* **Optimized OBJ / MTL Importer:** Triangulated batch rendering using OpenGL display lists (`GL_TRIANGLES`) to eliminate frame bottlenecks.
* **Global Texture Caching:** Efficient VRAM memory management via `TEXTURE_CACHE` avoiding duplicate GPU uploads.
* **Native Multi-Language Support:** Built-in launcher UI localizations for English (EN), Turkish (TR), German (DT), and Chinese (CN).
* **Interactive Settings & Keybindings:** Dynamic resolution switcher (up to Ultra-HD presets), VSync toggle, target FPS limits, sensitivity slider, and customizable key binding configuration.
* **Built-in Console & Cheats:** Integrated developer console supporting `god`, `noclip`, `nojump`, and `nocrouch` commands with smooth animation overlays.
* * - Auto-assigned AABB collision and gravity system for every object.
- Designed for FPS (first-person shooter) games.
- Uses `.obj` and `.mtl` files for models and textures.  
  *(Note: `.glb` format is not supported.)*
- Supports a wide range of resolutions:
  - HD (1280×720)
  - Full HD (1920×1080)
  - 2K / QHD (2560×1440)
  - 4K / UHD (3840×2160)
  - 8K (7680×4320)
  - 16K (15360×8640)
 
---

## Repository Structure

```text
MiniPyEngine/
│   About
│   Config.cfg
│   Engine.py
│   GameMaker.py
│   Main.py
│   MapLoader.py
│
├───Maps
│       default.mpf
│
├───Maths
│       Collision.py
│       Light.py
│       Physics.py
│
├───Objects
│   ├───Ammo
│   │   │   Ammo.jpg
│   │   │   Ammo.mtl
│   │   │   Ammo.obj
│   │   │   Ammo.py
│   │   │
│   │   └───__pycache__
│   │           Ammo.cpython-311.pyc
│   │
│   ├───Crate
│   │   │   Crate.mtl
│   │   │   Crate.obj
│   │   │   Crate.png
│   │   │   Crate.py
│   │   │   crate1.png
│   │   │
│   │   └───__pycache__
│   │           Crate.cpython-311.pyc
│   │
│   ├───Cube
│   │   │   cube.py
│   │   │
│   │   └───__pycache__
│   │           cube.cpython-311.pyc
│   │
│   ├───Default
│   │   │   Player.py
│   │   │
│   │   └───Bullet
│   │       │   Bullet.jpg
│   │       │   Bullet.mtl
│   │       │   Bullet.obj
│   │       │   Bullet.py
│   │       │
│   │       └───__pycache__
│   │               Bullet.cpython-311.pyc
│   │
│   ├───Floor
│   │   │   Floor.png
│   │   │   Floor.py
│   │   │
│   │   └───__pycache__
│   │           Floor.cpython-311.pyc
│   │
│   ├───Gun
│   │   │   Gun.mtl
│   │   │   Gun.obj
│   │   │   Gun.png
│   │   │   Gun.py
│   │   │
│   │   └───__pycache__
│   │           Gun.cpython-311.pyc
│   │
│   ├───TexturedCube
│   │   │   TexturedCube.py
│   │   │
│   │   └───__pycache__
│   │           TexturedCube.cpython-311.pyc
│   │
│   └───Walls
│       │   longwall.png
│       │   longwall2.png
│       │   Walls.py
│       │
│       └───__pycache__
│               Walls.cpython-311.pyc
│
├───Shaders
├───Sounds
│       Damage.mp3
│       Dead.mp3
│       Menu.mp3
│       Shot.mp3
│
└───Textures
    └───Main
            Main.png

```

---

## Requirements & Installation

### Minimum System Requirements

- **OS:** Windows 10 / Linux (Ubuntu 18.04+)  
- **Python:** 3.8+  
- **CPU:** Dual-core 2.0 GHz  
- **RAM:** 80 MB (in-game usage)  
- **GPU:** Integrated GPU with OpenGL 3.3 support  
- **Storage:** 50 MB free  
- **Dependencies:**  
  `pygame`, `PyOpenGL`, `numpy`

### Setup Instructions

1. Clone or download the repository:
```bash
git clone https://github.com/EgeOnderX/MiniPyEngine.git
cd MiniPyEngine

```


2. Run the launcher:
```bash
python Main.py

```


---

## Map File Format (.mpf) & Usage

MiniPyEngine uses `.mpf` (MiniPyEngine Map File) to construct level geometry dynamically at runtime.

### Line Format Parameters

* **ObjectType:** Name registered in `MapLoader.py` (`TexturedCube`, `Crate`, `Ammo`, `Gun`, `Floor`, `Walls`, `Cube`).
* **Position:** X, Y, Z coordinates in world space.
* **Rotation:** Rotation angles in degrees along X, Y, Z axes.
* **Scale:** Scale multipliers along X, Y, Z axes.
* **Texture Path (Optional):** Path to custom image texture.

### Example `.mpf` Map File

```text
# === MiniPyEngine Map Example ===
object: Floor, 0,0,0, 0,0,0, 100,1,100
object: Walls, 0,5,-50, 0,0,0, 100,10,1
object: Walls, 0,5,50, 0,0,0, 100,10,1
object: Walls, -50,5,0, 0,0,0, 1,10,100
object: Walls, 50,5,0, 0,0,0, 1,10,100
object: Crate, 0,0.4,0, 0,45,0, 0.8,0.8,0.8
object: Crate, 3,0.4,2, 0,20,0, 0.8,0.8,0.8
object: Crate, -4,0.4,-2, 0,90,0, 0.8,0.8,0.8
object: Ammo, 2,0.1,3, 0,0,0, 0.2,0.2,0.2
object: Ammo, 2.5,0.1,3.2, 0,15,0, 0.2,0.2,0.2
object: Gun, 5,0.5,0, 0,0,0, 1,1,1

```

---

## Default Controls

| Action | Key / Input |
| --- | --- |
| Move Forward / Backward | W / S |
| Strafe Left / Right | A / D |
| Run | Hold Left Shift |
| Jump | Space |
| Crouch | Left Control |
| Shoot | Left Mouse Button |
| Weapon Selection | Numbers 1–4 / Mouse Wheel |
| Open Console | F3 |
| Pause Menu | Esc |

---

## Console Commands

Press `F3` in-game to toggle the console:

* `god`: Toggle God Mode (invincibility).
* `noclip`: Pass through physical collisions.
* `nojump`: Disable jump mechanics.
* `nocrouch`: Disable crouching mechanics.
* `clear`: Clear console history buffer.
* `help`: Display list of available console commands.

---

## Contributors:
- @OwnderDuck

---


## License

Distributed under the **Apache License 2.0**. See `LICENSE` for more information.

Copyright 2025 Ege Önder.

---

## Planned Features for Future Versions

- Better performance and optimizations  
- Enhanced graphics/rendering pipeline  
- Additional platform support  
- NPC system  
- Expanded documentation and tutorials  

---

If you downloaded or used this project, thank you for trying out **MiniPyEngine**!

## ...AND If you like MiniPyEngine, don’t forget to give it a ⭐!
