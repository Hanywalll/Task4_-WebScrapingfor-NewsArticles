📰 Web Scraping for News Articles (Detik.com)
📌 Deskripsi Proyek

Proyek ini adalah aplikasi web scraping berbasis Python yang dirancang untuk mengambil artikel berita dari Detik.com
.
Dengan memasukkan kata kunci pencarian, pengguna dapat memperoleh daftar artikel yang relevan beserta detailnya.

✨ Fitur

🔍 Menerima input berupa kata kunci pencarian.

📑 Mengambil detail artikel:

Judul

Tautan gambar

Teks isi

Waktu publikasi

📄 Mendukung pagination hingga 3 halaman hasil pencarian.

🧹 Menghapus iklan dan tag HTML yang tidak relevan.

⚡ Menggunakan requests dan BeautifulSoup sebagai inti scraping.

🗄️ Database

Proyek ini terhubung dengan MySQL untuk menyimpan umpan balik pengguna.

Nama Database: user_auth

Nama Tabel: feedback

👉 Skrip SQL untuk membuat tabel tersedia secara terpisah dalam repositori.

🚀 Cara Menjalankan
1. Persiapan Lingkungan

Pastikan Python sudah terinstal, lalu pasang library yang diperlukan:

pip install requests beautifulsoup4 mysql-connector-python

2. Jalankan Skrip
python your_script_name.py

3. Input Pencarian

Masukkan kata kunci saat diminta, lalu skrip akan otomatis mengambil artikel dari Detik.com.

⚙️ Penjelasan Teknis

requests digunakan untuk mengirim HTTP GET request ke halaman pencarian Detik.com.

BeautifulSoup digunakan untuk parsing HTML dan mengekstrak data dengan CSS selector.

Looping & pagination dipakai untuk menavigasi hasil pencarian hingga 3 halaman.

Error handling diimplementasikan untuk menangani:

Koneksi gagal

Respons kosong

Elemen HTML yang hilang
