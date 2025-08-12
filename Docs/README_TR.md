[Main README](README.md)
###### Türkçe sürümünü görüntülüyorsunuz.
---

# 🎮 MiniPyEngine
# Bu sürümün desteği yakın zamanda kalkacaktır tüm dillerin tek bir depoda  (minipyengine) deposunda birleştirilmesli planlanmaktadır!
**MiniPyEngine**, ilk olarak Alexander Freyr Lúðvíksson tarafından 2023'te geliştirilen bir oyun motorunun yeniden yapılandırılmış ve genişletilmiş halidir.  
Bu versiyon **Ege** tarafından 2025 yılında MIT Lisansı altında geliştirilmiştir.

> ⚠️ **UYARI**  
> Bu depo: https://github.com/mitoschan/MiniPyEngine-Turkce-Turkish-Edition , orijinal MiniPyEngine projesinin izinsiz bir kopyasıdır.  
> ✅ Gerçek ve tek resmi proje burada yer almaktadır:  
> [https://github.com/EgeOnderX/MiniPyEngine](https://github.com/EgeOnderX/MiniPyEngine)  
>
> ⚖️ Bu repo hakkında GitHub'a resmi **DMCA bildirimi yapılmıştır.**  
> Telif hakkı ihlali nedeniyle işlem süreci başlatılmıştır.
> Lütfen orijinal projeyi kullanın, sahte sürümlerden uzak durun.

---

> ⚠️ **WARNING: Copyright Infringement**  
> This repository: https://github.com/mitoschan/MiniPyEngine-Turkce-Turkish-Edition  is an **unauthorized copy** of the official MiniPyEngine project.  
> ✅ The only legitimate version is hosted at:  
> [https://github.com/EgeOnderX/MiniPyEngine](https://github.com/EgeOnderX/MiniPyEngine)  
>
> ⚖️ A **DMCA takedown notice has been filed** with GitHub for copyright violation.  
> Legal review is in progress. Use only the original project, not unauthorized copies.

---

## 🚀 Özellikler

- `.obj` ve `.mtl` dosya formatlarını kullanır. `.glb` desteği **yoktur**.  
- Çok oyunculu mod **desteklenmektedir**.

**Desteklenen çözünürlükler:**
- VGA (640×480)
- SVGA (800×600)
- HD (1280×720)
- Full HD (1920×1080)
- 2K QHD (2560×1440)
- 4K UHD (3840×2160)

---

## 🛠️ Değişiklikler ve Geliştirmeler

- Orijinal kod tabanındaki hatalar düzeltildi  
- Varsayılan olarak tam ekran modu eklendi  
- Yeni ve kullanıcı dostu ana menü oluşturuldu  
- Serbest bakış (mouse-look) sistemi düzeltildi  
- ...

---

## 🐞 Bilinen Hatalar

- Şu anda bilinen herhangi bir hata yok.

---

## 🎮 Oynanış (Varsayılan Player.py ile)

- **W, A, S, D:** Hareket  
- **Shift:** Koş  
- **Space:** Zıpla  
- **Ctrl:** Eğil  
- **Fare:** Bak ve nişan al  
- **Sol Tıklama:** Ateş et veya etkileşim kur  
- **Esc:** Duraklatma menüsünü aç

---

## ⚙️ Başlatma Adımları

1. `main.py` dosyasını çift tıklayın  
2. Ayarlar butonunu kontrol edin  
3. Çalışmazsa `config` dosyasını bir metin düzenleyiciyle açın  
4. Ardından `StartGame.py` dosyasını çalıştırarak başlatın

---

## 💻 Sistem Gereksinimleri

**MiniPyEngine** için minimum sistem gereksinimleri:

- **İşletim Sistemi:** Windows 10, Linux (Ubuntu 18.04+ önerilir)  
- **Python:** 3.8  
- **CPU:** Çift çekirdek 2.0 GHz  
- **RAM:** 80 MB (sadece oyun için)  
- **GPU:** OpenGL 3.3 destekli entegre grafik  
- **Depolama:** 20 MB boş alan  
- **Bağımlılıklar:** `pygame`, `PyOpenGL`, `numpy`, `shortuuid`, `psutil`

---

## 🧪 Teknik Detaylar

- Modern OpenGL + özel GLSL shader'ları kullanır  
- Shader'lar `shaders/` klasöründen yüklenip çalıştırma sırasında derlenir  
- Kendi oyununuzu oluşturmak için:  
  - `Player.py` dosyasını düzenleyin  
  - `.obj`, `.mtl`, ve doku dosyalarınızı ekleyin  
  - Nesneleri `objects` klasörü altında tanımlayın

---

## 🤝 Katkıda Bulunanlar

- README dosyasını Çince’ye çeviren: @OwnderDuck

---

## 📄 Lisans

MIT Lisansı altında yayınlanmıştır.  
- Orijinal geliştirici: Alexander Freyr Lúðvíksson (2023)  
- Geliştirici: Ege Onder (2025)

---

## 🌟 Gelecek Sürümler

Geliştirme **aktif** olarak sürmektedir.  
Planlanan özellikler (1.1.0-S kararlı sürüm):

- Daha yüksek performans ve optimizasyon  
- Gelişmiş grafik / render yapısı  
- Ek çözünürlük ve platform desteği  
- Detaylı belgeler ve eğitim kaynakları  
- Ses sistemi desteği  
- Gelişmiş çok oyunculu altyapı  
- Harita dosyası yükleyici  
- NPC desteği  

---

🎉 MiniPyEngine’i denediğiniz için teşekkürler!

