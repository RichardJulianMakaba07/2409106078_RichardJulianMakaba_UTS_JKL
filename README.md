# UTS Jaringan Komputer Lanjut - Integration Network with Python

**Nama** : Richard Julian Makaba
**NIM**  : 2409106078
**Kelas**: B 2024 - Program Studi Informatika

Satu project Python modular untuk otomatisasi kantor cabang virtual:
identitas, akses SSH, monitoring SNMP, pembuatan pesan NETCONF, dan analisis
data telemetry, ditutup dengan satu laporan gabungan.

## Struktur Project

```
.
├── main.py              # Titik masuk: menjalankan semua modul + laporan akhir
├── identitas.py         # Identitas cabang & buat_id_perangkat()
├── ssh_modul.py         # cek_ssh()            -> Paramiko
├── snmp_modul.py        # cek_snmp()           -> PySNMP (SNMPv2c, sysName)
├── netconf_modul.py     # buat_pesan_netconf() -> XML <rpc><edit-config>
├── telemetry_modul.py   # klasifikasi_telemetry() -> KRITIS/WASPADA/NORMAL
├── requirements.txt     # Dependensi (paramiko, pysnmp)
├── .gitignore
└── README.md
```

## Cara Menjalankan

```bash
# 1. Clone repository lalu masuk ke foldernya
# 2. Buat dan aktifkan virtual environment
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Pasang dependensi
pip install -r requirements.txt

# 4. Isi alamat target & password lewat variabel lingkungan (tidak disimpan di kode)
export SSH_HOST=<ip-vm>
export SNMP_HOST=<ip-vm>
export SSH_PASSWORD=<password>    

# 5. Jalankan
python3 main.py
```

Kegagalan koneksi SSH/SNMP ditangani dengan `try/except`, sehingga program
tetap berjalan sampai laporan akhir tercetak.

## Ringkasan Personalisasi

- Kode cabang diturunkan dari 3 digit terakhir NIM (`identitas.py`).
- Username SSH berpola `admin_<kode_cabang>`; community SNMP berpola `comm_<kode_cabang>`.
- VLAN ID pada pesan NETCONF = angka dari kode cabang.
- Sampel `cpuUsage` telemetry diturunkan dari potongan dua digit berurutan NIM.
- Ambang klasifikasi: di atas 80 = KRITIS, 50-80 = WASPADA, di bawah 50 = NORMAL.
- Kredensial tidak disimpan di repository.
