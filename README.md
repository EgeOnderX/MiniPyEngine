# MiniPyEngine 1.0.2-S
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Version](https://img.shields.io/badge/version-1.0.2--S-green.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellow.svg)
![OpenGL](https://img.shields.io/badge/OpenGL-3.3%2B-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)
![Engine](https://img.shields.io/badge/Engine-MiniPyEngine-orange.svg)
[![Download](https://img.shields.io/badge/Download-ZIP-success.svg)](https://github.com/EgeOnderX/MiniPyEngine/archive/refs/heads/main.zip)
[![Issues](https://img.shields.io/badge/Report-Issue-critical.svg)](https://github.com/EgeOnderX/MiniPyEngine/issues)

---

## Features

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

## What's New in MiniPyEngine 1.0.2-S

- Added **Game Maker App**
- Fixed **crouch** bug
- Fixed **collision** bug
- Added **.mpf** support
- Improved **player system**
- Cleaned and optimized core code
- Decision: From this version onward, the engine and its license belong **solely to Ege Önder**, as the project is now fully independent from Alexander Frey’s original logic and concept.

---

## Known Bugs

- On **AMD GPUs**, textures may turn black and walls can appear distorted or spinning.  
  *(Everything works correctly on NVIDIA GPUs.)*

---

## Default Controls (`Player.py`)

| Action | Key |
|:-------|:----|
| Move | W, A, S, D |
| Run | Hold `Shift` |
| Jump | `Space` |
| Crouch | `Ctrl` |
| Look Around | Move the mouse |
| Shoot / Interact | Left-click |
| Pause Menu | `Esc` |
| Open Console | `F3` |

---

## How to Launch

1. Run `main.py`.
2. Click **Settings** to configure resolution and options.
3. If the game doesn’t start:
   - Open the `config` file with a text editor.
   - Verify that all settings are valid.
4. Finally, run `StartGame.py` to launch the game.

---

## Screenshots

### Main Menu
<img width="1919" height="929" alt="main" src="https://github.com/user-attachments/assets/8948a77d-fa41-483a-8725-4326b7e846bf" />

### Console Menu
<img width="845" height="582" alt="console" src="https://github.com/user-attachments/assets/f1d4bf1a-04ab-419e-8f93-15a3238a2c33" />

### Module Verification System
<img width="661" height="252" alt="modulechk" src="https://github.com/user-attachments/assets/a1885e07-20fa-4224-b8fa-ffa2f21b89ec" />

---

## System Requirements

### Minimum

- **OS:** Windows 10 / Linux (Ubuntu 18.04+)  
- **Python:** 3.8+  
- **CPU:** Dual-core 2.0 GHz  
- **RAM:** 80 MB (in-game usage)  
- **GPU:** Integrated GPU with OpenGL 3.3 support  
- **Storage:** 20 MB free  
- **Dependencies:**  
  `pygame`, `PyOpenGL`, `numpy`, `shortuuid`, `psutil`

> **Note:** Even though `shortuuid` was originally for multiplayer, it’s still required internally to prevent data corruption.

---

## Technical Overview

MiniPyEngine uses **modern OpenGL** with **custom GLSL shaders**, avoiding the fixed-function pipeline.  
Shaders are loaded and compiled at runtime from the `/shaders` directory.  

It supports up to **16K resolution** — tested to run stably even on RTX 4090.  
Resolution can be adjusted in the `config` file.  
⚠️ **Warning:** Never set the resolution below QVGA, as it may cause unpredictable behavior.

---

##To create your own game:

- Edit `maps/default.mpf`
*(Note: You can use the GMMKR GUI. To open it: run main.py and click Game Maker)*
*(Note: The current sound system includes only sample sounds.)*

---


## What is “.mpf”?

**MiniPyEngine Map File** — a simple, human-readable map format used to define level geometry, object placement, and textures.

Each line represents an **object instance** with position, rotation, and scale data, along with optional texture or color information.

### Syntax Overview

- Each non-empty line is parsed from top to bottom.  
- Lines starting with `#` are treated as **comments** (ignored by the parser).  
- Each object line must start with:  
  `object: Type, px,py,pz, rx,ry,rz, sx,sy,sz, [extra...]`  
- where:  
  - `Type` → object class name (`TexturedCube`, `Crate`, `Gun`, etc.)  
  - `px,py,pz` → position (X, Y, Z)  
  - `rx,ry,rz` → rotation (X, Y, Z)  
  - `sx,sy,sz` → scale (X, Y, Z)  
  - `[extra...]` → optional fields (e.g. texture path, color, shininess)

### Notes

- Any line beginning with `#` is skipped by the loader — use this for comments or deactivated objects.  
- Optional texture paths (like `textures/crate.png`) are automatically resolved from the project root.  
- The parser automatically identifies the object type and spawns the corresponding Python class (e.g., `TexturedCube`, `Crate`, `Gun`).  
- Missing or invalid object types are logged with `[INFO] Unknown object type`.

---

### Example (Default Demo Map)

```Minipyengine Map File (.MPF)
# MiniPyEngine detailed demo map (default)
# Built for dynamic object + texture variety test (scaled down crates)

# === WALLS ===
object: TexturedCube, 0,0.2,10, 0,0,0, 20,1.5,0.1, textures/longwall.png
object: TexturedCube, 0,0.2,-10, 0,0,0, 20,1.5,0.1, textures/longwall.png
object: TexturedCube, 10,0.2,0, 0,0,0, 0.1,1.5,20, textures/longwall2.png
object: TexturedCube, -10,0.2,0, 0,0,0, 0.1,1.5,20, textures/longwall2.png

# === CENTER DECOR ===
object: Crate, 0,-0.45,0, 0,45,0, 0.18,0.18,0.18
object: Crate, 0,-0.15,0, 0,0,0, 0.18,0.18,0.18
object: Crate, 0,0.15,0, 0,90,0, 0.18,0.18,0.18

# === MIXED CRATES AREA (left) ===
object: Crate, -5,-0.45,3, 0,0,0, 0.15,0.15,0.15, textures/crate.png
object: Crate, -4.5,-0.15,2.75, 0,30,0, 0.12,0.12,0.12, textures/crate.png

# === STACKED CRATES (right) ===
object: Crate, 6,-0.45,-3, 0,0,0, 0.18,0.18,0.18, textures/crate.png

# === WEAPON ===
object: Gun, 2,0,1, 0,0,0, 0.2,0.2,0.2, textures/gun.png

# === DECOR WALL VARIATION ===
#object: TexturedCube, 0,1.5,-5, 0,0,0, 8,0.3,0.1, textures/longwall2.png
#object: TexturedCube, 0,1.8,-5, 0,0,0, 7,0.1,0.1, textures/longwall.png
```

## Console Commands

| Command | Description |
|:--------|:-------------|
| `god` | Enables God Mode (health = 9999) |
| `noclip` | Walk through walls |
| `nocrouch` | Toggle crouching |
| `nojump` | Toggle jumping |
| `exit` | Close console |

> **Pro Tip:** You can auto-execute commands by adding  
> `console("command")` inside the config file.

---

---

## Contributors:
- @OwnderDuck

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
