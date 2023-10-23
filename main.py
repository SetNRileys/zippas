import zipfile
import rarfile
import tkinter as tk
from tkinter import filedialog, messagebox

def extract_zip(zip_path, password):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            zip_file.extractall(pwd=password.encode())
        return True
    except Exception as e:
        return False

def extract_rar(rar_path, password):
    try:
        with rarfile.RarFile(rar_path) as rar_file:
            rar_file.extractall(pwd=password.encode())
        return True
    except Exception as e:
        return False

def browse_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def browse_password_files(entry):
    file_paths = filedialog.askopenfilenames()
    entry.delete(0, tk.END)
    for file_path in file_paths:
        entry.insert(tk.END, file_path + '\n')

def start_bruteforce():
    zip_path = zip_path_entry.get()
    password_file_paths = password_file_paths_entry.get()

    if not zip_path or not password_file_paths:
        messagebox.showerror("Error", "Please provide both archive and password file paths.")
        return

    password_file_paths = password_file_paths.split('\n')
    password_file_paths = [path.strip() for path in password_file_paths if path.strip()]

    passwords = []
    for password_file_path in password_file_paths:
        try:
            with open(password_file_path, 'r') as password_file:
                passwords.extend(password_file.read().splitlines())
        except Exception as e:
            messagebox.showerror("Error", f"Error reading password file: {password_file_path}")
            return

    try:
        for password in passwords:
            if extract_zip(zip_path, password):
                messagebox.showinfo("Success", f"Password found: {password}")
                return

        messagebox.showinfo("Result", "Password not found in the provided list.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def clear_fields():
    zip_path_entry.delete(0, tk.END)
    password_file_paths_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Archive Password Bruteforce")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

zip_path_label = tk.Label(frame, text="Archive Path:")
zip_path_label.grid(row=0, column=0)
zip_path_entry = tk.Entry(frame)
zip_path_entry.grid(row=0, column=1)
zip_path_button = tk.Button(frame, text="Browse", command=lambda: browse_file(zip_path_entry))
zip_path_button.grid(row=0, column=2)

password_file_paths_label = tk.Label(frame, text="Password Files:")
password_file_paths_label.grid(row=1, column=0)
password_file_paths_entry = tk.Entry(frame)
password_file_paths_entry.grid(row=1, column=1)
password_file_paths_button = tk.Button(frame, text="Browse", command=lambda: browse_password_files(password_file_paths_entry))
password_file_paths_button.grid(row=1, column=2)

bruteforce_button = tk.Button(frame, text="Start Bruteforce", command=start_bruteforce)
bruteforce_button.grid(row=2, column=0, columnspan=3)

clear_button = tk.Button(frame, text="Clear Fields", command=clear_fields)
clear_button.grid(row=4, column=0, columnspan=3)

root.mainloop()
