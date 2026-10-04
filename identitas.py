#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nama File : identitas.py
Tujuan    : Menyimpan identitas cabang (NIM, nama, kode cabang) dan
            function pembuat ID perangkat untuk dipakai modul lain.
Pembuat   : Richard Julian Makaba (NIM 2409106078)
"""

nim = "2409106078"
nama = "Richard Julian Makaba"
kode_cabang = nim[-3:]  # 3 digit terakhir NIM 


def buat_id_perangkat(jenis, nomor):
    """Membuat ID perangkat, contoh: buat_id_perangkat("sw", 1) -> "SW-<kode_cabang>-01"."""
    return f"{jenis.upper()}-{kode_cabang}-{int(nomor):02d}"


if __name__ == "__main__":
    print(f"NIM         : {nim}")
    print(f"Nama        : {nama}")
    print(f"Kode cabang : {kode_cabang}")
    print(f"ID Router   : {buat_id_perangkat('rtr', 1)}")
    print(f"ID Switch   : {buat_id_perangkat('sw', 2)}")
