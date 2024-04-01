import tkinter as tk
from tkinter import messagebox, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD

def encrypt(text, keyword):
    encrypted_text = ""
    keyword_index = 0
    for char in text:
        if char.isalpha():
            offset = ord('A') if char.isupper() else ord('a')
            shift = ord(keyword[keyword_index % len(keyword)]) - ord('A')
            encrypted_char = chr((ord(char) - offset + shift) % 26 + offset)
            encrypted_text += encrypted_char
            keyword_index += 1
        else:
            encrypted_text += char
    return encrypted_text

def decrypt(text, keyword):
    decrypted_text = ""
    keyword_index = 0
    for char in text:
        if char.isalpha():
            offset = ord('A') if char.isupper() else ord('a')
            shift = ord(keyword[keyword_index % len(keyword)]) - ord('A')
            decrypted_char = chr((ord(char) - offset - shift + 26) % 26 + offset)
            decrypted_text += decrypted_char
            keyword_index += 1
        else:
            decrypted_text += char
    return decrypted_text

def encrypt_file(input_file, output_file, keyword):
    with open(input_file, 'r') as f:
        text = f.read()
    encrypted_text = encrypt(text, keyword)
    with open(output_file, 'w') as f:
        f.write(encrypted_text)

def decrypt_file(input_file, output_file, keyword):
    with open(input_file, 'r') as f:
        text = f.read()
    decrypted_text = decrypt(text, keyword)
    with open(output_file, 'w') as f:
        f.write(decrypted_text)

def on_encrypt():
    global mode
    mode = "encrypt"
    keyword = keyword_entry.get()
    if keyword:
        global selected_keyword
        selected_keyword = keyword
        status_label.config(text="Ready to encrypt. Drag and drop a text file here.")
    else:
        messagebox.showerror("Error", "Please enter a keyword.")

def on_decrypt():
    global mode
    mode = "decrypt"
    keyword = keyword_entry.get()
    if keyword:
        global selected_keyword
        selected_keyword = keyword
        status_label.config(text="Ready to decrypt. Drag and drop an encrypted file here.")
    else:
        messagebox.showerror("Error", "Please enter a keyword.")

def on_drop(event):
    global mode
    if mode == "encrypt":
        file_path = event.data
        if isinstance(file_path, list):
            file_path = file_path[0]
        file_path = file_path.strip('{}')
        destination_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if destination_path:
            encrypt_file(file_path, destination_path, selected_keyword)
            status_label.config(text="File encrypted successfully.")
    elif mode == "decrypt":
        file_path = event.data
        if isinstance(file_path, list):
            file_path = file_path[0]
        file_path = file_path.strip('{}')
        destination_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if destination_path:
            decrypt_file(file_path, destination_path, selected_keyword)
            status_label.config(text="File decrypted successfully.")

root = TkinterDnD.Tk()
root.title("File Encryption/Decryption")

frame = tk.Frame(root)
frame.pack(pady=10)

encrypt_button = tk.Button(frame, text="Encrypt", command=on_encrypt)
encrypt_button.pack(side=tk.LEFT, padx=10)

decrypt_button = tk.Button(frame, text="Decrypt", command=on_decrypt)
decrypt_button.pack(side=tk.LEFT, padx=10)

keyword_entry = tk.Entry(root)
keyword_entry.pack()

global status_label
status_label = tk.Label(root, text="Enter a keyword, choose encrypt/decrypt and drag and drop a file here.", pady=10)
status_label.pack()

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

root.mainloop()
