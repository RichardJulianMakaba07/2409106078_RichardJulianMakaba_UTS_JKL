#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nama File : ssh_modul.py
Tujuan    : Login ke VM/laptop via SSH (Paramiko) memakai username
            admin_<kode_cabang>, lalu menjalankan perintah diagnostik.
Pembuat   : Richard Julian Makaba (NIM 2409106078)
"""

import getpass
import os

import paramiko

from identitas import kode_cabang

SSH_USERNAME = f"admin_{kode_cabang}"
PERINTAH_DIAGNOSTIK = ["hostname", "uname -a", "uptime"]


def cek_ssh(host=None, port=2222):
    """Login SSH, jalankan perintah diagnostik, cetak dan kembalikan hasilnya (dict).

    Host dibaca dari variabel lingkungan SSH_HOST dan password dari SSH_PASSWORD
    (atau diminta lewat prompt) supaya kredensial TIDAK tersimpan di repository.
    """
    host = host or os.environ.get("SSH_HOST", "127.0.0.1")
    hasil = {"status": "GAGAL", "host": host, "username": SSH_USERNAME,
             "perintah": {}, "error": None}

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print(f"[SSH] Menghubungi {SSH_USERNAME}@{host}:{port} ...")
    try:
        password = os.environ.get("SSH_PASSWORD") or getpass.getpass(
            f"Password SSH untuk {SSH_USERNAME}: ")
        client.connect(host, port=port, username=SSH_USERNAME,
                       password=password, timeout=10,
                       look_for_keys=False, allow_agent=False)

        for perintah in PERINTAH_DIAGNOSTIK:
            _, stdout, stderr = client.exec_command(perintah, timeout=10)
            keluaran = stdout.read().decode().strip()
            galat = stderr.read().decode().strip()
            hasil["perintah"][perintah] = keluaran or galat
            print(f"[SSH] $ {perintah}\n      {hasil['perintah'][perintah]}")

        hasil["status"] = "BERHASIL"
    except paramiko.AuthenticationException:
        hasil["error"] = "Autentikasi gagal (username/password salah)"
    except (paramiko.SSHException, OSError, EOFError) as e:
        hasil["error"] = f"Koneksi gagal: {e}"
    except Exception as e:  # supaya program utama tidak pernah berhenti
        hasil["error"] = f"Kesalahan tak terduga: {e}"
    finally:
        client.close()

    if hasil["error"]:
        print(f"[SSH] GAGAL -> {hasil['error']}")
    return hasil


if __name__ == "__main__":
    cek_ssh()
