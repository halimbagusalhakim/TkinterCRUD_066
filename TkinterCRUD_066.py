# Mengimpor library yang dibutuhkan
import sqlite3  # Library untuk mengelola database SQLite
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk  # Library untuk GUI

# Fungsi untuk membuat database dan tabel
def create_database():
    # Membuat atau membuka file database SQLite
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka/terhubung dengan file database 'nilai_siswa.db'
    cursor = conn.cursor()  # Membuat objek cursor untuk eksekusi query SQL
    # Membuat tabel 'nilai_siswa' jika belum ada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- ID otomatis
            nama_siswa TEXT, -- Nama siswa
            biologi INTEGER, -- Nilai Biologi
            fisika INTEGER, -- Nilai Fisika
            inggris INTEGER, -- Nilai Inggris
            prediksi_fakultas TEXT -- Prediksi Fakultas berdasarkan nilai
        )
    ''')  # Membuat tabel dengan kolom dan tipe data yang sesuai
    conn.commit()  # Menyimpan perubahan ke database
    conn.close()  # Menutup koneksi database

# Fungsi untuk mengambil data dari database
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')  # Terhubung ke database
    cursor = conn.cursor()  # Membuat objek cursor
    cursor.execute("SELECT * FROM nilai_siswa")  # Mengambil semua data dari tabel
    rows = cursor.fetchall()  # Menyimpan data dalam bentuk list
    conn.close()  # Menutup koneksi database
    return rows  # Mengembalikan data

# Fungsi untuk menyimpan data baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Terhubung ke database
    cursor = conn.cursor()  # Membuat objek cursor
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))  # Query untuk menambahkan data baru
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi database

# Fungsi untuk memperbarui data di database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Terhubung ke database
    cursor = conn.cursor()  # Membuat objek cursor
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))  # Query untuk memperbarui data berdasarkan ID
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi database

# Fungsi untuk menghapus data dari database
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')  # Terhubung ke database
    cursor = conn.cursor()  # Membuat objek cursor
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))  # Query untuk menghapus data berdasarkan ID
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi database

# Logika prediksi fakultas berdasarkan nilai
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"  # Prediksi fakultas jika nilai Biologi paling tinggi
    elif fisika > biologi and fisika > inggris:
        return "Teknik"  # Prediksi fakultas jika nilai Fisika paling tinggi
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"  # Prediksi fakultas jika nilai Inggris paling tinggi
    else:
        return "Tidak Diketahui"  # Jika nilai seimbang atau tidak memenuhi kriteria

# Fungsi untuk menambahkan data baru ke database
def submit():
    try:
        nama = nama_var.get()  # Mengambil input nama siswa
        biologi = int(biologi_var.get())  # Mengambil dan mengonversi input Biologi ke integer
        fisika = int(fisika_var.get())  # Mengambil dan mengonversi input Fisika ke integer
        inggris = int(inggris_var.get())  # Mengambil dan mengonversi input Inggris ke integer

        if not nama:  # Validasi input nama
            raise Exception("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)  # Hitung prediksi fakultas
        save_to_database(nama, biologi, fisika, inggris, prediksi)  # Simpan data ke database

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")  # Notifikasi sukses
        clear_inputs()  # Hapus input
        populate_table()  # Perbarui tabel di GUI
    except ValueError as e:  # Tangani kesalahan input
        messagebox.showerror("Error", f"Input tidak valid: {e}")

# Fungsi untuk memperbarui data yang dipilih
def update():
    try:
        if not selected_record_id.get():  # Validasi jika belum ada data yang dipilih
            raise Exception("Pilih data dari tabel untuk di-update!")

        record_id = int(selected_record_id.get())  # Mengambil ID data yang dipilih
        nama = nama_var.get()  # Mengambil input nama siswa
        biologi = int(biologi_var.get())  # Mengambil nilai Biologi
        fisika = int(fisika_var.get())  # Mengambil nilai Fisika
        inggris = int(inggris_var.get())  # Mengambil nilai Inggris

        if not nama:  # Validasi input nama
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)  # Hitung prediksi fakultas
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)  # Perbarui data di database

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")  # Notifikasi sukses
        clear_inputs()  # Hapus input
        populate_table()  # Perbarui tabel di GUI
    except ValueError as e:  # Tangani kesalahan input
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menghapus data yang dipilih
def delete():
    try:
        if not selected_record_id.get():  # Validasi jika belum ada data yang dipilih
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())  # Mengambil ID data yang dipilih
        delete_database(record_id)  # Hapus data berdasarkan ID
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")  # Notifikasi sukses
        clear_inputs()  # Hapus input
        populate_table()  # Perbarui tabel di GUI
    except ValueError as e:  # Tangani kesalahan input
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk membersihkan input di form
def clear_inputs():
    nama_var.set("")  # Hapus input nama
    biologi_var.set("")  # Hapus input nilai Biologi
    fisika_var.set("")  # Hapus input nilai Fisika
    inggris_var.set("")  # Hapus input nilai Inggris
    selected_record_id.set("")  # Hapus ID data yang dipilih

# Fungsi untuk mengisi tabel di GUI dengan data dari database
def populate_table():
    for row in tree.get_children():  # Bersihkan data lama di tabel
        tree.delete(row)
    for row in fetch_data():  # Ambil data dari database dan tambahkan ke tabel
        tree.insert('', 'end', values=row)

# Fungsi untuk mengisi form berdasarkan data yang dipilih di tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]  # Ambil data yang dipilih
        selected_row = tree.item(selected_item)['values']  # Dapatkan nilai data

        selected_record_id.set(selected_row[0])  # Isi ID data
        nama_var.set(selected_row[1])  # Isi nama siswa
        biologi_var.set(selected_row[2])  # Isi nilai Biologi
        fisika_var.set(selected_row[3])  # Isi nilai Fisika
        inggris_var.set(selected_row[4])  # Isi nilai Inggris
    except IndexError:  # Tangani jika tidak ada data yang dipilih
        messagebox.showerror("Error", "Pilih data yang valid!")

# Inisialisasi database
create_database()

# Membuat GUI dengan tkinter
root = Tk()  # Inisialisasi tkinter
root.title("Prediksi Fakultas Siswa")  # Judul jendela GUI

# Variabel tkinter untuk input
nama_var = StringVar()  # Variabel untuk nama siswa
biologi_var = StringVar()  # Variabel untuk nilai Biologi
fisika_var = StringVar()  # Variabel untuk nilai Fisika
inggris_var = StringVar()  # Variabel untuk nilai Inggris
selected_record_id = StringVar()  # Variabel untuk menyimpan ID data yang dipilih

# Komponen input di GUI
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)  # Label untuk nama siswa
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)  # Input untuk nama siswa

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)  # Label untuk nilai Biologi
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)  # Input untuk nilai Biologi

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)  # Label untuk nilai Fisika
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)  # Input untuk nilai Fisika

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)  # Label untuk nilai Inggris
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)  # Input untuk nilai Inggris

# Tombol untuk aksi
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)  # Tombol untuk menambahkan data
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)  # Tombol untuk memperbarui data
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)  # Tombol untuk menghapus data

# Tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")  # Kolom tabel
tree = ttk.Treeview(root, columns=columns, show='headings')  # Membuat tabel

# Mengatur posisi isi tabel di tengah
for col in columns:
    tree.heading(col, text=col.capitalize())  # Atur header kolom
    tree.column(col, anchor='center')  # Atur teks berada di tengah

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)  # Tempatkan tabel di grid

# Event untuk mengisi form berdasarkan pilihan tabel
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)  # Tangkap event klik pada tabel

# Mengisi tabel saat pertama kali dijalankan
populate_table()

# Menjalankan GUI
root.mainloop()  # Loop utama untuk menjalankan aplikasi
