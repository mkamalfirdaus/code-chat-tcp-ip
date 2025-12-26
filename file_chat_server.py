import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import datetime

class ChatServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Server TCP/IP")
        self.root.geometry("600x400")

        self.text_area = scrolledtext.ScrolledText(root, height=20, width=70)
        self.text_area.pack(padx=10, pady=10)

        self.start_button = tk.Button(root, text="Start Server", command=self.start_server)
        self.start_button.pack(pady=5)

        self.server_socket = None
        self.clients = {}              # {client_id: socket}
        self.client_lock = threading.Lock()
        self.log_file = "server_log.txt"

    def log_message(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log = f"[{timestamp}] {message}"
        self.text_area.insert(tk.END, log + "\n")
        self.text_area.see(tk.END)
        with open(self.log_file, "a") as f:
            f.write(log + "\n")

    def handle_client(self, client_socket, client_address, client_id):
        self.log_message(f"Client terhubung: {client_id} dari {client_address}")

        with self.client_lock:
            self.clients[client_id] = client_socket

        try:
            while True:
                data = client_socket.recv(1024).decode("ascii")
                if not data or data.lower() == "exit":
                    break

                # PRIVATE MESSAGE
                if data.startswith("TO:"):
                    try:
                        _, target_id, message = data.split(":", 2)
                        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                        full_msg = f"[{timestamp}] {client_id} -> {target_id}: {message}"

                        with self.client_lock:
                            if target_id in self.clients:
                                self.clients[target_id].send(full_msg.encode("ascii"))
                                self.log_message(full_msg)
                            else:
                                client_socket.send(
                                    f"Error: Client {target_id} tidak ditemukan".encode("ascii")
                                )
                    except ValueError:
                        client_socket.send(
                            "Error format. Gunakan TO:<ClientID>:<Pesan>".encode("ascii")
                        )

                # BROADCAST MESSAGE
                elif data.startswith("ALL:"):
                    message = data[4:]
                    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                    broadcast_msg = f"[{timestamp}] [BROADCAST] {client_id}: {message}"

                    with self.client_lock:
                        for cid, sock in self.clients.items():
                            if cid != client_id:
                                sock.send(broadcast_msg.encode("ascii"))

                    self.log_message(broadcast_msg)

                else:
                    client_socket.send(
                        "Format salah. Gunakan TO:<ClientID>:<Pesan> atau ALL:<Pesan>".encode("ascii")
                    )

        except Exception as e:
            self.log_message(f"Error client {client_id}: {e}")

        finally:
            with self.client_lock:
                if client_id in self.clients:
                    del self.clients[client_id]
            client_socket.close()
            self.log_message(f"Client {client_id} terputus")

    def accept_connections(self):
        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                client_id = client_socket.recv(1024).decode("ascii")
                threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address, client_id),
                    daemon=True
                ).start()
            except:
                break

    def start_server(self, host="0.0.0.0", port=12345):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((host, port))
            self.server_socket.listen(5)
            self.log_message(f"Server berjalan di {host}:{port}")
            self.start_button.config(state="disabled")
            threading.Thread(target=self.accept_connections, daemon=True).start()
        except Exception as e:
            self.log_message(f"Gagal menjalankan server: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatServerGUI(root)
    root.mainloop()
