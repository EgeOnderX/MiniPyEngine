# MiniPyEngine
## 🌐 Select Language English | [简体中文](readme.cn.md)
**MiniPyEngine** is a heavily improved and restructured version of a game engine originally created by Alexander Freyr Lúðvíksson in 2023.

This version was developed and extended by **Ege** in 2025 under the MIT License.

---

## Features:
- Uses .obj and .mtl files for models and textures. Does not support .glb format.
- It supports multiplayer.

**Supports a wide range of resolutions, including:**
- VGA (`640×480 pixels`)
- SVGA (`800×600 pixels`)
- HD (`720p, 1280×720 pixels`)
- Full HD (`1080p, 1920×1080 pixels`)
- 2K (`QHD / WQHD, 2560×1440 pixels`)
- 4K (`UHD, 3840×2160 pixels`) 

## Changes and Improvements in MiniPyEngine
- Fixed numerous bugs from the original codebase  
- Added full-screen mode by default  
- Created a new, user-friendly main menu    
- Fixed the broken free-look (mouse-look) system
- ...

---

## Known bugs:
- None.
  
---

## How to Play (with default Player.py)
- Use `W, A, S, D` keys to move your character forward, left, backward, and right.
- Hold `Shift` to run.
- Press `Space` to jump.
- Press `Ctrl` to crouch.
- Use the mouse to look around and aim.
- Left-click to shoot or interact.
- Press `Esc` to open the pause menu.

---

## How to Launch

- Double-click on `main.py`.  
- Then, make sure to check the **Settings button**.  
- If the program doesn't launch, open the `config` file with a text editor (e.g., Notepad) and verify the configuration.  
- Finally, run `StartGame.py` to launch the game.

---

## System Requirements

### Minimum system requirements for running **MiniPyEngine** smoothly:
- **OS:** Windows 10, Linux (Ubuntu 18.04 LTS or later recommended)
- **Python:** 3.8  
- **CPU:** Dual-core 2.0 GHz  
- **RAM:** 80 MB (RAM needed only for the game, not total system RAM)
- **GPU:** Integrated graphics with OpenGL 3.3 support  
- **Storage:** 20 MB free space  
- **Dependencies:** `pygame`, `PyOpenGL`, `numpy`, `shortuuid`, `psutil`

---

## Technical Details

MiniPyEngine uses modern OpenGL with custom GLSL shaders for advanced graphics beyond the fixed-function pipeline.  
Shaders are loaded and compiled at runtime from the `shaders/` directory.
To create your own game, simply modify `Player.py`, add your object files (`.obj`, `.mtl`, and textures), and define your objects inside the `objects` folder.

---

## Contributors
### README translated into Chinese by: @OwnderDuck


---

## License

This project is licensed under the `MIT` License.

- Original engine: Alexander Freyr Lúðvíksson (2023)  
- Modified and extended: MiniPyEngine by Ege Onder (2025)

---

## Future Versions

MiniPyEngine is actively being developed.  
New versions with additional features, performance improvements, and tools are planned for future releases. (1.1.0-S (stable))
Planned features:

- Optimization and performance upgrades  
- Improved graphics/rendering pipeline  
- Support for additional platforms and resolutions  
- Extended documentation and learning resources
- Sound support
- Much better multiplayer support
- Map file loader support
- NPCs
---

If you downloaded or used this project, thank you for trying out MiniPyEngine!
