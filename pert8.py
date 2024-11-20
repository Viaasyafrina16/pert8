# Import Library:
import sqlite3  #Digunakan untuk berinteraksi dengan database SQLite.
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk #Digunakan untuk membuat antarmuka pengguna grafis (GUI).

# Fungsi untuk membuat database dan tabel
def create_database():
    conn = sqlite3.connect('nilai_siswa.db') #Membuat koneksi ke database nilai_siswa.db.
    cursor = conn.cursor() # Membuat objek untuk menjalankan perintah SQL.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        ) 
    ''')#Membuat tabel nilai_siswa jika belum ada, dengan kolom untuk ID, nama siswa, nilai biologi, fisika, inggris, dan prediksi fakultas.
    conn.commit()# Menyimpan perubahan.
    conn.close()# Menutup koneksi.

def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa")# Mengambil semua data dari tabel "nilai_siswa".
    rows = cursor.fetchall()
    conn.close()
    return rows #Mengambil semua data dari tabel nilai_siswa dan mengembalikannya sebagai daftar.

def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))# Menyimpan data baru ke tabel.
    conn.commit()
    conn.close()

def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))# Memperbarui data berdasarkan ID.
    conn.commit()
    conn.close()

def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,)) # Menghapus data berdasarkan ID.
    conn.commit()
    conn.close()

def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Diketahui"

def submit():
    try:
        nama = nama_var.get() # Mengambil nama siswa dari input.
        biologi = int(biologi_var.get()) # Mengambil dan mengonversi nilai Biologi ke integer.
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise Exception("Nama siswa tidak boleh kosong.")# Validasi nama.

        prediksi = calculate_prediction(biologi, fisika, inggris)#  Menghitung prediksi fakultas.
        save_to_database(nama, biologi, fisika, inggris, prediksi)  # Menyimpan data ke database.
        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        clear_inputs()# Mengosongkan form input.
        populate_table()# Memperbarui tabel.
    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")# Menangani error input.

def update():
    try:
        # Cek apakah ada data yang dipilih dari tabel
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk di-update!")
        
        # Ambil data ID record yang dipilih
        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())
         
        # Validasi input nama siswa
        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")# Jika nama kosong, tampilkan pesan error.

        # Hitung prediksi fakultas berdasarkan nilai
        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi) # Update data ke database

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!") # Tampilkan pesan sukses
        clear_inputs()   # Bersihkan form input
        populate_table() # Perbarui tabel dengan data terbaru
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")# Tampilkan pesan error jika ada masalah dengan input

def delete():
    try:
         # Cek apakah ada data yang dipilih dari tabel
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk dihapus!")
         # Ambil ID record yang dipilih dari tabel
        record_id = int(selected_record_id.get())
        delete_database(record_id)# Hapus data dari database berdasarkan ID
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")# Tampilkan pesan sukses jika penghapusan berhasil
        clear_inputs()# Bersihkan form input setelah penghapusan
        populate_table() # Perbarui tabel dengan data terbaru
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")# Jika terjadi error, tampilkan pesan kesalahan

def clear_inputs():
    # Menghapus semua input di form dengan mengatur nilai variabel ke string kosong
    nama_var.set("") # Menghapus input nama siswa
    biologi_var.set("") # Menghapus input nilai biologi
    fisika_var.set("") # Menghapus input nilai fisika
    inggris_var.set("") # Menghapus input nilai inggris
    selected_record_id.set("")# Menghapus ID record yang dipilih dari tabel

def populate_table():
     # Membersihkan semua data yang ada di tabel terlebih dahulu
    for row in tree.get_children():
        tree.delete(row)# Menghapus setiap baris di tabel Treeview
    for row in fetch_data():  # Mengambil data terbaru dari database dan menambahkan ke tabel
        tree.insert('', 'end', values=row)# Menambahkan setiap baris data ke tabel

def fill_inputs_from_table(event):
    try:
         # Mengambil item yang dipilih dari tabel
        selected_item = tree.selection()[0] # Mengambil ID item yang dipilih
        selected_row = tree.item(selected_item)['values'] # Mendapatkan nilai dari baris yang dipilih
        # Mengisi form input dengan data yang dipilih dari tabel
        selected_record_id.set(selected_row[0])# Mengatur ID record yang dipilih
        nama_var.set(selected_row[1])# Mengisi input nama siswa
        biologi_var.set(selected_row[2])# Mengisi input nilai biologi
        fisika_var.set(selected_row[3])# Mengisi input nilai fisika
        inggris_var.set(selected_row[4])# Mengisi input nilai inggris
    except IndexError:
        # Jika tidak ada item yang dipilih, tampilkan pesan error
        messagebox.showerror("Error", "Pilih data yang valid!")

# Inisialisasi database
create_database()

# Membuat GUI dengan tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")

# Variabel tkinter
nama_var = StringVar() # Menyimpan nama siswa
biologi_var = StringVar() # Menyimpan nilai biologi
fisika_var = StringVar() # Menyimpan nilai fisika
inggris_var = StringVar() # Menyimpan nilai inggris
selected_record_id = StringVar()  # Untuk menyimpan ID record yang dipilih

# Membuat label dan input untuk nama siswa.
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

# Membuat label dan input untuk nilai biologi.
Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

# Membuat label dan input untuk nilai fisika.
Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

# Membuat label dan input untuk nilai inggris.
Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)# Tombol untuk menambahkan data ke database.
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)# Tombol untuk memperbarui data yang dipilih dari tabel.
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)# Tombol untuk menghapus data yang dipilih dari tabel.

# Tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')





# Mengatur posisi isi tabel di tengah
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center') # Mengatur posisi isi kolom berada di tengah.

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)# Menempatkan tabel di jendela utama pada baris ke-5 dengan padding.

tree.bind('<ButtonRelease-1>', fill_inputs_from_table)# Menghubungkan tabel dengan fungsi fill_inputs_from_table
                                                    # Ketika baris di tabel dipilih, data tersebut akan otomatis terisi di form input.

populate_table()# Memanggil fungsi untuk mengambil data dari database dan menampilkannya di tabel saat aplikasi pertama kali berjalan.

root.mainloop()# Memulai loop utama aplikasi untuk menjalankan GUI.