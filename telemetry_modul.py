"""
Nama   : Richard Julian Makaba (NIM 2409106078)
"""

from identitas import buat_id_perangkat, nim

# Nilai cpuUsage diturunkan dari potongan dua digit berurutan pada NIM:
#   nim[0:2] = "24" -> 24 | nim[3:5] = "91" -> 91
#   nim[6:8] = "60" -> 60 | nim[8:10] = "78" -> 78
data_telemetry = {
    "sampel_1": {"waktu": "2026-10-04T08:00:00", "perangkat": buat_id_perangkat("rtr", 1),
                 "cpuUsage": int(nim[0:2])},
    "sampel_2": {"waktu": "2026-10-04T08:00:10", "perangkat": buat_id_perangkat("rtr", 1),
                 "cpuUsage": int(nim[3:5])},
    "sampel_3": {"waktu": "2026-10-04T08:00:20", "perangkat": buat_id_perangkat("rtr", 1),
                 "cpuUsage": int(nim[6:8])},
    "sampel_4": {"waktu": "2026-10-04T08:00:30", "perangkat": buat_id_perangkat("rtr", 1),
                 "cpuUsage": int(nim[8:10])},
}


def _tentukan_status(nilai):
    if nilai > 80:
        return "KRITIS"
    elif nilai >= 50:
        return "WASPADA"
    return "NORMAL"


def klasifikasi_telemetry():
    """Iterasi seluruh sampel, klasifikasikan, cetak, dan kembalikan daftar hasilnya."""
    hasil = []
    print("[TELEMETRY] Klasifikasi cpuUsage:")
    for nama_sampel, isi in data_telemetry.items():
        status = _tentukan_status(isi["cpuUsage"])
        hasil.append({"sampel": nama_sampel, "waktu": isi["waktu"],
                      "cpuUsage": isi["cpuUsage"], "status": status})
        print(f"  {nama_sampel} | {isi['waktu']} | cpuUsage = {isi['cpuUsage']:>3}% -> {status}")
    return hasil


if __name__ == "__main__":
    klasifikasi_telemetry()
