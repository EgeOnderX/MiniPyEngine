[Main README](README.md) || [Türkçe](Docs/README_TR.md) || [简体中文](Docs/README_zh-CN.md) || [Deutsch](Docs/README_DE.md)
---

# MiniPyEngine 1.0.1-S language pach


---

## Features

- Uses `.obj` and `.mtl` files for models and textures. (Does **not** support `.glb` format.)
- Supports a wide range of resolutions:
  - HD (`1280×720`)
  - Full HD (`1920×1080`)
  - 2K / QHD (`2560×1440`)
  - 4K / UHD (`3840×2160`)
  - 8K (`7680×4320`)
  - 16K (`15360×8640`) 

---

## What's New in MiniPyEngine 1.0.1-S

- Added **Game Maker App** Button, **NOT** the app ( Comes in v1.0.3 )
- Multiplayer removed  (But still it needs shortuuid)
- Added support for **8K** and **16K** resolution!
- Fixed crouch-jump bug  
- Various bug fixes and internal improvements  
- VGA and SVGA resolution support removed for stability
- Added console menu.
- Added modulechk system.

---

## Known Bugs

- On AMD GPUs, textures turn black and the walls render incorrectly, as if they’re spinning or warped, but everything works properly on NVIDIA GPUs.

---

## Controls (default `Player.py`)

- Move: `W`, `A`, `S`, `D`  
- Run: Hold `Shift`  
- Jump: `Space`  
- Crouch: `Ctrl`  
- Look around: Move the mouse  
- Shoot / Interact: Left-click  
- Pause menu: `Esc`
- Press f3 to open console.

---

## How to Launch

1. Double-click `main.py`.
2. In the menu, click the **Settings** button to configure resolution and other options.
3. If the game doesn't launch:
   - Open the `config` file with a text editor (e.g., Notepad).
   - Verify the configuration settings.
4. Finally, run `StartGame.py` to start the game.

---

##   Screenshots:

## Main Menu:  

<img width="1919" height="929" alt="main" src="https://github.com/user-attachments/assets/8948a77d-fa41-483a-8725-4326b7e846bf" />

## Console Menu:   

<img width="845" height="582" alt="console" src="https://github.com/user-attachments/assets/f1d4bf1a-04ab-419e-8f93-15a3238a2c33" />

## Module Verification System:  

<img width="661" height="252" alt="modulechk" src="https://github.com/user-attachments/assets/a1885e07-20fa-4224-b8fa-ffa2f21b89ec" />

---

## System Requirements

### Minimum:

- **OS:** Windows 10 / Linux (Ubuntu 18.04+)  
- **Python:** 3.8+  
- **CPU:** Dual-core 2.0 GHz  
- **RAM:** 80 MB (game usage only)  
- **GPU:** Integrated graphics with OpenGL 3.3 support  
- **Storage:** 20 MB free space  
- **Dependencies:**  
  `pygame`, `PyOpenGL`, `numpy`, `***shortuuid***`, `psutil`

> NOTE: You might think shortuuid is only needed when there is multiplayer, but since we gradually removed it step by step, it is still necessary to prevent corruption.

---

## Technical Overview

MiniPyEngine uses **modern OpenGL** with custom GLSL shaders for advanced graphics, going beyond the fixed-function pipeline.  
Shaders are compiled at runtime from the `shaders/` directory.
16K resolution: I don't know how it works on an RTX 4090, but it runs without any problems.
You can change the resolution from the config file (without extension). Note: NEVER set the resolution below VGA — it causes weird behavior.

To create your own game:

- Modify `Player.py`  
- Add `.obj`, `.mtl`, and texture files  
- Register your objects in the `objects/` folder  
- You can create your own map by editing the level1.py file.
> NOTE: For a super silly map filled with boxes, replace the level1 file in the maps folder with the original level1
### The sound system contains only sample sounds!
---

## Console Commands

- Type 'god' to enable God Mode (health set to 9999).
- Type 'noclip' to pass through walls.
- Type 'nocrouch' to disable/enable crouching.
- Type 'nojump' to disable/enable jumping.
- Type 'exit' to close the console.
### ProTip: If you go into the config file and write `console("*consolecommand*")` there, *consolecommand* will be executed.


## License

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

**Important Notice:**  
A significant portion of the development of this version of MiniPyEngine was done entirely by Ege Önder.  
The original work by Alexander Freyr Lúðvíksson was merely a simple game with some bugs, and none of the following features existed:  

- Main menu  
- GUI  
- Developer console  
- Module verification system  
- Multi-language support  
- Functional free mouse look — in fact, even this was broken  

This notice is added to clarify that all of these features, fixes, and enhancements in the current version were implemented by Ege Önder.  
It is included solely to protect the author's rights and acknowledge the scope of contributions.

---

## Contributors:
- @OwnderDuck

---
## Planned Features for Future Versions

- Better performance and optimizations  
- Enhanced graphics/rendering pipeline  
- Additional platform support  
- Complete map file system  
- NPC system  
- Expanded documentation and tutorials  

---

If you downloaded or used this project, thank you for trying out **MiniPyEngine**!

# ...AND If you like MiniPyEngine, don’t forget to give it a ⭐!
