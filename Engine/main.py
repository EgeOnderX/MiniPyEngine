import modulechk
modulechk.chk.module()
import sys, subprocess, os, socket, pygame, psutil

# Settings default
screen_width = 1920
screen_height = 1080
sensitivity = 25
settings_active = False
button_texts = {
    "tr": {
        "btn_gamemaker": "Oyun Yapıcı",
        "btn_startgame": "Oyunu Başlat",
        "btn_settings": "Ayarlar",
        "btn_about": "Hakkında",
        "btn_exit": "Çıkış",
        "btn_back": "Geri",
        "btn_sens": "Hassasiyet"
    },
    "dt": {
        "btn_gamemaker": "Spielersteller",
        "btn_startgame": "Spiel Starten",
        "btn_settings": "Einstellungen",
        "btn_about": "Über",
        "btn_exit": "Beenden",
        "btn_back": "Zurück",
        "btn_sens": "Empfindlichkeit"
    },
    "en": {
        "btn_gamemaker": "Game Maker",
        "btn_startgame": "Start Game",
        "btn_settings": "Settings",
        "btn_about": "About",
        "btn_exit": "Exit",
        "btn_back": "Back",
        "btn_sens": "Sensitivity"
    },
    "cn": {
        "btn_gamemaker": "游戏制作",
        "btn_startgame": "开始游戏",
        "btn_settings": "设置",
        "btn_about": "关于",
        "btn_exit": "退出",
        "btn_back": "返回",
        "btn_sens": "灵敏度"
    }
}
lang_buttons = {
    "German": pygame.Rect(450, 300, 150, 40),
    "English": pygame.Rect(450, 350, 150, 40),
    "Turkish": pygame.Rect(450, 400, 150, 40),
    "Chinese": pygame.Rect(450, 450, 150, 40)
}

lang_mapping = {
    "German": "dt",
    "English": "en",
    "Turkish": "tr",
    "Chinese": "cn"
}
current_lang = "en"
pygame.init()
try:
    with open("config", "r") as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")  # tırnak varsa temizle

            if key == "screen-width":
                screen_width = int(value)
            elif key == "screen-height":
                screen_height = int(value)
            elif key == "sensitivity":
                sensitivity = int(value)
            elif key == "lang":
                if value in button_texts:
                    current_lang = value
except Exception as e:
    print("Fatal Error:", e)
# Dil seçenekleri için buton metinleri (anahtarlar string olmalı)

# Dil seçimine göre buton başlıklarını güncelle
def update_button_texts(lang):
    global btn_gamemaker, btn_startgame, btn_settings, btn_about, btn_exit, btn_back, btn_sens
    btn_gamemaker = button_texts[lang]["btn_gamemaker"]
    btn_startgame = button_texts[lang]["btn_startgame"]
    btn_settings = button_texts[lang]["btn_settings"]
    btn_about = button_texts[lang]["btn_about"]
    btn_exit = button_texts[lang]["btn_exit"]
    btn_back = button_texts[lang]["btn_back"]
    btn_sens = button_texts[lang]["btn_sens"]

update_button_texts(current_lang)

# Screen info
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
pygame.display.set_caption("MiniPyEngine Main Menu")
print("===MiniPyEngine Main Menu===")

if current_lang == "cn":
    font = pygame.font.Font("fonts/simhei.ttf", 40)
    small_font = pygame.font.Font("fonts/simhei.ttf", 30)
else:
    font = pygame.font.Font("fonts/arial.ttf", 40)
    small_font = pygame.font.Font("fonts/arial.ttf", 30)

clock = pygame.time.Clock()

# Renkler
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLUE = (70, 130, 180)
BLACK = (0, 0, 0)

button_width = 200
button_height = 50
button_x = 100
buttons = {
    btn_gamemaker: pygame.Rect(button_x, 180, button_width, button_height),
    btn_startgame: pygame.Rect(button_x, 250, button_width, button_height),
    btn_settings: pygame.Rect(button_x, 320, button_width, button_height),
    btn_about: pygame.Rect(button_x, 390, button_width, button_height),
    btn_exit: pygame.Rect(button_x, 460, button_width, button_height)
}
def update_buttons():
    global buttons
    buttons = {
        btn_gamemaker: pygame.Rect(button_x, 180, button_width, button_height),
        btn_startgame: pygame.Rect(button_x, 250, button_width, button_height),
        btn_settings: pygame.Rect(button_x, 320, button_width, button_height),
        btn_about: pygame.Rect(button_x, 390, button_width, button_height),
        btn_exit: pygame.Rect(button_x, 460, button_width, button_height)
    }

