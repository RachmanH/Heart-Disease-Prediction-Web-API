# Heart Disease Prediction — Web API

Project ini merupakan aplikasi untuk memprediksi risiko penyakit jantung menggunakan model Machine Learning yang diintegrasikan dengan REST API dan aplikasi web.

Project ini dibuat untuk praktikum Mata Kuliah **Pemrograman Berbasis Platform**. Fokus utama project ini adalah memahami proses integrasi antara model Machine Learning, REST API, dan aplikasi web.

## Deskripsi Project

Aplikasi ini menggunakan model Machine Learning yang telah dilatih sebelumnya di Google Colab menggunakan notebook `heart-disease-prediction-comparison.ipynb`. Model tersebut disimpan dalam format `.pkl`, kemudian digunakan oleh REST API berbasis Flask untuk memproses data input dari pengguna.

Pengguna mengisi data kesehatan melalui halaman web. Data tersebut dikirim ke API dalam format JSON. API melakukan prediksi menggunakan model Machine Learning, kemudian mengembalikan hasil prediksi ke halaman web.

## Alur Sistem

```
Google Colab
    ↓
Training Model (Logistic Regression vs Random Forest)
    ↓
Export Model Pipeline (.pkl)
    ↓
REST API Flask
    ↓
Aplikasi Web (HTML + CSS + JavaScript)
    ↓
Input Data Pengguna
    ↓
Hasil Prediksi Penyakit Jantung
```

## Fitur Aplikasi

- Membaca model Machine Learning dari file `.pkl`
- Menyediakan endpoint API untuk prediksi penyakit jantung
- Menerima input data dalam format JSON (13 fitur kesehatan)
- Mengembalikan hasil prediksi, probabilitas, dan tingkat risiko dalam format JSON
- Menyediakan tampilan web untuk input data pengguna

## Struktur Folder Project

```
hearth_diseases/
│
├── api/
│   ├── app.py              ← File utama Flask REST API
│   └── requirements.txt    ← Daftar library Python
│
├── model/
│   ├── heart_model.pkl     ← Full pipeline (preprocessor + classifier)
│   ├── model_full.pkl      ← Backup full pipeline
│   ├── scaler.pkl          ← Preprocessor (ColumnTransformer)
│   └── feature_names.json  ← Nama fitur dan info model
│
└── web/
    ├── index.html          ← Struktur halaman web
    ├── style.css           ← Desain tampilan web
    └── script.js           ← Koneksi web ke API Flask
```

## Keterangan Folder

| Folder/File | Keterangan |
|---|---|
| `api/` | Berisi file backend API Flask |
| `api/app.py` | File utama untuk menjalankan REST API |
| `api/requirements.txt` | Daftar library Python yang digunakan |
| `model/` | Berisi file model hasil training dari Google Colab |
| `model/heart_model.pkl` | Full pipeline (preprocessor + classifier) |
| `model/scaler.pkl` | Preprocessor untuk transformasi input |
| `web/` | Berisi file tampilan aplikasi web |
| `web/index.html` | Struktur halaman web |
| `web/style.css` | Desain tampilan web |
| `web/script.js` | Koneksi antara web dan API |

## Dataset

Dataset yang digunakan adalah dataset penyakit jantung berbasis data tabular dari Kaggle. Dataset ini memiliki 14 atribut kesehatan yang digunakan untuk memprediksi risiko penyakit jantung.

Link Dataset : https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset/data

### Atribut Dataset

| No | Atribut | Keterangan |
|---|---|---|
| 1 | `age` | Usia dalam tahun |
| 2 | `sex` | Jenis kelamin (1 = Laki-laki, 0 = Perempuan) |
| 3 | `cp` | Tipe nyeri dada (0–3) |
| 4 | `trestbps` | Tekanan darah saat istirahat (mmHg) |
| 5 | `chol` | Kolesterol serum (mg/dl) |
| 6 | `fbs` | Gula darah puasa >120 mg/dl (1 = Ya, 0 = Tidak) |
| 7 | `restecg` | Hasil elektrokardiografi saat istirahat (0–2) |
| 8 | `thalach` | Detak jantung maksimum yang dicapai |
| 9 | `exang` | Angina yang dipicu olahraga (1 = Ya, 0 = Tidak) |
| 10 | `oldpeak` | Depresi ST yang dipicu olahraga relatif terhadap istirahat |
| 11 | `slope` | Kemiringan segmen ST saat latihan puncak (0–2) |
| 12 | `ca` | Jumlah pembuluh darah utama yang tersumbat (0–4) |
| 13 | `thal` | Hasil tes thalassemia (0–3) |
| 14 | `target` | Label target: 0 = tidak ada penyakit, 1 = ada penyakit |

Kolom `target` hanya digunakan pada proses training. Pada tahap prediksi, pengguna mengisi 13 atribut input.

## Tahap 1: Training Model di Google Colab

Model dilatih di Google Colab menggunakan notebook `heart-disease-prediction-comparison.ipynb`.

### Langkah Training

