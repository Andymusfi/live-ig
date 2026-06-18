import subprocess
import os
import time
import urllib.request
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# =======================================================
# 0. DUMMY WEB SERVER (AGAR RENDER.COM GRATIS)
# =======================================================
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bot IG Live Sedang Berjalan 24/7!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), DummyHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# =======================================================
# 1. KONFIGURASI
# =======================================================
link_latar = "https://i.ibb.co.com/3mDcmkfg/Proyek-Baru-32-F8-FB05-E.png"

# Daftar video YouTube (Bisa Anda ubah/tambah)
daftar_video = [
    "https://youtu.be/5zaOt7ErPzQ?si=jJXxDbXr_Z-8035i",
    "https://youtu.be/bEI0fqUhv9k?si=qJQikXv_VLVlX2_7I",
    "https://youtu.be/DcHwGEApnYI?si=XoenIKZ2tvUEAHhn"
]

# MASUKKAN STREAM KEY INSTAGRAM DI SINI (Ganti setiap mau Live)
stream_url = "rtmps://edgetee-upload-cgk2-1.xx.fbcdn.net:443/rtmp/"
stream_key = "18140325739558216?s_bl=1&s_fbp=sin2-2&s_ow=10&s_prp=cgk2-1&s_sw=0&s_tids=1&s_vt=ig&a=Ab4oSpqlRXszn72kX5r1rL0w"

gabungan = stream_url + stream_key if stream_url.endswith("/") else stream_url + "/" + stream_key

# =======================================================
# 2. PERSIAPAN ASET
# =======================================================
print("Mengunduh gambar latar...")
if os.path.exists("latar.png"): os.remove("latar.png")
urllib.request.urlretrieve(link_latar, "latar.png")
print("Gambar latar berhasil diunduh.")

# =======================================================
# 3. PROSES STREAMING LITE (OPTIMASI UNTUK SERVER GRATIS)
# =======================================================
print("STATUS: Memulai sistem. Pantau dari Instagram Live Producer...")

putaran = 1
while True:
    print(f"\n--- Memulai Putaran ke-{putaran} ---")
    for url_yt in daftar_video:
        print(f"Memproses video: {url_yt}")
        
        # Ekstrak link video 720p (Lebih ringan)
        ekstrak = subprocess.run(["yt-dlp", "-f", "best[height<=720]/best", "-g", url_yt], capture_output=True, text=True)
        jalur_live_yt = ekstrak.stdout.strip()
        
        if not jalur_live_yt:
            print("Gagal mengekstrak link video, melewati...")
            continue

        # SETTINGAN SUPER RINGAN UNTUK RENDER.COM
        # Resolusi diturunkan jadi 720p, preset ultrafast, bitrate 1500k
        perintah = (
            f'ffmpeg -loglevel warning -re -loop 1 -framerate 30 -i "latar.png" '
            f'-timeout 20000000 -i "{jalur_live_yt}" '
            f'-filter_complex "[0:v]scale=720:1280[bg];[1:v]scale=720:-2[vid];[bg][vid]overlay=(W-w)/2:(H-h)/2" '
            f'-c:v libx264 -preset ultrafast -profile:v main -crf 25 -b:v 1500k -maxrate 1500k -bufsize 3000k '
            f'-pix_fmt yuv420p -g 60 -c:a aac -b:a 128k -ar 44100 '
            f'-reconnect 1 -reconnect_at_eof 1 -reconnect_streamed 1 -reconnect_delay_max 5 '
            f'-f flv "{gabungan}"'
        )
        
        try:
            subprocess.run(perintah, shell=True, check=True)
        except subprocess.CalledProcessError:
            print("Koneksi terputus, mencoba memulihkan dalam 5 detik...")
            time.sleep(5)
            
    print(f"--- Putaran ke-{putaran} selesai, mengulang dari awal... ---")
    putaran += 1
