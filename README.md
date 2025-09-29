<h1 align="center">
  ⚡️ BeOnePhysics  
  <br>
  <img src="https://media.giphy.com/media/ZVik7pBtu9dNS/giphy.gif" width="200"/>
</h1>

<p align="center">
  <b>Simulasi Medan Listrik Interaktif & Analisis Gaya Coulomb berbasis Python</b><br>
  🌐 Proyek Fisika Digital untuk Pembelajaran & Eksperimen
</p>

---

## ✨ **Fitur Utama**

- 🧲 **Interaksi dua muatan** dengan visualisasi gaya & arah
- 🌌 **Simulasi medan listrik** menggunakan streamplot, quiver, dan heatmap
- 🧮 **Analisis kuantitatif** gaya Coulomb dan medan listrik di titik uji (multi-point)
- 🧠 **Superposisi medan** dari beberapa muatan (total E di sensor)
- 📄 **Export otomatis ke PDF** lengkap dengan rumus, input, hasil, dan gambar simulasi

---

## 🛠️ **Instalasi**

### 1️⃣ Clone Repositori

```bash
git clone https://github.com/username/BeOnePhysics.git
cd BeOnePhysics
```

### 2️⃣ Buat Virtual Environment (Opsional)
python -m venv venv

### Aktifkan Virtual Environment

Windows:
venv\Scripts\activate

Mac / Linux:
source venv/bin/activate

### 4️⃣ Install Dependensi
pip install -r requirements.txt

### 🚀 Cara Menjalankan Program

Jalankan dengan perintah:
```bash 
python main.py
```
Akan muncul menu utama di terminal:
```bash
Pilih satuan posisi input:
Masukkan 'm' untuk meter atau 'cm' untuk centimeter [m/cm, default m]: m

Menu utama:
1) Interaksi Muatan
2) Medan Listrik & Garis Medan
3) Analisis Kuantitatif
4) Superposisi Medan
0) Keluar
Pilih menu (0-4):
```

🧭 Panduan Menu
1️⃣ Interaksi Muatan

Simulasikan dua muatan (Q1 di (0,0) dan Q2 di posisi tertentu).

Tampilkan arah gaya Coulomb antar muatan.

2️⃣ Medan Listrik & Garis Medan

Visualisasi interaktif medan listrik dengan:

Garis medan (streamplot)

Vektor medan (quiver)

Heatmap intensitas (log skala)

3️⃣ Analisis Kuantitatif 🧮

Input muatan sumber (dalam nC)

Masukkan beberapa titik gaya (dengan q_uji) dan titik sensor (tanpa q_uji)

Program otomatis:

Konversi nC ke Coulomb

Tampilkan hasil dengan format ilmiah

Generate PDF laporan lengkap

Contoh:
```bash
Masukkan muatan sumber Q1 (nC) di (0,0): -6
Titik gaya (x y / done): 0.5 0
  Masukkan muatan uji q di titik ini (nC): 2
Titik gaya (x y / done): done
Titik sensor (x y / done): 1.5 0
Titik sensor (x y / done): done

```
Hasil:
```bash
=== HASIL TITIK GAYA ===
Titik Gaya 1: (0.5, 0) m, q_uji=2 nC
  r = 0.5 m
  |E| = 2.16e+02 N/C
  |F| = 4.32e-07 N

```
PDF laporan otomatis disimpan di folder hasil_simulasi_.../.

4️⃣ Superposisi Medan
Masukkan beberapa muatan sumber

Hitung total medan listrik di titik sensor dengan prinsip superposisi

Tampilkan visualisasi dan laporan PDF

Tampilan Simulasi
<p align="center"> <img src="https://media.giphy.com/media/26tPplGWjN0xLybiU/giphy.gif" width="500"/><br> <em>Contoh visualisasi medan listrik</em> </p>

👨‍💻 Dibuat Oleh

BeOnePhysics Team — Proyek Fisika Digital Kelompok 1 🧠
📅 2025 | 🐍 Python 3.10+

📝 Lisensi

MIT License © 2025 BeOnePhysics
Feel free to fork & modify!

<p align="center"> <img src="https://media.giphy.com/media/xT8qBepJQzUj6yHFFK/giphy.gif" width="120"/> <br> <b>“Belajar Fisika Bukan Hanya Menghitung, Tapi Memvisualisasikan.”</b> </p> ```
