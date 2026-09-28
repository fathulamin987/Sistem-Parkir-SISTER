from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
from datetime import datetime
import uuid
import threading


# Server dapat melayani beberapa client secara bersamaan
class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


# Data slot parkir
slots = {
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

# Data kendaraan yang sedang parkir
kendaraan = {}

# Riwayat transaksi
transaksi = []

# Pengaman data ketika banyak client mengakses server
lock = threading.Lock()


def kendaraan_masuk(no_plat, jenis):
    with lock:

        # Cek apakah kendaraan sudah ada
        if no_plat in kendaraan:
            return {
                "status": False,
                "pesan": "Kendaraan tersebut masih berada di area parkir."
            }

        # Cari slot kosong
        slot_ditemukan = None

        for nomor_slot, data in slots.items():
            if data is None:
                slot_ditemukan = nomor_slot
                break

        if slot_ditemukan is None:
            return {
                "status": False,
                "pesan": "Parkiran penuh."
            }

        # Buat ID tiket
        id_tiket = str(uuid.uuid4())[:8]

        waktu_masuk = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data_kendaraan = {
            "id_tiket": id_tiket,
            "no_plat": no_plat,
            "jenis": jenis,
            "slot": slot_ditemukan,
            "waktu_masuk": waktu_masuk
        }

        kendaraan[no_plat] = data_kendaraan
        slots[slot_ditemukan] = data_kendaraan

        return {
            "status": True,
            "pesan": "Kendaraan berhasil masuk.",
            "data": data_kendaraan
        }


def kendaraan_keluar(no_plat):
    with lock:

        if no_plat not in kendaraan:
            return {
                "status": False,
                "pesan": "Kendaraan tidak ditemukan."
            }

        data = kendaraan[no_plat]

        waktu_masuk = datetime.strptime(
            data["waktu_masuk"],
            "%Y-%m-%d %H:%M:%S"
        )

        waktu_keluar = datetime.now()

        durasi_detik = (waktu_keluar - waktu_masuk).total_seconds()

        # Minimal dihitung 1 jam
        durasi_jam = max(1, int((durasi_detik + 3599) // 3600))

        if data["jenis"].lower() == "motor":
            tarif = 2000
        else:
            tarif = 5000

        total_bayar = durasi_jam * tarif

        waktu_keluar_text = waktu_keluar.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        data_transaksi = {
            "id_transaksi": str(uuid.uuid4())[:8],
            "id_tiket": data["id_tiket"],
            "no_plat": data["no_plat"],
            "jenis": data["jenis"],
            "slot": data["slot"],
            "waktu_masuk": data["waktu_masuk"],
            "waktu_keluar": waktu_keluar_text,
            "durasi": durasi_jam,
            "total_bayar": total_bayar
        }

        # Kosongkan slot
        slots[data["slot"]] = None

        # Hapus kendaraan dari daftar parkir
        del kendaraan[no_plat]

        # Simpan transaksi
        transaksi.append(data_transaksi)

        return {
            "status": True,
            "pesan": "Kendaraan berhasil keluar.",
            "data": data_transaksi
        }


def get_status_parkir():
    with lock:

        hasil = []

        for nomor_slot, data in slots.items():

            if data is None:
                hasil.append({
                    "slot": nomor_slot,
                    "status": "KOSONG",
                    "no_plat": "-"
                })
            else:
                hasil.append({
                    "slot": nomor_slot,
                    "status": "TERISI",
                    "no_plat": data["no_plat"]
                })

        return hasil


def get_laporan():
    with lock:

        total_transaksi = len(transaksi)

        total_pendapatan = sum(
            item["total_bayar"]
            for item in transaksi
        )

        kendaraan_parkir = len(kendaraan)

        slot_terisi = sum(
            1 for data in slots.values()
            if data is not None
        )

        slot_kosong = len(slots) - slot_terisi

        transaksi_terakhir = transaksi[-5:]

        return {
            "total_transaksi": total_transaksi,
            "total_pendapatan": total_pendapatan,
            "kendaraan_parkir": kendaraan_parkir,
            "slot_terisi": slot_terisi,
            "slot_kosong": slot_kosong,
            "transaksi_terakhir": transaksi_terakhir
        }


# Membuat server
server = ThreadedXMLRPCServer(
    ("0.0.0.0", 8000),
    allow_none=True
)

server.register_function(kendaraan_masuk, "kendaraan_masuk")
server.register_function(kendaraan_keluar, "kendaraan_keluar")
server.register_function(get_status_parkir, "get_status_parkir")
server.register_function(get_laporan, "get_laporan")


print("=" * 50)
print("           SERVER SISTEM PARKIR")
print("=" * 50)
print("Server aktif")
print("Port : 8000")
print("Status : Menunggu koneksi client...")
print("=" * 50)

server.serve_forever()