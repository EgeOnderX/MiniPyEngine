import sys
import subprocess
import pygame
import configparser
import os
from Engine import MiniPyEngine

button_texts = {
    "tr": {
        "btn_gamemaker": "Oyun Yapıcı",
        "btn_startgame": "Oyunu Başlat",
        "btn_settings": "Ayarlar",
        "btn_about": "Hakkında",
        "btn_exit": "Çıkış",
        "btn_back": "Geri",
        "btn_sens": "Hassasiyet",
        "title_settings": "Ayarlar",
        "title_about": "Hakkında",
        "btn_res": "Çözünürlük",
        "btn_vsync": "VSync",
        "btn_fps": "Maks FPS",
        "btn_lang": "Dil",
        "btn_render_mode": "Render Modu"
    },
    "dt": {
        "btn_gamemaker": "Spielersteller",
        "btn_startgame": "Spiel Starten",
        "btn_settings": "Einstellungen",
        "btn_about": "Über",
        "btn_exit": "Beenden",
        "btn_back": "Zurück",
        "btn_sens": "Empfindlichkeit",
        "title_settings": "Einstellungen",
        "title_about": "Über",
        "btn_res": "Auflösung",
        "btn_vsync": "VSync",
        "btn_fps": "Max FPS",
        "btn_lang": "Sprache",
        "btn_render_mode": "Render-Modus"
    },
    "en": {
        "btn_gamemaker": "Game Maker",
        "btn_startgame": "Start Game",
        "btn_settings": "Settings",
        "btn_about": "About",
        "btn_exit": "Exit",
        "btn_back": "Back",
        "btn_sens": "Sensitivity",
        "title_settings": "Settings",
        "title_about": "About",
        "btn_res": "Resolution",
        "btn_vsync": "VSync",
        "btn_fps": "Max FPS",
        "btn_lang": "Language",
        "btn_render_mode": "Render Mode"
    },
    "cn": {
        "btn_gamemaker": "游戏制作",
        "btn_startgame": "开始游戏",
        "btn_settings": "设置",
        "btn_about": "关于",
        "btn_exit": "退出",
        "btn_back": "返回",
        "btn_sens": "灵敏度",
        "title_settings": "设置",
        "title_about": "关于",
        "btn_res": "分辨率",
        "btn_vsync": "VSync",
        "btn_fps": "最大 FPS",
        "btn_lang": "语言",
        "btn_render_mode": "渲染模式"
    }
}

lang_display_names = {
    "en": "English",
    "tr": "Türkçe",
    "dt": "Deutsch",
    "cn": "中文"
}

def get_txt(key, lang):
    lang_dict = button_texts.get(lang, button_texts["en"])
    return lang_dict.get(key, button_texts["en"].get(key, key))

def get_key_name(event):
    if event.type == pygame.KEYDOWN:
        name = pygame.key.name(event.key).upper()
        if "SHIFT" in name: return "LSHIFT" if "LEFT" in name else "RSHIFT"
        if "CTRL" in name: return "LCTRL" if "LEFT" in name else "RCTRL"
        if "ALT" in name: return "LALT"
        if name == "SPACE": return "SPACE"
        if name == "ESCAPE": return "ESC"
        return name
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1: return "LEFT"
        if event.button == 2: return "MIDDLE"
        if event.button == 3: return "RIGHT"
    return None

