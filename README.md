# Aplikasi Manajemen Barang — Docker Compose

**Praktikum Cloud Computing**
Thomas Damianus — 23083000045
Universitas Merdeka Malang 2026

## Deskripsi
Aplikasi manajemen barang berbasis multi-container menggunakan Docker Compose.
Terdiri dari 3 service: PostgreSQL (db), Flask API (api), dan Flask Web (web).

## Arsitektur
```
Browser → Web (port 8000) → API (port 8080) → PostgreSQL → Volume db-data
```

## Cara Menjalankan
```bash
docker compose up -d --build
```
Akses di: http://localhost:8000

## Data Barang Awal
- Tas — Rp150.000
- Sepatu — Rp250.000
- Topi — Rp85.000

## Perintah Berguna
```bash
docker compose ps          # cek status
docker compose logs -f     # lihat log
docker compose down        # hentikan (data tetap)
docker compose down -v     # hentikan + hapus volume
```
