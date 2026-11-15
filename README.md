# Proyek Analisis Data Penyewaan Sepeda (Bike Sharing Dataset)

## Latar Belakang Proyek
Sistem penyewaan sepeda merupakan solusi transportasi perkotaan yang sangat dipengaruhi oleh faktor lingkungan, musim, kondisi cuaca, serta ritme aktivitas harian masyarakat. Pemahaman yang mendalam terhadap dinamika permintaan penyewaan diperlukan untuk mengoptimalkan ketersediaan armada sepeda di berbagai stasiun dan menyusun strategi operasional yang efisien.

## Pertanyaan Bisnis
1. **Pengaruh Musim dan Cuaca:** Bagaimana perbandingan volume rata-rata penyewaan sepeda antara musim panas (*Summer*) dan musim dingin (*Winter*) pada kondisi cuaca cerah dibandingkan dengan kondisi cuaca buruk?
2. **Pola Aktivitas Harian & Segmen Pengguna:** Bagaimana perbedaan pola penyewaan sepeda berdasarkan jam (*hourly pattern*) antara hari kerja (*working day*) dan hari libur/akhir pekan (*holiday/weekend*) pada segmen pengguna *casual* dan *registered*?

## Struktur Direktori

submission
├── dashboard
│   ├── main_data.csv
│   └── dashboard.py
├── data
│   ├── day.csv
│   └── hour.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt

## Setup Environment

Membuat Environment menggunakan conda
conda create --name main-ds python=3.9
conda activate main-ds
pip install numpy pandas scipy matplotlib seaborn jupyter streamlit

## Menjalankan Notebook
Import file notebook.ipynb ke dalam Google Colab
Pastikan untuk menekan tombol "Jalankan Semua" untuk memastikan seluruh analisis tereksekusi

## Menjalankan Dashboard Streamlit secara lokal

Masuk ke dalam directory dashboard melalui Terminal
dan jalankan streamlit menggunakan
streamlit run dashboard.py

## Data Wrangling

### Gathering Data
Tahap ini bertujuan untuk memuat dataset penyewaan sepeda ke dalam lingkungan kerja Google Colab agar siap diproses lebih lanjut. Dataset yang digunakan terdiri dari dua tabel utama:
* **`day_df` (`day.csv`):** Berisi catatan agregasi penyewaan sepeda harian selama periode 2011–2012 (731 baris, 16 kolom).
* **`hour_df` (`hour.csv`):** Berisi catatan penyewaan sepeda dengan granularitas per jam pada periode yang sama (17.379 baris, 17 kolom).

### Assessing Data
Proses pemeriksaan kualitas data dilakukan secara menyeluruh pada `day_df` dan `hour_df` untuk mengidentifikasi potensi masalah sebelum masuk ke tahap analisis:
* **Kelengkapan & Duplikasi Data:** Tidak ditemukan nilai kosong (*missing values*) maupun baris duplikat (*duplicate rows*) pada kedua dataset.
* **Kesesuaian Tipe Data:** Kolom `dteday` pada kedua tabel masih terbaca sebagai tipe data `object` (string), sehingga perlu dikonversi menjadi format `datetime` untuk mendukung analisis berbasis waktu.
* **Anomali Nilai & Outlier (Metode IQR):**
  * Ditemukan nilai `0` pada kolom kelembapan (`hum`) yang merupakan anomali pencatatan sensor cuaca (karena kelembapan udara tidak mungkin bernilai 0% di lingkungan terbuka), serta fluktuasi ekstrem pada variabel suhu (`temp` dan `atemp`).
  * Variabel jumlah penyewaan (`casual`, `registered`, dan `cnt`) memiliki sejumlah nilai di atas batas atas IQR, yang mencerminkan lonjakan permintaan alami pada jam sibuk maupun akhir pekan (*natural outliers*), bukan kesalahan pencatatan.

### Cleaning Data
Berdasarkan hasil temuan pada tahap *assessing*, langkah pembersihan data diterapkan sebagai berikut:
1. **Konversi Tipe Data:** Mengubah kolom `dteday` pada `day_df` dan `hour_df` menjadi tipe `datetime64` agar pemfilteran dan agregasi berbasis tanggal berjalan akurat.
2. **Penanganan Anomali Sensor (Imputasi & Interpolasi):**
   * Nilai anomali `hum == 0` diubah menjadi `NaN` terlebih dahulu agar tidak mendistorsi perhitungan statistik.
   * Pada `hour_df`, nilai kosong hasil konversi anomali pada kelembapan (`hum`) dan suhu (`temp`) ditangani menggunakan metode **interpolasi linear** untuk menjaga kontinuitas perubahan cuaca antar-jam.
   * Pada `day_df`, nilai anomali diperbaiki menggunakan **imputasi nilai tengah (median)** berdasarkan kelompok musim dan kondisi cuaca terkait.
3. **Transformasi Label Kategorikal:** Memetakan kode numerik pada kolom `season`, `yr`, `mnth`, `weathersit`, dan `workingday` ke dalam label deskriptif yang informatif untuk memudahkan interpretasi pada tahap eksplorasi dan visualisasi.

## Exploratory Data Analysis (EDA)

