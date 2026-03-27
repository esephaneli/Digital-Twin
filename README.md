# 🤖 Bilişsel Dijital İkiz (Cognitive Digital Twin)

Edge AI tabanlı, gerçek zamanlı tam vücut ve bakış takibi uygulaması. RTX 4050 (6GB) gibi kısıtlı donanımlarda 60+ FPS performansla çalışır.

## 🚀 Özellikler

- 🧍‍♂️ **Tam Vücut Takibi**: MediaPipe Holistic ile 33 vücut + 21 el landmark'ı
- 👁️ **Bakış Analizi**: Iris takibi ve kırmızı lazer işaretçi
- 📊 **Biyometrik Analiz**: Omuz stabilitesi ve göz kırpma oranı (EAR)
- ⚡ **Edge AI**: Bulut bağımsız, yerel işleme

## 📋 Gereksinimler

- Python 3.11
- Webcam
- GPU (Önerilen: RTX 3050/4050+)

## 🛠️ Kurulum

```bash
# 1. Repoyu klonla
git clone https://github.com/esephaneli/Digital-Twin.git
cd Digital-Twin

# 2. Sanal ortam oluştur (uv ile)
uv venv --python 3.11
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 3. Bağımlılıkları yükle
uv pip install opencv-python mediapipe==0.10.9 numpy

Kullanım :
# Çalıştır
python main.py

# Kontroller:
# Q - Çıkış
# S - Ekran görüntüsü
# R - Kayıt başlat/durdur

İletişim için Linkedin : https://www.linkedin.com/in/emrehan-%C5%9Fephanelio%C4%9Flu-101a22235/
