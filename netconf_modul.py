"""
Nama   : Richard Julian Makaba (NIM 2409106078)
"""

import xml.etree.ElementTree as ET

from identitas import kode_cabang

NS_NETCONF = "urn:ietf:params:xml:ns:netconf:base:1.0"
NS_VLAN = "http://openconfig.net/yang/vlan"

# TRANSPORT layer: tidak ada di dalam string XML. Pesan ini nantinya dikirim
# melalui sesi SSH (subsystem "netconf", port 830) atau TLS.


def buat_pesan_netconf(message_id="101"):
    """Mengembalikan string XML <rpc><edit-config> untuk membuat VLAN."""
    vlan_id = str(int(kode_cabang))  # "078" -> "78" (VLAN ID berupa angka)

    # --- MESSAGES layer: pembungkus <rpc> beserta message-id ---
    rpc = ET.Element("rpc", {
        "message-id": message_id,
        "xmlns": NS_NETCONF,
        "xmlns:nc": NS_NETCONF,
    })

    # --- OPERATIONS layer: operasi <edit-config> pada datastore running ---
    edit = ET.SubElement(rpc, "edit-config")
    target = ET.SubElement(edit, "target")
    ET.SubElement(target, "running")
    ET.SubElement(edit, "default-operation").text = "merge"

    # --- CONTENT layer: data konfigurasi (model YANG VLAN) di dalam <config> ---
    config = ET.SubElement(edit, "config")
    vlans = ET.SubElement(config, "vlans", {"xmlns": NS_VLAN})
    vlan = ET.SubElement(vlans, "vlan", {"nc:operation": "create"})
    ET.SubElement(vlan, "vlan-id").text = vlan_id
    cfg = ET.SubElement(vlan, "config")
    ET.SubElement(cfg, "vlan-id").text = vlan_id
    ET.SubElement(cfg, "name").text = f"VLAN{vlan_id}"
    ET.SubElement(cfg, "status").text = "ACTIVE"

    ET.indent(rpc, space="  ")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(rpc, encoding="unicode")


if __name__ == "__main__":
    print(buat_pesan_netconf())
