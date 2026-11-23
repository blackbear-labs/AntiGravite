# AntiGravite: AI "What If" Motion Video Generator (FFmpeg)

Otomasi pembuatan video motion animasi vertikal (9:16 Shorts/Reels/TikTok) bertema **"What If"** menggunakan kombinasi Generative AI dan FFmpeg (Ken Burns Camera Motion, Subtitle Burn-in, & Audio Stitching).

---

## 🚀 Fitur Utama
- **Automated Ken Burns Effect:** Efek gerak kamera sinematik (Slow Zoom-In, Zoom-Out, Pan Horizontal, Pan Vertical) dari gambar statis via filter FFmpeg `zoompan`.
- **Text & Subtitle Overlay:** Render teks hook dan subtitle dramatis langsung ke dalam video.
- **Transisi & Concat:** Penggabungan multi-scene dengan transisi fade halus.
- **Audio Synchronization:** Penggabungan voiceover dan background music otomatis.

---

## 📁 Struktur Proyek
```text
AntiGravite/
│
├── assets/
│   ├── images/          # Simpan gambar scene (scene1.png, scene2.png, dst.)
│   └── audio/           # voiceover.mp3 dan bgm.mp3 (opsional)
│
├── output/              # Hasil video final
├── create_motion_video.py # Script utama otomasi FFmpeg
├── prompts_what_if.md   # Template prompt visual & narasi per scene
├── requirements.txt     # Dependensi Python
└── README.md
```

---

## 🛠️ Persyaratan Sistem
1. **Python 3.8+**
2. **FFmpeg** terpasang di sistem dan terdaftar di `PATH`.
   - Cek dengan: `ffmpeg -version`

---

## 🎬 Cara Menjalankan

1. Masukkan gambar per adegan ke folder `assets/images/`:
   - `scene1.png`, `scene2.png`, `scene3.png`, `scene4.png`, `scene5.png`
2. Jalankan script generator:
   ```bash
   python create_motion_video.py
   ```
3. Video final akan otomatis tersimpan di folder `output/final_what_if_video.mp4`.
