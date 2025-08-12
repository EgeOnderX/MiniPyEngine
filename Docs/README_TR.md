[Main README](../README.md)

# MiniPyEngine 1.0.1-S Dil Paketi  

**MiniPyEngine**, 2023 yılında **Alexander Freyr Lúðvíksson** tarafından oluşturulan bir oyun motorunun, büyük ölçüde geliştirilmiş ve yeniden yapılandırılmış versiyonudur.  

Bu sürüm, 2025 yılında **Ege** tarafından MIT Lisansı altında geliştirilmiş ve genişletilmiştir.  

---

## Özellikler  

- Modeller ve dokular için `.obj` ve `.mtl` dosyalarını kullanır. (`.glb` formatını **desteklemez**.)  
- Geniş çözünürlük desteği:  
  - HD (`1280×720`)  
  - Full HD (`1920×1080`)  
  - 2K / QHD (`2560×1440`)  
  - 4K / UHD (`3840×2160`)  
  - 8K (`7680×4320`)  
  - 16K (`15360×8640`)  

---

## MiniPyEngine 1.0.1-S’teki Yenilikler  

- **Game Maker App** düğmesi eklendi, uygulamanın kendisi eklenmedi (**v1.0.3**’te gelecek)  
- Çok oyunculu (multiplayer) kaldırıldı (**ancak hâlâ shortuuid gerektiriyor**)  
- **8K** desteği eklendi, ayrıca eğlence için **16K** çözünürlük desteği eklendi  
- Eğilerek zıplama hatası düzeltildi  
- Çeşitli hata düzeltmeleri ve içsel iyileştirmeler yapıldı  
- Stabilite için VGA ve SVGA çözünürlük desteği kaldırıldı  
- Konsol menüsü eklendi  
- **modulechk** sistemi eklendi  

---

## Bilinen Hatalar  

- Bildirilmiş bir hata yok.  

---

## Kontroller (varsayılan `Player.py`)  

- Hareket: `W`, `A`, `S`, `D`  
- Koşma: `Shift` basılı tut  
- Zıplama: `Space`  
- Eğilme: `Ctrl`  
- Etrafa bakma: Fareyi hareket ettir  
- Ateş etme / Etkileşim: Sol tık  
- Duraklatma menüsü: `Esc`  
- `F3` tuşuna basarak konsolu aç  

---

## Çalıştırma Talimatı  

1. `main.py` dosyasına çift tıkla.  
2. Menüde **Ayarlar** düğmesine tıklayarak çözünürlük ve diğer ayarları yap.  
3. Oyun başlamazsa:  
   - `config` dosyasını bir metin düzenleyici (ör. Not Defteri) ile aç.  
   - Ayarların doğru olduğundan emin ol.  
4. Son olarak, oyunu başlatmak için `StartGame.py` dosyasını çalıştır.  

---

## Ekran Görüntüleri  

### Ana Menü:  

<img width="1919" height="929" alt="main" src="https://github.com/user-attachments/assets/8948a77d-fa41-483a-8725-4326b7e846bf" />  

### Konsol Menüsü:  

<img width="845" height="582" alt="console" src="https://github.com/user-attachments/assets/f1d4bf1a-04ab-419e-8f93-15a3238a2c33" />  

### Modül Doğrulama Sistemi:  

<img width="661" height="252" alt="modulechk" src="https://github.com/user-attachments/assets/a1885e07-20fa-4224-b8fa-ffa2f21b89ec" />  

---

## Sistem Gereksinimleri  

### Minimum:  

- **İşletim Sistemi:** Windows 10 / Linux (Ubuntu 18.04+)  
- **Python:** 3.8+  
- **İşlemci:** Çift çekirdekli 2.0 GHz  
- **RAM:** 80 MB (oyun içi kullanım)  
- **Ekran Kartı:** OpenGL 3.3 destekli dahili grafik  
- **Depolama:** 20 MB boş alan  
- **Bağımlılıklar:**  
  `pygame`, `PyOpenGL`, `numpy`, `***shortuuid***`, `psutil`  

> NOT: shortuuid yalnızca çok oyunculu için gerekli sanabilirsiniz, ancak kademeli olarak kaldırıldığı için hâlâ bozulmaları önlemek amacıyla kullanılmaktadır.  

---

## Teknik Özellikler  

MiniPyEngine, gelişmiş grafikler için **modern OpenGL** ve özel GLSL shader’lar kullanır, sabit işlevli grafik hattının ötesine geçer.  
Shader’lar çalışma zamanında `shaders/` klasöründen derlenir.  

Kendi oyununuzu oluşturmak için:  
- `Player.py` dosyasını düzenleyin  
- `.obj`, `.mtl` ve doku dosyaları ekleyin  
- Nesnelerinizi `objects/` klasörüne kaydedin  
- `level1.py` dosyasını düzenleyerek kendi haritanızı yapabilirsiniz  

> NOT: Sadece kutularla dolu, komik bir harita istiyorsanız, `maps` klasöründeki level1 dosyasını orijinal level1 ile değiştirin  

### Ses Sistemi:  
Sadece örnek sesler içerir.  

---

## Konsol Komutları  

- `god` → Tanrı Modunu açar (can değeri 9999 olur).  
- `noclip` → Duvarlardan geçmenizi sağlar.  
- `nocrouch` → Eğilme özelliğini kapat/aç.  
- `nojump` → Zıplama özelliğini kapat/aç.  
- `exit` → Konsolu kapatır.  

---

## Lisans  

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

## Katkıda Bulunanlar  

- @OwnderDuck  

---

## Gelecek Sürümler İçin Planlanan Özellikler  

- Daha iyi performans ve optimizasyon  
- Geliştirilmiş grafik/çizim sistemi  
- Ek platform desteği  
- Tam harita dosya sistemi  
- NPC sistemi  
- Genişletilmiş dokümantasyon ve eğitimler  

---

Eğer bu projeyi indirdiyseniz veya kullandıysanız, **MiniPyEngine**’i denediğiniz için teşekkürler!
