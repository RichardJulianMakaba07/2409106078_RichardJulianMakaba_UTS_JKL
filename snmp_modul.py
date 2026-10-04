#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nama File : snmp_modul.py
Tujuan    : Mengambil nilai sysName (OID 1.3.6.1.2.1.1.5.0) memakai SNMPv2c
            dengan community string comm_<kode_cabang> (PySNMP).
Pembuat   : Richard Julian Makaba (NIM 2409106078)
"""

import asyncio
import os

from pysnmp.hlapi.v3arch.asyncio import (
    CommunityData, ContextData, ObjectIdentity, ObjectType,
    SnmpEngine, UdpTransportTarget, get_cmd,
)

from identitas import kode_cabang

COMMUNITY = f"comm_{kode_cabang}"
OID_SYSNAME = "1.3.6.1.2.1.1.5.0"


async def _ambil_sysname(host, port):
    engine = SnmpEngine()
    try:
        target = await UdpTransportTarget.create((host, port), timeout=3, retries=1)
        return await get_cmd(
            engine,
            CommunityData(COMMUNITY, mpModel=1),  # mpModel=1 -> SNMPv2c
            target,
            ContextData(),
            ObjectType(ObjectIdentity(OID_SYSNAME)),
        )
    finally:
        engine.close_dispatcher()


def cek_snmp(host=None, port=1161):
    """Ambil sysName via SNMPv2c, cetak dan kembalikan hasilnya (dict)."""
    host = host or os.environ.get("SNMP_HOST", "127.0.0.1")
    hasil = {"status": "GAGAL", "host": host, "oid": OID_SYSNAME,
             "sysName": None, "error": None}

    print(f"[SNMP] GET {OID_SYSNAME} dari {host}:{port} (SNMPv2c) ...")
    try:
        err_indication, err_status, err_index, var_binds = asyncio.run(
            _ambil_sysname(host, port))

        if err_indication:
            hasil["error"] = str(err_indication)
        elif err_status:
            posisi = var_binds[int(err_index) - 1][0] if err_index else "?"
            hasil["error"] = f"{err_status.prettyPrint()} pada {posisi}"
        else:
            for oid, nilai in var_binds:
                hasil["sysName"] = nilai.prettyPrint()
            hasil["status"] = "BERHASIL"
    except Exception as e:
        hasil["error"] = f"Kesalahan tak terduga: {e}"

    if hasil["status"] == "BERHASIL":
        print(f"[SNMP] sysName = {hasil['sysName']}")
    else:
        print(f"[SNMP] GAGAL -> {hasil['error']}")
    return hasil


if __name__ == "__main__":
    cek_snmp()