#

# Dil güncellemesini config okunduktan sonra yap
update_button_texts(current_lang)
buttons = {
    btn_gamemaker: pygame.Rect(button_x, 180, button_width, button_height),
    btn_startgame: pygame.Rect(button_x, 250, button_width, button_height),
    btn_settings: pygame.Rect(button_x, 320, button_width, button_height),
    btn_about: pygame.Rect(button_x, 390, button_width, button_height),
    btn_exit: pygame.Rect(button_x, 460, button_width, button_height)
}
print(current_lang)
# Arka plan resmi yükle
try:
    bg_image = pygame.image.load("textures/main.png")
except:
    bg_image = pygame.image.load("textures/missing.png")

def save_config():
    with open("config", "w") as f:
        f.write(f"server-ip:127.0.0.1\n")
        f.write(f"server-port:7532\n")
        f.write(f"screen-width:{screen_width}\n")
        f.write(f"screen-height:{screen_height}\n")
        f.write(f"sensitivity:{sensitivity}\n")
        f.write(f"lang:{current_lang}\n")

def draw_background():
    scaled_bg = pygame.transform.scale(bg_image, (info.current_w, info.current_h))
    screen.blit(scaled_bg, (0, 0))

def draw_menu():
    draw_background()
    mouse_pos = pygame.mouse.get_pos()

    for text, rect in buttons.items():
        is_hovered = rect.collidepoint(mouse_pos)

        button_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        if is_hovered:
            button_surface.fill((255, 255, 0, 160))
            if not hasattr(draw_menu, "hovered") or draw_menu.hovered != text:
                draw_menu.hovered = text
                try:
                    pygame.mixer.init()
                    pygame.mixer.Sound("sounds/buttonmenu.mp3").play()
                except:
                    pass
        else:
            button_surface.fill((0, 0, 0, 0))

        screen.blit(button_surface, rect.topleft)
        label = font.render(text, True, WHITE)
        screen.blit(label, label.get_rect(center=rect.center))

    pygame.display.flip()

resolution_options = [
    ("1280x720 (HD)", (1280, 720), pygame.Rect(100, 300, 200, 40)),
    ("1920x1080 (Full HD)", (1920, 1080), pygame.Rect(100, 350, 200, 40)),
    ("2560x1440 (2K)", (2560, 1440), pygame.Rect(100, 400, 200, 40)),
    ("3840x2160 (4K)", (3840, 2160), pygame.Rect(100, 450, 200, 40)),
    ("7680x4320 (8K)", (7680, 4320), pygame.Rect(100, 500, 200, 40)),
    ("15360x8640 (16K)", (15360, 8640), pygame.Rect(100, 550, 200, 40))
]

sens_rect = pygame.Rect(100, 610, 300, 40)
back_rect = pygame.Rect(100, 670, 200, 50)

# Ayarlar menüsüne dil butonları
lang_buttons = {
    "German": pygame.Rect(450, 300, 150, 40),
    "English": pygame.Rect(450, 350, 150, 40),
    "Turkish": pygame.Rect(450, 400, 150, 40),
    "Chinese": pygame.Rect(450, 450, 150, 40)
}

lang_mapping = {
    "German": "dt",
    "English": "en",
    "Turkish": "tr",
    "Chinese": "cn"
}