Eksplorasi data dilakukan menggunakan rangkuman statistik deskriptif dan pembuatan *Pivot Table* pada `day_df` serta `hour_df` untuk menggali pola utama penyewaan sepeda:
* **Tren Pertumbuhan Tahunan:** Total volume penyewaan sepeda mengalami peningkatan signifikan dari tahun 2011 ke tahun 2012, yang didorong oleh bertambahnya basis pengguna terdaftar (*registered*).
* **Kontras Musim & Kondisi Cuaca:** Musim panas (*Summer*) dan musim gugur (*Fall*) mencatatkan rata-rata penyewaan harian tertinggi, sementara musim dingin (*Winter*) mengalami penurunan volume yang tajam. Pada kedua musim tersebut, cuaca cerah/sedikit berawan menghasilkan permintaan tertinggi, sedangkan hujan ringan maupun salju menekan angka penyewaan secara drastis.
* **Dinamika Segmen Pengguna Berdasarkan Jam:** Pengguna *registered* menyumbang porsi mayoritas penyewaan dengan pola distribusi bimodal yang memuncak pada jam komuter (pukul **08.00** dan **17.00–18.00**) saat hari kerja. Sebaliknya, pengguna *casual* menunjukkan pola unimodal yang meningkat secara bertahap pada siang hingga sore hari (**12.00–16.00**), terutama pada akhir pekan dan hari libur.

## Visualization & Explanatory Analysis

### Pertanyaan 1: Perbandingan Penyewaan Musim Panas vs. Musim Dingin Berdasarkan Cuaca
Visualisasi *grouped bar chart* digunakan untuk membandingkan rata-rata penyewaan harian pada musim panas (*Summer*) dan musim dingin (*Winter*) di setiap kategori cuaca. Grafik menunjukkan bahwa meskipun kondisi cuaca yang cerah mampu mendongkrak minat bersepeda di musim dingin, volume penyewaannya tetap tertinggal jauh dibandingkan musim panas pada kondisi cuaca yang sama. Saat cuaca memburuk (hujan/salju), penurunan permintaan terjadi secara konsisten di kedua musim.

### Pertanyaan 2: Pola Penyewaan Per Jam pada Hari Kerja vs. Hari Libur
Visualisasi *line chart* multi-seri memperlihatkan perbedaan perilaku penggunaan sepeda sepanjang 24 jam:
* **Hari Kerja (*Working Day*):** Terjadi dua lonjakan tajam pada pagi hari (07.00–09.00) dan sore hari (17.00–19.00) yang didominasi oleh pengguna *registered* untuk keperluan mobilitas berangkat dan pulang kerja/sekolah.
* **Akhir Pekan & Hari Libur (*Weekend/Holiday*):** Kurva penyewaan membentuk satu puncak landai di tengah hari (11.00–17.00) dengan proporsi pengguna *casual* yang meningkat pesat untuk aktivitas rekreasi.

## Analisis Lanjutan: Demand Clustering

Untuk mendukung pengambilan keputusan operasional yang lebih terukur, dilakukan pengelompokan tingkat permintaan (*Demand Clustering*) berdasarkan distribusi volume penyewaan (`cnt`), waktu, dan kondisi cuaca ke dalam tiga kategori utama:
* **Low Demand:** Terjadi pada dini hari (00.00–05.00), hari dengan cuaca ekstrem/hujan lebat, serta periode musim dingin bersuhu rendah.
* **Medium Demand:** Terjadi pada jam operasional non-sibuk di siang hari pada hari kerja maupun kondisi cuaca berawan/berkabut.
* **High Demand:** Terkonsentrasi pada jam sibuk komuter di hari kerja serta siang hingga sore hari pada akhir pekan dengan cuaca cerah di musim panas dan musim gugur.

Seluruh hasil pembersihan data dan pengelompokan ini kemudian digabungkan dan diekspor ke dalam file **`main_data.csv`** sebagai sumber data utama bagi *dashboard* interaktif berbasis Streamlit (`dashboard.py`).

## Conclusion & Rekomendasi Bisnis

### Kesimpulan
1. **Musim dan Cuaca sebagai Faktor Penentu Utama:** Penyewaan sepeda mencapai performa puncak pada musim panas (*Summer*) dengan cuaca cerah, dan menurun drastis pada musim dingin (*Winter*) serta saat terjadi hujan/salju. Faktor cuaca buruk memberikan dampak penurunan yang proporsional di semua musim.
2. **Segmentasi Waktu Berdasarkan Tipe Pengguna:** Pengguna *registered* menggunakan layanan sepeda sebagai moda transportasi komuter rutin (puncak pukul 08.00 dan 17.00–18.00 pada hari kerja), sedangkan pengguna *casual* memanfaatkan layanan untuk rekreasi pada siang hingga sore hari di akhir pekan/hari libur.

### Rekomendasi Operasional
* **Optimalisasi Distribusi Armada (*Rebalancing*):** Menambah ketersediaan unit sepeda di area permukiman dan stasiun transit sebelum pukul 07.30 pagi, serta di kawasan perkantoran sebelum pukul 16.30 sore pada hari kerja untuk mengakomodasi lonjakan pengguna *registered*.
* **Penjadwalan Perawatan Rutin:** Memfokuskan pemeliharaan berkala (*maintenance*) dan perbaikan unit sepeda pada periode *Low Demand*, yakni pada musim dingin (*Winter*) serta saat prakiraan cuaca menunjukkan hujan/salju, sehingga kesiapan armada tetap 100% saat memasuki musim semi dan musim panas.
* **Strategi Promosi Akhir Pekan:** Menawarkan paket promo *day-pass* atau diskon penyewaan berkelompok pada rentang pukul 11.00–16.00 di akhir pekan dengan cuaca cerah untuk mengonversi pengguna *casual* menjadi pelanggan *registered*.