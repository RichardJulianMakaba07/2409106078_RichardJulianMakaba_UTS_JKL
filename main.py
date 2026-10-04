"""
Nama   : Richard Julian Makaba (NIM 2409106078)
"""

import identitas
import netconf_modul
import snmp_modul
import ssh_modul
import telemetry_modul


class LaporanCabang:
    """Merangkum seluruh hasil otomatisasi satu cabang menjadi satu laporan."""

    def __init__(self, nim, nama, kode_cabang):
        self.nim = nim
        self.nama = nama
        self.kode_cabang = kode_cabang

    def tampilkan_laporan(self, hasil_ssh, hasil_snmp, pesan_netconf, hasil_telemetry):
        garis = "=" * 64
        print(f"\n{garis}\n LAPORAN AKHIR CABANG VIRTUAL\n{garis}")
        print(f" Nama / NIM    : {self.nama} / {self.nim}")
        print(f" Kode cabang   : {self.kode_cabang}")
        print(f" ID perangkat  : {identitas.buat_id_perangkat('rtr', 1)}")

        print(f"\n[1] SSH  ({hasil_ssh['username']}@{hasil_ssh['host']})")
        print(f"    Status : {hasil_ssh['status']}")
        if hasil_ssh["error"]:
            print(f"    Error  : {hasil_ssh['error']}")
        for perintah, keluaran in hasil_ssh["perintah"].items():
            print(f"    $ {perintah} -> {keluaran}")

        print(f"\n[2] SNMP (OID {hasil_snmp['oid']}, host {hasil_snmp['host']})")
        print(f"    Status : {hasil_snmp['status']}")
        if hasil_snmp["error"]:
            print(f"    Error  : {hasil_snmp['error']}")
        else:
            print(f"    sysName: {hasil_snmp['sysName']}")

        print("\n[3] NETCONF - pesan <rpc><edit-config> yang dibangun:")
        for baris in pesan_netconf.splitlines():
            print(f"    {baris}")

        print("\n[4] TELEMETRY - klasifikasi cpuUsage:")
        for h in hasil_telemetry:
            print(f"    {h['sampel']}: {h['cpuUsage']:>3}% -> {h['status']}")
        print(garis)


def main():
    hasil_ssh = ssh_modul.cek_ssh()
    hasil_snmp = snmp_modul.cek_snmp()
    pesan_netconf = netconf_modul.buat_pesan_netconf()
    hasil_telemetry = telemetry_modul.klasifikasi_telemetry()

    laporan = LaporanCabang(identitas.nim, identitas.nama, identitas.kode_cabang)
    laporan.tampilkan_laporan(hasil_ssh, hasil_snmp, pesan_netconf, hasil_telemetry)


if __name__ == "__main__":
    main()
