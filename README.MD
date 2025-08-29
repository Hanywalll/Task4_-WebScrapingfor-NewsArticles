Web Scraping for News Articles
Proyek
Proyek ini adalah skrip Python yang dirancang untuk melakukan web scraping artikel berita dari situs https://www.detik.com/.

Fitur
Menerima input berupa kata kunci pencarian.

Mengambil detail artikel:

Judul

Tautan gambar

Teks isi

Waktu publikasi

Mendukung penomoran halaman (pagination) hingga 3 halaman.

Menghilangkan iklan atau tag HTML yang tidak relevan.

Menggunakan requests dan BeautifulSoup untuk fungsionalitas inti.

Database
Proyek ini terhubung ke database MySQL. Berikut adalah detailnya:

Nama Database: user_auth

Nama Tabel: feedback

Skrip SQL untuk membuat tabel ini harus disediakan secara terpisah di repositori.

Panduan Penggunaan
Pastikan Anda telah menginstal semua library yang diperlukan:
pip install requests beautifulsoup4

Jalankan skrip Python dengan perintah berikut:
python your_script_name.py

Masukkan kata kunci pencarian saat diminta.

Penjelasan Teknis
Skrip menggunakan requests untuk mengirim permintaan GET ke URL pencarian Detik.com.

BeautifulSoup digunakan untuk mengurai konten HTML yang diterima dan mengekstrak data yang relevan menggunakan selektor CSS.

Looping digunakan untuk menavigasi halaman hasil pencarian berikutnya.

Pencegahan kesalahan (error handling) diimplementasikan untuk menangani kasus seperti koneksi gagal, respons kosong, atau elemen yang hilang.
