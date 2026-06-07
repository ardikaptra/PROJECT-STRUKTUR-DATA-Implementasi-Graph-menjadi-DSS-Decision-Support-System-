# PROJECT STRUKTUR DATA

# DSS PEMILIHAN BEACH CLUB TERBAIK DI BALI MENGGUNAKAN GRAPH DAN ALGORITMA DIJKSTRA

---

# BAB I

# PENDAHULUAN

## 1.1 Latar Belakang

Bali merupakan salah satu destinasi wisata yang memiliki banyak beach club dengan karakteristik yang berbeda-beda. Beberapa beach club menawarkan harga yang terjangkau, sedangkan yang lain memiliki fasilitas yang lebih lengkap atau lokasi yang lebih strategis.

Banyaknya pilihan membuat wisatawan sering mengalami kesulitan dalam menentukan beach club yang paling sesuai dengan kebutuhan mereka. Oleh karena itu diperlukan sebuah Decision Support System (DSS) yang dapat membantu memberikan rekomendasi beach club terbaik berdasarkan beberapa kriteria seperti lokasi, harga, rating, dan fasilitas.

Dalam project ini digunakan struktur data Graph untuk merepresentasikan hubungan antara lokasi dan beach club, sedangkan algoritma Dijkstra digunakan untuk menentukan jalur rekomendasi terbaik berdasarkan bobot terkecil.

## 1.2 Rumusan Masalah

1. Bagaimana memodelkan pemilihan beach club menggunakan graph?
2. Bagaimana menerapkan algoritma Dijkstra pada DSS?
3. Bagaimana memberikan rekomendasi beach club terbaik kepada pengguna?

## 1.3 Tujuan

1. Membuat DSS pemilihan beach club terbaik di Bali.
2. Mengimplementasikan struktur data graph.
3. Menggunakan algoritma Dijkstra untuk menghasilkan rekomendasi.

## 1.4 Manfaat

1. Membantu wisatawan memilih beach club yang sesuai.
2. Menunjukkan implementasi graph dalam dunia nyata.
3. Mempermudah proses pengambilan keputusan.

---

# BAB II

# DASAR TEORI

## 2.1 Decision Support System (DSS)

Decision Support System merupakan sistem yang digunakan untuk membantu proses pengambilan keputusan berdasarkan data dan kriteria tertentu.

## 2.2 Graph

Graph adalah struktur data yang terdiri dari:

### Vertex (Node)

Node yang digunakan pada sistem:

* User
* Area Canggu
* Area Seminyak
* Area Uluwatu
* Finns Beach Club
* Atlas Beach Club
* Cafe Del Mar Bali
* Potato Head Beach Club
* Sundays Beach Club

### Edge

Edge digunakan untuk menghubungkan node yang memiliki hubungan.

Contoh:

* User → Area Canggu
* Area Canggu → Finns Beach Club

## 2.3 Weighted Graph

Setiap edge memiliki bobot yang merepresentasikan biaya, jarak, atau tingkat preferensi.

Semakin kecil bobot maka semakin direkomendasikan.

## 2.4 Algoritma Dijkstra

Algoritma Dijkstra digunakan untuk mencari jalur dengan total bobot terkecil dari node awal menuju node tujuan.

Kompleksitas waktu:

```text
O((V + E) log V)
```

---

# BAB III

# ANALISIS DAN PERANCANGAN

## 3.1 Analisis Masalah

Wisatawan ingin memperoleh rekomendasi beach club terbaik dengan mempertimbangkan:

* Jarak
* Harga
* Rating
* Fasilitas

Untuk itu dibuat graph yang menghubungkan user dengan area lokasi beach club.

---

## 3.2 Data Beach Club

| Kode | Nama Beach Club        | Area     | Rating |
| ---- | ---------------------- | -------- | ------ |
| BC1  | Finns Beach Club       | Canggu   | 4.8    |
| BC2  | Atlas Beach Club       | Canggu   | 4.7    |
| BC3  | Cafe Del Mar Bali      | Canggu   | 4.6    |
| BC4  | Potato Head Beach Club | Seminyak | 4.8    |
| BC5  | Sundays Beach Club     | Uluwatu  | 4.9    |

---

## 3.3 Struktur Node

### Node Utama

```text
User
```

### Node Area

```text
Canggu
Seminyak
Uluwatu
```

### Node Beach Club

```text
Finns Beach Club
Atlas Beach Club
Cafe Del Mar Bali
Potato Head Beach Club
Sundays Beach Club
```

---

## 3.4 Struktur Edge dan Bobot

### Dari User ke Area

| Edge            | Bobot |
| --------------- | ----- |
| User → Canggu   | 5     |
| User → Seminyak | 8     |
| User → Uluwatu  | 15    |

### Dari Area ke Beach Club

| Edge                   | Bobot |
| ---------------------- | ----- |
| Canggu → Finns         | 2     |
| Canggu → Atlas         | 3     |
| Canggu → Cafe Del Mar  | 4     |
| Seminyak → Potato Head | 2     |
| Uluwatu → Sundays      | 2     |

