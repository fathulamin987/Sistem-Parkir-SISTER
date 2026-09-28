from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
from datetime import datetime
import threading
import uuid


# ==============================
# DATA AWAL
# ==============================

slot_parkir = {
    "A01": None,
    "A02": None,
    "A03": None,
    "A04": None,
    "A05": None,
    "A06": None,
    "A07": None,
    "A08": None,
    "A09": None,
    "A10": None
}

kendaraan = {}
riwayat = []

lock = threading.Lock()


# ==============================
# FUNGSI KENDARAAN MASUK
# ==============================

def kendaraan_masuk(nomor_plat, jenis):
    with lock:

        # Cek apakah kendaraan sudah parkir
        if nomor_plat in kendaraan:
            return {
                "status": False,
                "pesan": "Kendaraan tersebut masih berada di area parkir."
            }

        # Cari slot kosong
        slot = None

        for nomor_slot in slot_parkir:
            if slot_parkir[nomor_slot] is None:
                slot = nomor_slot
                break

        if slot is None:
            return {
                "status": False,
                "pesan": "Parkiran penuh."
            }

        # Buat ID tiket
        id_tiket = str(uuid.uuid4())[:8]

        waktu_masuk = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data = {
            "id_tiket": id_tiket,
            "nomor_plat": nomor_plat,
            "jenis": jenis,
            "slot": slot,
            "waktu_masuk": waktu_masuk
        }

        kendaraan[nomor_plat] = data
        slot_parkir[slot] = nomor_plat

        return {
            "status": True,
            "pesan": "Kendaraan berhasil masuk.",
            "data": data
        }


# ==============================
# FUNGSI KENDARAAN KELUAR
# ==============================

def kendaraan_keluar(nomor_plat):

    with lock:

        if nomor_plat not in kendaraan:
            return {
                "status": False,
                "pesan": "Kendaraan tidak ditemukan."
            }

        data = kendaraan[nomor_plat]

        # Hitung durasi parkir
        waktu_masuk = datetime.strptime(
            data["waktu_masuk"],
            "%Y-%m-%d %H:%M:%S"
        )

        waktu_keluar = datetime.now()

        durasi = waktu_keluar - waktu_masuk
        total_detik = durasi.total_seconds()

        # Minimal dihitung 1 jam
        jam = max(1, int(total_detik / 3600))

        # Tarif
        if data["jenis"].lower() == "motor":
            tarif = 2000
        else:
            tarif = 5000

        total_bayar = jam * tarif

        # Kosongkan slot
        slot = data["slot"]
        slot_parkir[slot] = None

        # Simpan transaksi
        transaksi = {
            "id_tiket": data["id_tiket"],
            "nomor_plat": nomor_plat,
            "jenis": data["jenis"],
            "slot": slot,
            "waktu_masuk": data["waktu_masuk"],
            "waktu_keluar": waktu_keluar.strftime("%Y-%m-%d %H:%M:%S"),
            "durasi_jam": jam,
            "total_bayar": total_bayar
        }

        riwayat.append(transaksi)

        # Hapus kendaraan yang sedang parkir
        del kendaraan[nomor_plat]

        return {
            "status": True,
            "pesan": "Kendaraan berhasil keluar.",
            "data": transaksi
        }


# ==============================
# MELIHAT KONDISI PARKIR
# ==============================

def lihat_slot():

    with lock:

        hasil = {}

        for slot, plat in slot_parkir.items():

            if plat is None:
                hasil[slot] = "KOSONG"
            else:
                hasil[slot] = plat

        return hasil


# ==============================
# MENCARI KENDARAAN
# ==============================

def cari_kendaraan(nomor_plat):

    with lock:

        if nomor_plat not in kendaraan:
            return {
                "status": False,
                "pesan": "Kendaraan tidak sedang parkir."
            }

        return {
            "status": True,
            "data": kendaraan[nomor_plat]
        }


# ==============================
# LAPORAN MANAJEMEN
# ==============================

def laporan():

    with lock:

        total_pendapatan = 0

        for transaksi in riwayat:
            total_pendapatan += transaksi["total_bayar"]

        total_kendaraan_sedang_parkir = len(kendaraan)

        total_slot = len(slot_parkir)

        slot_terisi = total_kendaraan_sedang_parkir

        slot_kosong = total_slot - slot_terisi

        return {
            "total_transaksi": len(riwayat),
            "total_pendapatan": total_pendapatan,
            "kendaraan_sedang_parkir": total_kendaraan_sedang_parkir,
            "slot_terisi": slot_terisi,
            "slot_kosong": slot_kosong
        }


# ==============================
# RIWAYAT TRANSAKSI
# ==============================

def riwayat_transaksi():

    with lock:

        return riwayat[-5:]


# ==============================
# SERVER RPC
# ==============================

class ThreadedXMLRPCServer(
    ThreadingMixIn,
    SimpleXMLRPCServer
):
    pass


server = ThreadedXMLRPCServer(
    ("0.0.0.0", 8000),
    allow_none=True
)

server.register_function(kendaraan_masuk, "kendaraan_masuk")
server.register_function(kendaraan_keluar, "kendaraan_keluar")
server.register_function(lihat_slot, "lihat_slot")
server.register_function(cari_kendaraan, "cari_kendaraan")
server.register_function(laporan, "laporan")
server.register_function(riwayat_transaksi, "riwayat_transaksi")

print("====================================")
print("      SERVER PARKIR KAMPUS")
print("====================================")
print("Server berjalan pada port 8000")
print("Menunggu koneksi dari client...")
print("====================================")

server.serve_forever()