def draw_ui_button(screen, text, font, rect, mouse_pos, is_waiting=False, align="left"):
    is_hovered = rect.collidepoint(mouse_pos)
    button_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    
    bg_color = (255, 255, 255, 0)
    if is_waiting:
        bg_color = (255, 100, 100, 180)
    elif is_hovered:
        bg_color = (255, 220, 0, 180)

    pygame.draw.rect(button_surface, bg_color, button_surface.get_rect(), border_radius=12)

    label = font.render(text, True, (255, 255, 255))
    if align == "left":
        text_rect = label.get_rect(midleft=(20, rect.height // 2))
    else:
        text_rect = label.get_rect(center=(rect.width // 2, rect.height // 2))
        
    button_surface.blit(label, text_rect)
    screen.blit(button_surface, rect.topleft)
    return is_hovered

def draw_slider(screen, rect, value, min_val, max_val, font, label_text, is_hovered):
    slider_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    bg_color = (255, 220, 0, 100) if is_hovered else (255, 255, 255, 30)
    pygame.draw.rect(slider_surface, bg_color, slider_surface.get_rect(), border_radius=12)
    screen.blit(slider_surface, rect.topleft)

    txt = f"{label_text}: {value}"
    label = font.render(txt, True, (255, 255, 255))
    screen.blit(label, (rect.x + 15, rect.y + 6))

    track_x = rect.x + 15
    track_y = rect.y + rect.height - 12
    track_w = rect.width - 30
    
    pygame.draw.line(screen, (150, 150, 150), (track_x, track_y), (track_x + track_w, track_y), 4)

    ratio = (value - min_val) / float(max_val - min_val)
    knob_x = track_x + int(ratio * track_w)
    
    pygame.draw.line(screen, (255, 220, 0), (track_x, track_y), (knob_x, track_y), 4)
    pygame.draw.circle(screen, (255, 255, 255), (knob_x, track_y), 7)

def main():
    pygame.init()
    pygame.mixer.init()
    
    config = configparser.ConfigParser()
    config_file = "config.cfg"
    config.read(config_file)
    
    title = config.get('ENGINE', 'title', fallback='MiniPyEngine')
    w = config.getint('ENGINE', 'width', fallback=1024)
    h = config.getint('ENGINE', 'height', fallback=720)
    is_fullscreen = config.getboolean('ENGINE', 'fullscreen', fallback=False)
    vsync_on = config.getboolean('ENGINE', 'vsync', fallback=False)
    max_fps = config.getint('ENGINE', 'fps', fallback=144)
    
    if is_fullscreen:
        info = pygame.display.Info()
        display_size = (info.current_w, info.current_h)
        flags = pygame.FULLSCREEN
    else:
        display_size = (w, h)
        flags = 0
        
    vsync_val = 1 if vsync_on else 0
    
    try:
        screen = pygame.display.set_mode(display_size, flags, vsync=vsync_val)
    except:
        screen = pygame.display.set_mode(display_size, flags)
            
    pygame.display.set_caption(title)
    actual_w, actual_h = screen.get_size()

    font_names = ["Arial", "SimSun", "Microsoft YaHei", "Segoe UI", "sans-serif"]
    font = pygame.font.SysFont(font_names, 40)
    small_font = pygame.font.SysFont(font_names, 22)
    title_font = pygame.font.SysFont(font_names, 60, bold=True)
    clock = pygame.time.Clock()

    engine = MiniPyEngine()
    state = "MAIN"

    click_sound_path = None
    sound_dirs = ["Sounds", "sounds"]
    for s_dir in sound_dirs:
        if os.path.exists(s_dir):
            for f in os.listdir(s_dir):
                if f.lower().endswith(".mp3"):
                    click_sound_path = os.path.join(s_dir, f)
                    break
            if click_sound_path:
                break

    def play_click():
        if click_sound_path:
            try:
                pygame.mixer.music.load(click_sound_path)
                pygame.mixer.music.set_volume(0.15)
                pygame.mixer.music.play()
            except Exception as e:
                print(f"[AUDIO ERROR] {e}")

    bg_image = pygame.Surface((actual_w, actual_h))
    bg_image.fill((25, 25, 35)) 
    bg_paths = [
        os.path.join("Textures", "Main", "Main.jpg"), 
        os.path.join("Textures", "Main", "Main.png"),
        os.path.join("textures", "main", "main.jpg"),
        os.path.join("textures", "main", "main.png")
    ]
    
    for path in bg_paths:
        if os.path.exists(path):
            try:
                img = pygame.image.load(path).convert()
                bg_image = pygame.transform.smoothscale(img, (actual_w, actual_h))
                break
            except Exception as e:
                print(f"[BG ERROR] {e}")

    btn_w, btn_h = 300, 60
    btn_x = 50

    main_button_rects = {
        "btn_startgame": pygame.Rect(btn_x, actual_h // 2 - 150, btn_w, btn_h),
        "btn_gamemaker": pygame.Rect(btn_x, actual_h // 2 - 75, btn_w, btn_h),
        "btn_about":     pygame.Rect(btn_x, actual_h // 2, btn_w, btn_h),
        "btn_settings":  pygame.Rect(btn_x, actual_h // 2 + 75, btn_w, btn_h),
        "btn_exit":      pygame.Rect(btn_x, actual_h // 2 + 150, btn_w, btn_h)
    }

    resolutions = [
        (640, 480), (800, 600), (1024, 720), (1024, 768),
        (1280, 720), (1366, 768), (1920, 1080), (2560, 1440),
        (3840, 2160), (7680, 4320), (15360, 8640), (30720, 17280)
    ]
    
    fps_options = [60, 75, 120, 144, 240, 0]
    render_modes = ["fixed_function", "opengl_shader"]
    langs = ["en", "tr", "dt", "cn"]
    input_actions = ["forward", "backward", "left", "right", "run", "jump", "crouch", "console", "pause", "shoot"]
    
    waiting_for_key = None
    back_rect = pygame.Rect(50, actual_h - 80, 150, 50)

    current_sens_val = config.getint('ENGINE', 'sensitivity', fallback=50)
    current_sens_val = max(1, min(100, current_sens_val))
    is_dragging_slider = False

    about_scroll_y = 0
    about_lines = []
    about_file_path = "about" if os.path.exists("about") else ("About" if os.path.exists("About") else None)
    if about_file_path:
        try:
            with open(about_file_path, "r", encoding="utf-8") as f:
                about_lines = f.read().splitlines()
        except Exception as e:
            about_lines = [f"[ERROR] Could not read about file: {e}"]
    else:
        about_lines = ["'about' dosyası bulunamadı."]

    running = True
    while running:
        screen.blit(bg_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        mouse_released = False

        cur_lang = config.get('ENGINE', 'lang', fallback='en')
        if cur_lang not in langs:
            cur_lang = 'en'

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_released = True

            if state == "ABOUT":
                if event.type == pygame.MOUSEWHEEL:
                    about_scroll_y -= event.y * 35
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        about_scroll_y -= 35
                    elif event.key == pygame.K_DOWN:
                        about_scroll_y += 35

            if state == "SETTINGS" and waiting_for_key:
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    if not back_rect.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
                        new_key = get_key_name(event)
                    elif event.type == pygame.KEYDOWN:
                        new_key = get_key_name(event)
                    else:
                        new_key = None
                        
                    if new_key and new_key != "ESC":
                        config.set('INPUT', waiting_for_key, new_key)
                        with open(config_file, 'w') as f:
                            config.write(f)
                            
                    waiting_for_key = None
                    mouse_clicked = False
                    play_click()
                    continue

        if state == "MAIN":
            for btn_key, rect in main_button_rects.items():
                btn_label = get_txt(btn_key, cur_lang)
                if draw_ui_button(screen, btn_label, font, rect, mouse_pos, align="left") and mouse_clicked:
                    play_click()
                    if btn_key == "btn_startgame":
                        engine.run_game()
                        # Oyundan çıkıldığında 2D Pygame ekran modunu yeniden yükler
                        try:
                            screen = pygame.display.set_mode(display_size, flags, vsync=vsync_val)
                        except Exception:
                            screen = pygame.display.set_mode(display_size, flags)
                        pygame.event.set_grab(False)
                        pygame.mouse.set_visible(True)
                    elif btn_key == "btn_gamemaker":
                        try:
                            subprocess.Popen([sys.executable, "GameMaker.py"])
                        except Exception as e:
                            print(f"[ERROR] Failed to launch GameMaker: {e}")
                    elif btn_key == "btn_about":
                        state = "ABOUT"
                        about_scroll_y = 0
                    elif btn_key == "btn_settings":
                        state = "SETTINGS"
                    elif btn_key == "btn_exit":
                        running = False

        elif state == "ABOUT":
            title_text = get_txt("title_about", cur_lang)
            title_surf = title_font.render(title_text, True, (255, 255, 255))
            screen.blit(title_surf, (actual_w // 2 - title_surf.get_width() // 2, 30))

            back_label = get_txt("btn_back", cur_lang)
            if draw_ui_button(screen, back_label, small_font, back_rect, mouse_pos, align="center") and mouse_clicked:
                play_click()
                state = "MAIN"

            content_rect = pygame.Rect(50, 120, actual_w - 100, actual_h - 220)
            line_height = 35
            total_text_height = len(about_lines) * line_height
            max_scroll = max(0, total_text_height - content_rect.height)
            
            about_scroll_y = max(0, min(about_scroll_y, max_scroll))

            screen.set_clip(content_rect)
            y_offset = content_rect.y - about_scroll_y
            for line in about_lines:
                if y_offset + line_height > content_rect.y and y_offset < content_rect.bottom:
                    line_surf = small_font.render(line, True, (220, 220, 220))
                    screen.blit(line_surf, (content_rect.x + 20, y_offset))
                y_offset += line_height
                
            screen.set_clip(None)

        elif state == "SETTINGS":
            title_text = get_txt("title_settings", cur_lang)
            title_surf = title_font.render(title_text, True, (255, 255, 255))
            screen.blit(title_surf, (actual_w // 2 - title_surf.get_width() // 2, 30))

            back_label = get_txt("btn_back", cur_lang)
            if draw_ui_button(screen, back_label, small_font, back_rect, mouse_pos, align="center") and mouse_clicked:
                play_click()
                state = "MAIN"

            engine_start_x, engine_start_y = 50, 120
            
            cur_res = f"{config.get('ENGINE', 'width', fallback='1024')}x{config.get('ENGINE', 'height', fallback='720')}"
            res_label_prefix = get_txt("btn_res", cur_lang)
            res_rect = pygame.Rect(engine_start_x, engine_start_y, 280, 45)
            if draw_ui_button(screen, f"{res_label_prefix}: {cur_res}", small_font, res_rect, mouse_pos, align="left") and mouse_clicked:
                play_click()
                current_tuple = (config.getint('ENGINE', 'width', fallback=1024), config.getint('ENGINE', 'height', fallback=720))
                next_idx = (resolutions.index(current_tuple) + 1) % len(resolutions) if current_tuple in resolutions else 0
                config.set('ENGINE', 'width', str(resolutions[next_idx][0]))
                config.set('ENGINE', 'height', str(resolutions[next_idx][1]))
                with open(config_file, 'w') as f: config.write(f)

            if not config.has_section('RENDER'): config.add_section('RENDER')
            cur_render_mode = config.get('RENDER', 'mode', fallback='fixed_function')
            mode_label_prefix = get_txt("btn_render_mode", cur_lang)
            mode_display = "Fixed Function" if cur_render_mode == "fixed_function" else "OpenGL Shader"
            mode_rect = pygame.Rect(engine_start_x, engine_start_y + 50, 280, 45)
            if draw_ui_button(screen, f"{mode_label_prefix}: {mode_display}", small_font, mode_rect, mouse_pos, align="left") and mouse_clicked:
                play_click()
                next_mode = "opengl_shader" if cur_render_mode == "fixed_function" else "fixed_function"
                config.set('RENDER', 'mode', next_mode)
                with open(config_file, 'w') as f: config.write(f)

            cur_vsync = config.getboolean('ENGINE', 'vsync', fallback=False)
            vsync_label_prefix = get_txt("btn_vsync", cur_lang)
            vsync_rect = pygame.Rect(engine_start_x, engine_start_y + 100, 280, 45)
            if draw_ui_button(screen, f"{vsync_label_prefix}: {'ON' if cur_vsync else 'OFF'}", small_font, vsync_rect, mouse_pos, align="left") and mouse_clicked:
                play_click()
                config.set('ENGINE', 'vsync', str(not cur_vsync).lower())
                with open(config_file, 'w') as f: config.write(f)

            cur_fps = config.getint('ENGINE', 'fps', fallback=144)
            fps_display_val = "Unlimited" if cur_fps == 0 else str(cur_fps)
            fps_label_prefix = get_txt("btn_fps", cur_lang)
            fps_rect = pygame.Rect(engine_start_x, engine_start_y + 150, 280, 45)
            if draw_ui_button(screen, f"{fps_label_prefix}: {fps_display_val}", small_font, fps_rect, mouse_pos, align="left") and mouse_clicked:
                play_click()
                next_fps = fps_options[(fps_options.index(cur_fps) + 1) % len(fps_options)] if cur_fps in fps_options else fps_options[0]
                config.set('ENGINE', 'fps', str(next_fps))
                max_fps = next_fps
                with open(config_file, 'w') as f: config.write(f)

            lang_label_prefix = get_txt("btn_lang", cur_lang)
            lang_native_display = lang_display_names.get(cur_lang, "English")
            lang_rect = pygame.Rect(engine_start_x, engine_start_y + 200, 280, 45)
            if draw_ui_button(screen, f"{lang_label_prefix}: {lang_native_display}", small_font, lang_rect, mouse_pos, align="left") and mouse_clicked:
                play_click()
                next_lang = langs[(langs.index(cur_lang) + 1) % len(langs)] if cur_lang in langs else 'en'
                config.set('ENGINE', 'lang', next_lang)
                with open(config_file, 'w') as f: config.write(f)

            sens_rect = pygame.Rect(engine_start_x, engine_start_y + 250, 280, 45)
            is_sens_hovered = sens_rect.collidepoint(mouse_pos)

            if mouse_clicked and is_sens_hovered:
                is_dragging_slider = True

            if is_dragging_slider:
                if pygame.mouse.get_pressed()[0]:
                    track_x = sens_rect.x + 15
                    track_w = sens_rect.width - 30
                    rel_x = max(0, min(mouse_pos[0] - track_x, track_w))
                    current_sens_val = int(1 + (rel_x / float(track_w)) * 99)
                else:
                    is_dragging_slider = False
                    config.set('ENGINE', 'sensitivity', str(current_sens_val))
                    with open(config_file, 'w') as f: config.write(f)

            if mouse_released and is_dragging_slider:
                is_dragging_slider = False
                config.set('ENGINE', 'sensitivity', str(current_sens_val))
                with open(config_file, 'w') as f: config.write(f)

            sens_title = get_txt("btn_sens", cur_lang)
            draw_slider(screen, sens_rect, current_sens_val, 1, 100, small_font, sens_title, is_sens_hovered)

            input_start_x = actual_w // 2 + 50
            input_start_y = 120
            
            for i, action in enumerate(input_actions):
                col = i % 2
                row = i // 2
                x_offset = input_start_x + (col * 220)
                y_offset = input_start_y + (row * 55)

                label_surf = small_font.render(action.capitalize(), True, (255, 255, 255))
                screen.blit(label_surf, (x_offset, y_offset + 10))

                current_key = config.get('INPUT', action, fallback='NONE')
                btn_text = "Press..." if waiting_for_key == action else current_key
                btn_rect = pygame.Rect(x_offset + 90, y_offset, 110, 45)
                
                is_waiting = (waiting_for_key == action)
                if draw_ui_button(screen, btn_text, small_font, btn_rect, mouse_pos, is_waiting, align="center") and mouse_clicked:
                    play_click()
                    waiting_for_key = action

        pygame.display.flip()
        
        if max_fps > 0:
            clock.tick(max_fps)
        else:
            clock.tick()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