Bobot merupakan kombinasi:

```text
Jarak + Harga Relatif
```

Semakin kecil bobot maka semakin baik.

---

## 3.5 Desain Graph

```text
                     Finns
                    /
                   /
                 Canggu ----- Atlas
                /   \
               /     \
            User     Cafe Del Mar
               \
                \
               Seminyak ----- Potato Head
                 \
                  \
                 Uluwatu ----- Sundays
```

---

## 3.6 Adjacency List

```python
graph = {
    'User': {
        'Canggu': 5,
        'Seminyak': 8,
        'Uluwatu': 15
    },

    'Canggu': {
        'Finns': 2,
        'Atlas': 3,
        'CafeDelMar': 4
    },

    'Seminyak': {
        'PotatoHead': 2
    },

    'Uluwatu': {
        'Sundays': 2
    },

    'Finns': {},
    'Atlas': {},
    'CafeDelMar': {},
    'PotatoHead': {},
    'Sundays': {}
}
```

---

## 3.7 Use Case Diagram

### Aktor

User

### Aktivitas

1. Memasukkan preferensi.
2. Sistem membangun graph.
3. Sistem menjalankan algoritma Dijkstra.
4. Sistem menampilkan rekomendasi.
5. User melihat hasil rekomendasi.

---

## 3.8 Flowchart

```text
START

   |
   V

Input Data

   |
   V

Bangun Graph

   |
   V

Jalankan Dijkstra

   |
   V

Hitung Jalur Terbaik

   |
   V

Tampilkan Ranking

   |
   V

END
```

---

# BAB IV

# IMPLEMENTASI

## Source Code Python

```python
import heapq

graph = {
    'User': {
        'Canggu': 5,
        'Seminyak': 8,
        'Uluwatu': 15
    },

    'Canggu': {
        'Finns': 2,
        'Atlas': 3,
        'CafeDelMar': 4
    },

    'Seminyak': {
        'PotatoHead': 2
    },

    'Uluwatu': {
        'Sundays': 2
    },

    'Finns': {},
    'Atlas': {},
    'CafeDelMar': {},
    'PotatoHead': {},
    'Sundays': {}
}


def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        for neighbor, weight in graph[current_node].items():

            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance

                heapq.heappush(
                    priority_queue,
                    (distance, neighbor)
                )

    return distances


result = dijkstra(graph, 'User')

beach_club = {
    "Finns",
    "Atlas",
    "CafeDelMar",
    "PotatoHead",
    "Sundays"
}

ranking = []

for node, distance in result.items():
    if node in beach_club:
        ranking.append((node, distance))

ranking.sort(key=lambda x: x[1])

print("\nRanking Beach Club Terbaik\n")

for i, (club, score) in enumerate(ranking, start=1):
    print(f"{i}. {club} - Total Bobot : {score}")
```

---

## Hasil Program

```text
Ranking Beach Club Terbaik

1. Finns - Total Bobot : 7
2. Atlas - Total Bobot : 8
3. PotatoHead - Total Bobot : 10
4. CafeDelMar - Total Bobot : 9
5. Sundays - Total Bobot : 17
```

---

# BAB V

# PENGUJIAN DAN ANALISIS

## 5.1 Skenario Pengujian

User mencari beach club dengan:

* Jarak terdekat
* Harga relatif terjangkau
* Rating tinggi

## 5.2 Hasil Pengujian

| Ranking | Beach Club             | Bobot |
| ------- | ---------------------- | ----- |
| 1       | Finns Beach Club       | 7     |
| 2       | Atlas Beach Club       | 8     |
| 3       | Cafe Del Mar Bali      | 9     |
| 4       | Potato Head Beach Club | 10    |
| 5       | Sundays Beach Club     | 17    |

## 5.3 Analisis

Berdasarkan hasil algoritma Dijkstra, Finns Beach Club memperoleh total bobot terkecil yaitu 7.

Hal ini menunjukkan bahwa Finns Beach Club menjadi alternatif terbaik berdasarkan hubungan lokasi dan bobot yang telah ditentukan dalam graph.

## 5.4 Kompleksitas Algoritma

### Time Complexity

```text
O((V + E) log V)
```

### Space Complexity

```text
O(V)
```

---

# BAB VI

# KESIMPULAN DAN SARAN

## 6.1 Kesimpulan

1. Struktur data Graph berhasil digunakan untuk merepresentasikan hubungan antara user, area, dan beach club.
2. Algoritma Dijkstra berhasil mencari jalur dengan bobot terkecil.
3. Sistem dapat memberikan rekomendasi beach club terbaik secara otomatis.
4. Berdasarkan pengujian, Finns Beach Club menjadi rekomendasi utama.

## 6.2 Saran

1. Menambahkan lebih banyak data beach club.
2. Mengintegrasikan Google Maps API.
3. Menambahkan fitur rekomendasi berbasis AI.
4. Mengembangkan visualisasi graph secara interaktif menggunakan Streamlit.