1. Load dataset `heart.csv`
2. EDA interpretatif (distribusi target, boxplot, histogram, korelasi, outlier detection)
3. Preprocessing:
   - Drop duplicate rows
   - IQR outlier removal pada `trestbps`, `chol`, `thalach`
   - Split data 80/20 (train/test)
   - ColumnTransformer: StandardScaler (numerik) + OneHotEncoder (kategorikal)
4. Model Comparison — Logistic Regression vs Random Forest
5. Pilih best model berdasarkan CV accuracy
6. Export model pipeline ke `.pkl`

### Hasil Perbandingan Model

| Model | Accuracy | CV Accuracy | AUC |
|---|---|---|---|
| Logistic Regression | 89.7% | 84.0% | 0.954 |
| Random Forest | 84.5% | 80.8% | 0.943 |

**Best Model: Logistic Regression** (dipilih berdasarkan CV accuracy tertinggi)

### Output Training

```
model/
├── heart_model.pkl      ← Full pipeline untuk Flask API
├── model_full.pkl       ← Backup full pipeline
├── scaler.pkl           ← Preprocessor terpisah
└── feature_names.json   ← Nama fitur dan info model
```

## Tahap 2: Menyiapkan REST API Flask

Masuk ke folder `api`:

```bash
cd api
```

Buat virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install library yang dibutuhkan:

```bash
pip install flask flask-cors numpy pandas scikit-learn
```

Simpan daftar library:

```bash
pip freeze > requirements.txt
```

## Tahap 3: Menjalankan API Flask

Jalankan perintah berikut dari folder `api`:

```bash
cd api
source venv/bin/activate
python3 app.py
```

Jika berhasil, API akan berjalan di:

```
http://127.0.0.1:5000
```

Buka browser dan akses:

```
http://127.0.0.1:5000/
```

Respons yang benar:

```json
{
  "status": "success",
  "message": "API Prediksi Penyakit Jantung berjalan",
  "endpoint": "/predict",
  "method": "POST"
}
```

## Tahap 4: Menguji Endpoint Prediksi

Endpoint prediksi:

```
POST http://127.0.0.1:5000/predict
```

### Contoh Request JSON

```json
{
  "age": 55,
  "sex": 1,
  "cp": 0,
  "trestbps": 140,
  "chol": 250,
  "fbs": 0,
  "restecg": 1,
  "thalach": 150,
  "exang": 1,
  "oldpeak": 2.0,
  "slope": 1,
  "ca": 2,
  "thal": 3
}
```

### Contoh Response JSON

```json
{
  "status": "success",
  "prediction": 0,
  "result": "Tidak Berisiko Penyakit Jantung",
  "probability": 0.0226,
  "risk_level": "Rendah"
}
```

### Tingkat Risiko

| Probabilitas | Tingkat Risiko |
|---|---|
| ≥ 70% | Tinggi |
| 40% – 69% | Sedang |
| < 40% | Rendah |

## Tahap 5: Menjalankan Tampilan Web

Buka terminal kedua. Dari folder utama project, masuk ke folder `web`:

```bash
cd web
python3 -m http.server 5500
```

Web akan berjalan di:

```
http://localhost:5500
```

Form web memiliki 13 input sesuai fitur dataset. Setelah mengisi semua field dan klik "Prediksi Sekarang", hasil akan ditampilkan dalam box dengan informasi:
- Hasil prediksi (Berisiko / Tidak Berisiko)
- Probabilitas risiko dalam persen
- Tingkat risiko (Tinggi / Sedang / Rendah)

## Ringkasan Cara Menjalankan Project

Gunakan dua terminal secara bersamaan.

### Terminal 1 — Menjalankan API

```bash
cd hearth_diseases/api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Akses API: `http://127.0.0.1:5000/`

### Terminal 2 — Menjalankan Web

```bash
cd hearth_diseases/web
python3 -m http.server 5500
```

Akses web: `http://localhost:5500`

> **Catatan:** Terminal yang menjalankan API Flask tidak boleh ditutup selama aplikasi web digunakan.

## Troubleshooting

### 1. `ModuleNotFoundError: No module named 'flask'`

Aktifkan `venv`, lalu install dependencies:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Web tidak bisa mengakses API

- Pastikan API sudah berjalan di Terminal 1: `http://127.0.0.1:5000`
- Pastikan Flask menggunakan CORS (`from flask_cors import CORS`)
- Pastikan endpoint di `script.js` mengarah ke `http://127.0.0.1:5000/predict`
- Buka web via `http://localhost:5500`, bukan buka file langsung dari browser

### 3. Hasil prediksi error

Pastikan nama field yang dikirim dari web sama dengan yang diminta API (13 field: `age`, `sex`, `cp`, `trestbps`, `chol`, `fbs`, `restecg`, `thalach`, `exang`, `oldpeak`, `slope`, `ca`, `thal`).

## Catatan Penting

Aplikasi ini dibuat untuk tujuan pembelajaran. Hasil prediksi tidak boleh digunakan sebagai diagnosis medis. Sistem ini hanya merupakan simulasi integrasi Machine Learning, REST API, dan aplikasi web.

Keputusan medis tetap harus dilakukan oleh tenaga kesehatan profesional.
