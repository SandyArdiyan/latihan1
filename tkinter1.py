import sqlite3
from tkinter import Tk, Label, Entry, Button, messagebox, ttk, StringVar

# Fungsi untuk membuat tabel di database SQLite
def setup_database():
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nilai_siswa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_siswa TEXT,
        biologi INTEGER,
        fisika INTEGER,
        inggris INTEGER,
        prediksi_fakultas TEXT
    )
    """)
    conn.commit()
    conn.close()

# Fungsi untuk mengambil data dari database
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Fungsi untuk menyimpan data ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
    VALUES (?, ?, ?, ?, ?)
    """, (nama, biologi, fisika, inggris, prediksi))
    conn.commit()
    conn.close()

# Fungsi untuk memprediksi fakultas
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    """, (nama, biologi, fisika, inggris, prediksi, record_id))
    conn.commit()
    conn.close()

# Fungsi untuk menangani tombol submit
def delete_record(record_id):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()

# Fungsi untuk menghitung prediksi fakultas
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
        nama = entry_nama.get()
        biologi = int(entry_biologi.get())
        fisika = int(entry_fisika.get())
        inggris = int(entry_inggris.get())

        if not nama:
           raise Exception("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)
        save_to_database(nama, biologi, fisika, inggris, prediksi)

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        clear_inputs()
        populate_table()
    except ValueError:
        messagebox.showerror("Error", "Masukkan nilai yang valid untuk Biologi, Fisika, dan Inggris.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk diupdate!")

        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        populate_table()
        clear_inputs()
    except ValueError:
        messagebox.showerror("Error", "Masukkan nilai yang valid untuk Biologi, Fisika, dan Inggris.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())
        delete_record(record_id)

        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        populate_table()
        clear_inputs()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def clear_inputs():
    entry_nama.delete(0, 'end')
    entry_biologi.delete(0, 'end')
    entry_fisika.delete(0, 'end')
    entry_inggris.delete(0, 'end')

def populate_table():
    for row in treeview.get_children():
        treeview.delete(row)

    data = fetch_data()
    for record in data:
        treeview.insert('', 'end', values=record)

def fill_inputs_from_table(event):
    try:
        selected_item = treeview.selection()[0]
        selected_row = treeview.item(selected_item)['values']

        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid")

# Inisialisasi database dan GUI
setup_database()

root = Tk()
root.title("Prediksi Fakultas Siswa")

# Variabel tkinter
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()

# Elemen GUI
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
entry_nama = Entry(root, textvariable=nama_var)
entry_nama.grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
entry_biologi = Entry(root, textvariable=biologi_var)
entry_biologi.grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
entry_fisika = Entry(root, textvariable=fisika_var)
entry_fisika.grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
entry_inggris = Entry(root, textvariable=inggris_var)
entry_inggris.grid(row=3, column=1, padx=10, pady=5)

Button(root, text="Simpan", command=submit).grid(row=4, column=0, pady=5)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=5)
Button(root, text="Hapus", command=delete).grid(row=4, column=2, pady=5)

# Total untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
treeview = ttk.Treeview(root, columns=columns, show='headings')

# Mengatur posisi isi tabel di tengah
for col in columns:
    treeview.column(col, anchor='center')

treeview.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Event untuk memilih data dari tabel
treeview.bind('<ButtonRelease-1>', fill_inputs_from_table)

# Mengisi tabel dengan data
populate_table()

# Menjalankan Aplikasi
root.mainloop()
