# Foto-Kita-Blur
Mendeteksi Hand Gesture dengan Open VC dan Mediapipe

# Peace Blur Camera

Peace Blur Camera adalah project computer vision berbasis Python yang menggunakan OpenCV dan MediaPipe untuk mendeteksi gesture peace sign menggunakan webcam.

Ketika sistem mendeteksi dua tangan yang sama-sama membentuk gesture peace sign, kamera akan secara otomatis memberikan efek Gaussian Blur pada seluruh frame sebagai simulasi fitur Privacy Mode.

## Fitur

* Deteksi tangan secara real-time menggunakan webcam
* Deteksi gesture peace sign
* Mendukung hingga dua tangan
* Mengaktifkan Privacy Mode ketika dua tangan membentuk peace sign
* Memberikan efek Gaussian Blur pada kamera
* Tampilan kamera menggunakan mode mirror
* Tekan `Q` untuk keluar dari aplikasi

## Cara Kerja

```text
Webcam
   |
   v
OpenCV mengambil frame
   |
   v
Konversi BGR ke RGB
   |
   v
MediaPipe Hand Landmarker
   |
   v
Deteksi landmark tangan
   |
   v
Pengecekan gesture peace sign
   |
   v
Apakah terdapat dua tangan dengan gesture peace sign?
   |
   +---- Ya ----> Aktifkan Gaussian Blur
   |
   +---- Tidak -> Kamera tetap normal
```

## Teknologi

| Teknologi     | Fungsi                                |
| ------------- | ------------------------------------- |
| Python        | Bahasa pemrograman utama              |
| OpenCV        | Mengakses webcam dan memproses gambar |
| MediaPipe     | Mendeteksi tangan dan landmark        |
| Gaussian Blur | Memberikan efek blur pada frame       |

## Requirements

Pastikan komputer sudah memiliki:

* Python 3.x
* Webcam
* Koneksi internet saat pertama kali menjalankan program untuk mengunduh model MediaPipe

Install library yang dibutuhkan:

```bash
pip install opencv-python mediapipe
```

## Cara Menjalankan

### 1. Clone Repository

```bash
git clone https://github.com/USERNAME/REPOSITORY.git
```

### 2. Masuk ke Folder Project

```bash
cd REPOSITORY
```

### 3. Install Dependencies

```bash
pip install opencv-python mediapipe
```

### 4. Jalankan Program

```bash
python peace_blur_camera.py
```

Pada penggunaan pertama, program akan mengunduh model MediaPipe:

```text
hand_landmarker.task
```

Jika model sudah tersedia, program dapat langsung menggunakannya.

### 5. Gunakan Gesture

Tunjukkan dua tangan dengan gesture:

```text
Peace Sign     Peace Sign
     V              V
```

Jika kedua tangan terdeteksi sebagai peace sign, Privacy Mode akan aktif dan kamera akan menjadi blur.

Tekan `Q` untuk keluar.

## Logika Deteksi Gesture

Sistem memeriksa posisi landmark pada beberapa jari.

Gesture dianggap sebagai peace sign apabila:

* Telunjuk dalam posisi lurus
* Jari tengah dalam posisi lurus
* Jari manis dalam posisi terlipat
* Kelingking dalam posisi terlipat
* Posisi jempol tidak menjadi syarat utama

Sistem kemudian menghitung jumlah tangan yang membentuk peace sign.

```python
is_double_peace = peace_count >= 2
```

Jika jumlah tangan yang membentuk peace sign minimal dua, Privacy Mode akan aktif.

## Struktur Project

```text
peace-blur-camera/
|
├── peace_blur_camera.py
├── hand_landmarker.task
└── README.md
```

File `hand_landmarker.task` dapat diunduh secara otomatis oleh program apabila file tersebut belum tersedia.

## Pengembangan Selanjutnya

Beberapa pengembangan yang dapat dilakukan:

* Menambahkan suara ketika Privacy Mode aktif
* Menambahkan tombol untuk mengaktifkan dan menonaktifkan sistem
* Menambahkan gesture lainnya
* Mengembangkan fitur blur khusus pada wajah
* Menambahkan Graphical User Interface
* Menambahkan FPS counter
* Menyimpan log aktivitas gesture
* Membuat versi web menggunakan Streamlit
* Mengembangkan sistem privacy berbasis gesture yang lebih kompleks

## Author

**Achmad Tifli**

Information Systems Student
Universitas Hasanuddin

### Interests

* Computer Vision
* Data Analysis
* Software Engineering
* Artificial Intelligence
* Information Systems

