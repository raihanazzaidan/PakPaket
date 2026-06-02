# 📦 pakPaket - Sistem Manajemen Logistik & Tracking

pakPaket adalah sebuah aplikasi web sistem manajemen logistik dan pelacakan (*tracking*) pengiriman barang berbasis Django. Aplikasi ini dirancang untuk memfasilitasi tiga peran pengguna utama: **Customer**, **Kurir**, dan **Admin** dengan alur kerja yang terintegrasi secara *real-time*.

Proyek ini dikembangkan sebagai pemenuhan Tugas Akhir Mata Kuliah Pemrograman Berorientasi Objek (PBO) di Program Studi Teknik Informatika, Universitas Negeri Surabaya.

---

## ✨ Fitur Utama

* **Multi-Role Authentication:** Sistem *login* dan *register* kustom yang membedakan hak akses dan *dashboard* untuk Admin, Kurir, dan Pelanggan.
* **Smart Resi Generator:** Pembuatan nomor resi secara otomatis (contoh: `SBY-A4F89K2P`) berdasarkan kota tujuan pengiriman saat paket didaftarkan.
* **Kalkulator Volumetrik:** Penghitungan otomatis ongkos kirim yang membandingkan berat fisik dan berat dimensi/volumetrik paket.
* **Real-time Tracking Timeline:** Pelacakan riwayat perjalanan paket dengan visualisasi *timeline* yang responsif.
* **Kurir Task Management:** Kurir dapat mengambil (*pick-up*) paket yang siap dikirim dan menyelesaikan pesanan (konfirmasi penerimaan).

## 🛠️ Teknologi yang Digunakan

* **Backend:** Django Framework (Python)
* **Frontend:** HTML5, Tailwind CSS
* **Database:** MySQL
* **Paradigma Utama:** Object-Oriented Programming (OOP)

---

## 🎯 Implementasi Konsep OOP (PBO)

Proyek ini dibangun dengan menerapkan 4 konsep utama Object-Oriented Programming yang melekat pada arsitektur bawaan Django ORM (*Object-Relational Mapping*):

1. **Inheritance (Pewarisan)**
   Pewarisan digunakan secara ekstensif dalam pembentukan entitas *database*.
   * *Class* `User` mewarisi seluruh kemampuan autentikasi (*login*, *hashing*, dll) dari *class* induk `AbstractUser` milik Django.
   * *Class* `Paket`, `Kurir`, `Customer`, dan lainnya mewarisi *behavior* dari `models.Model`, yang memberikan mereka kemampuan bawaan untuk berinteraksi dengan database (seperti `.save()`, `.delete()`).

2. **Encapsulation (Enkapsulasi)**
   Enkapsulasi diterapkan dengan menyembunyikan proses bisnis yang kompleks dari jangkauan eksternal (*Controller/Views*).
   * **Contoh:** Logika *generate* nomor resi unik (penggabungan kode kota dan angka *random*) disembunyikan di dalam *method* pada *class* `Paket`. *Controller* hanya bertugas memberikan perintah `paket.save()`, sedangkan proses rumitnya dibungkus aman di dalam *model*.

3. **Abstraction (Abstraksi)**
   Abstraksi digunakan untuk menyembunyikan kompleksitas eksekusi tingkat rendah (seperti *query* SQL murni) menjadi antarmuka objek yang mudah dibaca.
   * **Contoh:** Penggunaan antarmuka `Paket.objects.create(...)` atau `User.objects.filter(...)` untuk memanipulasi *database* tanpa perlu menulis perintah SQL secara manual.

4. **Polymorphism (Polimorfisme)**
   Polimorfisme diimplementasikan melalui teknik *Method Overriding*.
   * **Contoh:** Menimpa (*override*) fungsi bawaan `save()` pada *class* `Paket`. Fungsi `save()` kini memiliki bentuk/perilaku baru: sebelum melakukan penyimpanan standar ke *database* (`super().save()`), ia juga akan mengeksekusi logika pencetakan nomor resi otomatis jika paket tersebut baru dibuat.

---

## 🚀 Cara Menjalankan Proyek Secara Lokal

Ikuti langkah-langkah di bawah ini untuk menjalankan aplikasi pakPaket:

**1. Clone repositori**
```bash
git clone https://github.com/raihanazzaidan/final-pbo
cd final-pbo

```

**2. Buat Virtual Environment (venv)**

```bash
python -m venv env

```

**3. Aktifkan venv**

* Untuk Mac/Linux:
```bash
source env/bin/activate

```


* Untuk Windows:
```bash
.\env\Scripts\activate

```



**4. Install Dependencies**

```bash
pip install -r requirements.txt

```

**5. Konfigurasi Database**

* Buka file `pakPaket/settings.py`.
* Pada bagian `DATABASES`, sesuaikan `USER` dan `PASSWORD` dengan konfigurasi MySQL milikmu.
* Buat database baru (kosong) di MySQL dengan nama `pakPaket`.
* Lakukan migrasi database dengan menjalankan perintah berikut:
```bash
python manage.py makemigrations
python manage.py migrate

```



**6. Buat Akun Superuser**
Ketik perintah di bawah ini dan ikuti instruksi yang muncul di terminal (disarankan menggunakan username: `superadmin`):

```bash
python manage.py createsuperuser

```

**7. Jalankan Server & Tambah Akun Admin**

```bash
python manage.py runserver

```

* Buka browser dan akses `http://127.0.0.1:8000/login`.
* Login menggunakan akun `superadmin` yang baru saja dibuat.
* Akses url `http://127.0.0.1:8000/adm/register` untuk mendaftarkan User baru dengan *role* **Admin**.

**8. Setup Data Master**

* Login sebagai **Admin** yang baru saja didaftarkan.
* Tambahkan data **Gudang**, **Tipe Layanan**, dan daftarkan akun **Kurir** melalui menu yang tersedia di Dashboard Admin.

**9. Skenario Penggunaan**

* **Customer:** Kembali ke halaman Login, klik "Daftar Sekarang" untuk membuat akun pelanggan, lalu login untuk mulai mengirim paket.
* **Kurir:** Login menggunakan akun kurir (yang telah dibuat oleh Admin) untuk melihat daftar paket dan memperbarui status pelacakan paket.