def draw_settings():
    draw_background()
    mouse_pos = pygame.mouse.get_pos()

    # Çözünürlük seçenekleri
    for label_text, res, rect in resolution_options:
        is_selected = (screen_width, screen_height) == res
        is_hovered = rect.collidepoint(mouse_pos)

        surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        if is_selected:
            surface.fill((255, 255, 0, 160))
        elif is_hovered:
            surface.fill((255, 255, 255, 40))
        else:
            surface.fill((0, 0, 0, 0))

        screen.blit(surface, rect.topleft)
        label = small_font.render(label_text, True, WHITE)
        screen.blit(label, label.get_rect(center=rect.center))

    # Sensitivity
    pygame.draw.rect(screen, BLUE, sens_rect, border_radius=12)
    sens_label = small_font.render(f"{btn_sens}: {sensitivity}", True, WHITE)
    screen.blit(sens_label, sens_rect.move(10, 8))

    # Back
    pygame.draw.rect(screen, GRAY, back_rect, border_radius=12)
    back_label = small_font.render(btn_back, True, WHITE)
    screen.blit(back_label, back_rect.move(10, 10))

    # Language buttons
    for name, rect in lang_buttons.items():
        is_hovered = rect.collidepoint(mouse_pos)
        button_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        
        if current_lang == lang_mapping[name]:
            button_surface.fill((255, 255, 0, 160))
        elif is_hovered:
            button_surface.fill((255, 255, 0, 160))
        else:
            button_surface.fill((0, 0, 0, 0))
        
        screen.blit(button_surface, rect.topleft)
        label = small_font.render(name, True, WHITE)
        screen.blit(label, label.get_rect(center=rect.center))


    pygame.display.flip()


def run_game():
    for p in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = p.info.get('cmdline')
            if cmdline and any("StartGame.py" in part for part in cmdline):
                print("StartGame is already running. Not launching again.")
                sys.exit()
                return
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, KeyError):
            pass
    try:
        subprocess.Popen([sys.executable, "StartGame.py", "--launched-from-menu"])
    except Exception as e:
        print("Failed to launch StartGame:", e)

running = True

while running:
    if settings_active:
        draw_settings()
    else:
        draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if settings_active:
                save_config()
                settings_active = False
            else:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if settings_active:
                for name, rect in lang_buttons.items():
                    if rect.collidepoint(pos):
                        current_lang = lang_mapping[name]
                        update_button_texts(current_lang)
                        update_buttons()
                        save_config()
                for label, res, rect in resolution_options:
                    if rect.collidepoint(pos):
                        screen_width, screen_height = res
                        try:
                            pygame.mixer.Sound("sounds/buttonmenu.mp3").play()
                        except:
                            pass
                if sens_rect.collidepoint(pos):
                    if sensitivity >= 100:
                        sensitivity = 0
                    else:
                        sensitivity += 5
                if back_rect.collidepoint(pos):
                    save_config()
                    settings_active = False
                    try:
                        pygame.mixer.Sound("sounds/buttonmenu.mp3").play()
                    except:
                        pass
            else:
                if buttons[btn_gamemaker].collidepoint(pos):
                    try:
                        pygame.mixer.Sound("sounds/buttonmenu.mp3").play()
                    except:
                        pass
                    parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
                    server_path = os.path.join(parent_dir, "GMMKR", "GMMKR.py")
                    subprocess.Popen([sys.executable, server_path])

                elif buttons[btn_startgame].collidepoint(pos):
                    run_game()
                    sys.exit()
                    pygame.quit()
                    try:
                        pygame.mixer.Sound("sounds/buttonmenu.mp3").play()
                    except:
                        pass
                elif buttons[btn_settings].collidepoint(pos):
                    settings_active = True
                    try:
                        pygame.mixer.Sound("sounds/buttonmenu.mp3").play()
                    except:
                        pass
                elif buttons[btn_about].collidepoint(pos):
                    try:
                        pygame.mixer.Sound("sounds/buttonmenu.mp3").play()
                    except:
                        pass
                    try:
                        import tkinter as tk
                        from tkinter import scrolledtext

                        with open("about", "r", encoding="utf-8") as af:
                            content = af.read()

                        def show_about():
                            about_root = tk.Tk()
                            about_root.title("About MiniPyEngine")
                            about_root.geometry("900x900")
                            text_box = scrolledtext.ScrolledText(about_root, wrap=tk.WORD, font=("Arial", 12))
                            text_box.insert(tk.END, content)
                            text_box.config(state=tk.DISABLED)
                            text_box.pack(expand=True, fill='both')
                            about_root.mainloop()

                        show_about()

                    except Exception as e:
                        print("Could not load about:", e)
                elif buttons[btn_exit].collidepoint(pos):
                    try:
                        for p in psutil.process_iter(['pid', 'name', 'cmdline']):
                            cmdline = p.info.get('cmdline')
                            if cmdline and any("main.py" in part or "StartGame.py" in part for part in cmdline):
                                p.terminate()
                    except:
                        pass
                    running = False

pygame.quit()
