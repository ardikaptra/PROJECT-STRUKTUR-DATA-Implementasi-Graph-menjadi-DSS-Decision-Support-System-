# 🏖️ Bali Beach Club Decision Support System (DSS)

Aplikasi Sistem Pendukung Keputusan (DSS) menggunakan struktur data **Graph** dan **Algoritma Dijkstra** untuk merekomendasikan Beach Club di Bali berdasarkan kriteria wilayah, rating, dan budget minimum spend, sekaligus mencari rute perjalanan tercepat antar destinasi.

---

## 🚀 Cara Menjalankan Aplikasi
1. Buka folder proyek ini di File Explorer komputer lu.
2. Klik **Address Bar** (kotak alamat folder) di bagian atas, ketik `cmd`, lalu tekan **Enter**.
3. Di dalam jendela CMD yang muncul, langsung ketik perintah ini untuk membuka aplikasi:
   ```bash
   python -m streamlit run app.py

```

---

## 🛠️ Deskripsi Berkas & Struktur Kode

* **`app.py`** — Berkas utama komponen antarmuka (*User Interface*), penanganan peta interaktif Bali, kontrol input filter kriteria DSS, serta fitur ekspor laporan ke format `.CSV`.
* **`dijkstra.py`** — Berkas komponen logika inti yang mengimplementasikan kelas Graph, algoritma pencarian rute terpendek Dijkstra, dan perhitungan fungsi *Degree Centrality*.
* **`dataset.py`** — Berkas basis data statis yang menyimpan seluruh metadata spasial (koordinat GPS), finansial (*min_spend*), kualitas (*rating*), serta matriks hubungan antar rute jalan.

---

## 📋 Penjelasan Sistem (Kesesuaian Parameter Graf & Algoritma)

### 1. Pemodelan Struktur Data Graph

* **Jenis Graph:** Menggunakan **Directed Weighted Graph** (Graf Berarah dan Berbobot). Sifat berarah (*Directed*) mewakili sistem alur lalu lintas satu arah atau jalur penyeberangan laut khusus. Sifat berbobot (*Weighted*) mewakili nilai biaya waktu tempuh dalam satuan **Menit**.
* **Representasi Memory:** Menggunakan **Adjacency List** (Daftar Ketetanggaan) berbasis struktur data *Dictionary* di Python. Pendekatan ini dipilih karena sangat efisien dalam menghemat penggunaan memori untuk memetakan jaringan rute jalan raya (*Sparse Graph*).
* **Entitas Simpul (Nodes/Vertex):** Total terdapat 30 simpul terdaftar yang terdiri dari 27 titik lokasi Beach Club aktif, 2 simpul infrastruktur transit (`Main Highway Hub` & `Sanur Port Hub`), serta 1 simpul posisi dinamis pengguna yang dilacak via GPS.

### 2. Algoritma Optimasi & Analisis

* **Mekanisme Dijkstra Min-Heap:** Proses pencarian lintasan terpendek dioptimalkan menggunakan struktur data **Min-Heap Priority Queue (`heapq`)**. Hal ini memangkas kompleksitas waktu menjadi lebih efisien, yaitu **$O((V + E) \log V)$** (di mana $V$ adalah jumlah simpul dan $E$ adalah jumlah sisi), jauh lebih cepat dibandingkan Dijkstra konvensional berbasis array biasa ($O(V^2)$).
* **Degree Centrality:** Fitur analisis jaringan untuk menghitung jumlah total koneksi masuk (*In-Degree*) dan keluar (*Out-Degree*) pada setiap simpul guna menentukan titik hub transportasi pariwisata yang paling krusial di Bali.
* **Sistem Keputusan Multi-Kriteria:** Menyaring alternatif destinasi secara berlapis berdasarkan wilayah geografis, batas atas pengeluaran finansial, dan batas bawah kualitas performa tempat sebelum rute tercepatnya dikalkulasi oleh mesin Dijkstra.

---

## 👥 Anggota Kelompok / Kontributor

* **[I Wayan Ardika Putra Widnyana]** - [2501010108]
* **[Putu Intan Cahyanti Putri]** - [2501010046]
* **[I Gede Aris Pratama Putra]** - [2501010011]
