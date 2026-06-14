# Dashboard Business Intelligence BPPI untuk Prioritas Promosi Pariwisata

Dashboard Business Intelligence berbasis Streamlit dan Python untuk membantu
Badan Promosi Pariwisata Indonesia (BPPI) menyusun pertimbangan awal prioritas
promosi berdasarkan 437 destinasi, 9.597 pasangan pengguna-destinasi unik yang
mewakili 9.921 observasi rating bersih, 300 pengguna, serta 100 paket wisata.
Arsitektur telah dipisahkan menjadi UI, service data, ETL, dan database agar
mudah dikembangkan menuju MySQL.

Dashboard hanya menggunakan informasi yang tersedia dalam dataset. Dashboard
tidak mengukur jumlah kunjungan, keberhasilan kampanye, pendapatan, atau ROI
promosi karena variabel tersebut tidak tersedia.

## Aturan kualitas data

Dataset rating memiliki 10.000 baris sumber. Proses pembersihan menghapus 79
duplikat persis, kemudian menggabungkan rating berulang untuk pasangan pengguna
dan destinasi yang sama menggunakan rata-rata karena dataset tidak memiliki
tanggal untuk menentukan rating terbaru. Hasil akhirnya adalah 9.597 pasangan
pengguna-destinasi unik yang mewakili 9.921 observasi rating setelah penghapusan
duplikat persis.

Validasi juga memastikan rating berada pada skala 1-5, harga tidak negatif,
serta seluruh `User_Id` dan `Place_Id` rating memiliki relasi yang valid.
Nama destinasi pada dataset paket dinormalisasi menggunakan crosswalk eksplisit
ke nama master destinasi; proses ini memperbaiki 5 perbedaan format dan 8 nama
alias tanpa menggunakan pencocokan fuzzy otomatis.

## Menjalankan aplikasi

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
streamlit run app.py
```

Dashboard saat ini menyediakan empat halaman:

- **Dashboard Overview**
- **Destinasi & Kategori**
- **Paket & Harga**
- **Halaman 5** untuk pengembangan berikutnya

Dashboard dilengkapi filter global untuk kota, kategori, harga tiket, rating
referensi dataset, dan kelompok usia.

Dashboard Overview juga menampilkan komponen actionable berbasis benchmark data
aktif: KPI keputusan, alert destinasi yang perlu validasi, distribusi status
prioritas, serta daftar rekomendasi tindakan untuk BPPI.

Dataset tidak memiliki kolom tanggal, sehingga dashboard tidak membuat visualisasi
tren waktu maupun Gantt chart yang tidak didukung data. Seluruh batas kuartil
merupakan benchmark analitis dari data aktif, bukan target resmi BPPI.

## Menyiapkan MySQL dan ETL

1. Instal dan jalankan MySQL.
2. Salin `.env.example` menjadi `.env`, lalu isi kredensial database.
3. Jalankan ETL. Perintah ini menjalankan seluruh tahap, membuat database dan
   star schema, lalu memuat seluruh CSV:

```bash
python3 -m etl.load_csv
```

Source code ETL dipisahkan berdasarkan tahap:

- `etl/extract.py`: membaca empat CSV sumber.
- `etl/transform.py`: membersihkan, memvalidasi, dan membentuk tabel star schema.
- `etl/load.py`: membuat schema dan memuat tabel hasil transformasi ke MySQL.
- `etl/load_csv.py`: entry point yang menjalankan Extract, Transform, lalu Load.

4. Setelah ETL berhasil, aktifkan MySQL sebagai sumber dashboard:

```env
DB_ENABLED=true
```

Star schema terdiri dari `dim_city`, `dim_category`, `dim_destination`,
`dim_user`, `dim_package`, `fact_rating`, dan `bridge_package_destination`.
Jika MySQL tidak tersedia, dashboard otomatis menggunakan fallback CSV.
