import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

class ChatClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client TCP/IP")
        self.root.geometry("500x400")

        self.text_area = scrolledtext.ScrolledText(root, height=18, width=60)
        self.text_area.pack(padx=10, pady=10)

        self.entry = tk.Entry(root, width=50)
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_host = "127.0.0.1"
        self.server_port = 12345
        self.client_id = None

    def connect_to_server(self):
        self.client_id = simpledialog.askstring(
            "Client ID",
            "Masukkan Client ID (contoh: ClientA):"
        )

        if not self.client_id:
            self.root.destroy()
            return

        try:
            self.client_socket.connect((self.server_host, self.server_port))
            self.client_socket.send(self.client_id.encode("ascii"))
            self.text_area.insert(tk.END, f"Terhubung sebagai {self.client_id}\n")
            threading.Thread(target=self.receive_message, daemon=True).start()
        except Exception as e:
            self.text_area.insert(tk.END, f"Gagal terhubung: {e}\n")

    def receive_message(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode("ascii")
                self.text_area.insert(tk.END, message + "\n")
                self.text_area.see(tk.END)
            except:
                break

    def send_message(self, event=None):
        message = self.entry.get()
        if message:
            self.client_socket.send(message.encode("ascii"))
            self.entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClientGUI(root)
    app.connect_to_server()
    root.mainloop()
