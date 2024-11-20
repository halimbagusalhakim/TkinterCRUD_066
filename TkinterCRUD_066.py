import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

# Fungsi untuk membuat database dan tabel
def create_database():
    # Membuat atau membuka file database SQLite
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
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
    ''')
    conn.commit()
    conn.close()

# Mengambil data dari database
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa") # Ambil semua data
    rows = cursor.fetchall()
    conn.close()
    return rows

# Menyimpan data ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi)) # Parameterized query untuk keamanan
    conn.commit()
    conn.close()

# Memperbarui data dalam database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id)) # Update data berdasarkan ID
    conn.commit()
    conn.close()

# Menghapus data dari database
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,)) # Hapus data berdasarkan ID
    conn.commit()
    conn.close()

# Logika prediksi berdasarkan nilai
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran" # Prediksi berdasarkan nilai Biologi
    elif fisika > biologi and fisika > inggris:
        return "Teknik" # Prediksi berdasarkan nilai Fisika
    elif inggris > biologi and inggris > fisika:
        return "Bahasa" # Prediksi berdasarkan nilai Inggris
    else:
        return "Tidak Diketahui" # Jika nilai seimbang atau tidak memenuhi kriteria

# Menangani input data baru
def submit():
    try:
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama: # Validasi input nama
            raise Exception("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)
        save_to_database(nama, biologi, fisika, inggris, prediksi)

        # Memberikan notifikasi berhasil
        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        clear_inputs()
        populate_table() # Perbarui tabel di GUI
    except ValueError as e: # Tangani error input
        messagebox.showerror("Error", f"Input tidak valid: {e}")

# Mengupdate data yang dipilih
def update():
    try:
        if not selected_record_id.get(): # Validasi jika belum ada data yang dipilih
            raise Exception("Pilih data dari tabel untuk di-update!")

        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama: # Validasi input nama
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        clear_inputs()
        populate_table() # Perbarui tabel di GUI
    except ValueError as e: # Tangani error input
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Menghapus data yang dipilih
def delete():
    try:
        if not selected_record_id.get(): # Validasi jika belum ada data yang dipilih
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())
        delete_database(record_id) # Hapus data berdasarkan ID
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        clear_inputs()
        populate_table() # Perbarui tabel di GUI
    except ValueError as e: # Tangani error
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Membersihkan input di form
def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")

# Mengisi tabel di GUI dengan data dari database
def populate_table():
    for row in tree.get_children(): # Bersihkan data lama di tabel
        tree.delete(row)
    for row in fetch_data(): # Tambahkan data dari database
        tree.insert('', 'end', values=row)

# Mengisi form berdasarkan data yang dipilih di tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]
        selected_row = tree.item(selected_item)['values']

        selected_record_id.set(selected_row[0]) # ID record
        nama_var.set(selected_row[1]) # Nama siswa
        biologi_var.set(selected_row[2]) # Nilai Biologi
        fisika_var.set(selected_row[3]) # Nilai Fisika
        inggris_var.set(selected_row[4]) # Nilai Inggris
    except IndexError: # Tangani jika tidak ada data yang dipilih
        messagebox.showerror("Error", "Pilih data yang valid!")

# Inisialisasi database
create_database()

# Membuat GUI dengan tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")

# Variabel tkinter untuk input
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()  # Untuk menyimpan ID record yang dipilih

# Komponen input di GUI
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

# Tombol untuk aksi
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

# Tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')

# Mengatur posisi isi tabel di tengah
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center') 

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Event untuk mengisi form berdasarkan pilihan tabel
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

# Mengisi tabel saat pertama kali dijalankan
populate_table()

# Menjalankan GUI
root.mainloop()
