# code-chat-tcp-ip
# Aplikasi Chat TCP/IP menggunakan Python

Aplikasi ini merupakan program chat berbasis TCP/IP menggunakan bahasa pemrograman Python. 
Program terdiri dari satu server dan beberapa client yang dapat saling berkomunikasi melalui jaringan lokal.

Aplikasi ini mendukung:
- Pengiriman pesan privat (private messaging)
- Pengiriman pesan ke semua client (broadcast)
- Pengujian dilakukan menggunakan satu laptop dengan menjalankan beberapa client secara bersamaan.

## Teknologi yang Digunakan
- Python
- Socket Programming
- Threading
- Tkinter (GUI)

## Cara Menjalankan Program

1. Jalankan server terlebih dahulu
2. Jalankan client
3. Masukkan Client ID saat diminta (contoh: ClientA, ClientB, ClientC).
4. Format pengiriman pesan:
- Pesan privat:
  ```
  TO:ClientB:Halo
  ```
- Pesan broadcast:
  ```
  ALL:Halo semua
  ```
## Pengujian
Pengujian dilakukan secara lokal menggunakan satu laptop dengan menjalankan server dan beberapa client secara bersamaan untuk mensimulasikan komunikasi multi-client.

## Penulis
M. Kamal Firdaus

