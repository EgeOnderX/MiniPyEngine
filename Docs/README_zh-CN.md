[Main README](../README.md)
---

# MiniPyEngine 1.0.1-S 语言补丁

**MiniPyEngine** 是对最初由 **Alexander Freyr Lúðvíksson** 于 2023 年创建的游戏引擎进行重大改进和重构后的版本。

该版本由 **Ege** 于 2025 年在 MIT 许可证下开发并扩展。

---

## Features

- 使用 `.obj` 和 `.mtl` 文件来加载模型和纹理。（**不支持** `.glb` 格式。）
- 支持多种分辨率：
  - HD (`1280×720`)
  - Full HD (`1920×1080`)
  - 2K / QHD (`2560×1440`)
  - 4K / UHD (`3840×2160`)
  - 8K (`7680×4320`)
  - 16K (`15360×8640`) 

---

## MiniPyEngine 1.0.1-S 的新功能

- 添加了 **Game Maker App** 按钮（**注意**：实际应用将在 v1.0.3 中推出）
- 移除了多人游戏功能（但仍需使用 **shortuuid** 库）
- 为趣味用途添加了 **8K** 支持，并新增了 **16K** 分辨率
- 修复了“蹲跳”相关的 bug
- 多项 bug 修复与内部优化
- 为提升稳定性，移除了 VGA 和 SVGA 分辨率支持
- 新增控制台菜单
- 添加了 modulechk 模块检查系统

---

## 已知问题

- 无报告
---

## 控制 (默认 `Player.py`)

- 移动: `W`, `A`, `S`, `D`
- 疾跑: 按住 `Shift`
- 跳跃: `Space`
- 蹲下: `Ctrl`
- 转动视角：移动鼠标
- 射击 / 交互：鼠标左键
- 暂停菜单: `Esc`
- 按 `F3` 打开控制台

---

## 如何启动 MiniPyEngine

1. 双击 `main.py` 文件
2. 在菜单中点击 **Settings（设置）** 按钮，配置分辨率和其他选项
3. 如果游戏无法启动：
   - 使用文本编辑器（如记事本）打开 `config` 文件
   - 检查配置设置是否正确
4. 最后运行 `StartGame.py` 来启动游戏

---

## 屏幕快照：

## 主菜单：

<img width="1919" height="929" alt="main" src="https://github.com/user-attachments/assets/8948a77d-fa41-483a-8725-4326b7e846bf" />

## 控制菜单：

<img width="845" height="582" alt="console" src="https://github.com/user-attachments/assets/f1d4bf1a-04ab-419e-8f93-15a3238a2c33" />

## 模块验证系统:

<img width="661" height="252" alt="modulechk" src="https://github.com/user-attachments/assets/a1885e07-20fa-4224-b8fa-ffa2f21b89ec" />

---

## 系统要求

### 最低要求：

- **系统：** Windows 10 / Linux (Ubuntu 18.04+)  
- **Python 版本：** 3.8+  
- **CPU:** Dual-core 2.0 GHz  
- **内存：** 80 MB （仅供游戏使用）
- **显卡：** 支持 OpenGL 3.3 的集成显卡
- **存储：** 20 MB
- **依赖库：**  
  `pygame` `PyOpenGL` `numpy` `shortuuid` `psutil`

> 我们在逐步移除多人游戏，但为防止数据损坏，仍需 **shortuuid**

---

## 技术概览

使用现代 OpenGL 和自定义 GLSL 着色器，支持高级图形渲染。
着色器在运行时从 `shaders/` 文件夹编译。

开发自己的游戏需：

- 修改 `Player.py`  
- 添加 `.obj`、`.mtl`，和纹理文件
- 在 `objects/` 文件夹注册对象
- 编辑 `level1.py` 创建地图
> 想要一个充满箱子的搞笑地图？替换 maps 文件夹中的 level1 文件即可。
### 音效系统：仅包含示例音效！
---

## 指令

- 'god'：开启上帝模式（生命值设为 9999）
- 'noclip'：穿墙模式
- 'nocrouch'：启用/禁用蹲下
- 'nojump'：启用/禁用跳跃
- 'exit'：关闭控制台

## License

MIT License

Original Copyright (c) 2023 Alexander Freyr Lúðvíksson  
Modified into MiniPyEngine by Ege, 2025  

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


---

## 贡献者：
- MiniPyEngine 中文文档 @OwnderDuck

---
## 未来计划

- 更好的性能与优化
- 增强的图形/渲染管线
- 支持更多平台
- 完整的地图文件系统
- NPC 系统
- 扩展的文档与教程

---

如果你下载了 **MiniPyEngine**，感谢你的试用！
