from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
import uuid
from datetime import datetime
import threading


IP_SERVER = "0.0.0.0"
PORT_SERVER = 8000


# =========================
# DATA PARKIR
# =========================

slot_parkir = {
    "A01": None,
    "A02": None,
    "A03": None,
    "A04": None,
    "A05": None,
    "B01": None,
    "B02": None,
    "B03": None,
    "B04": None,
    "B05": None
}

riwayat = []

lock = threading.Lock()


# =========================
# KENDARAAN MASUK
# =========================

def kendaraan_masuk(no_plat, jenis):

    with lock:

        for nomor_slot, data in slot_parkir.items():

            if data is None:

                id_tiket = str(uuid.uuid4())[:8]

                data_kendaraan = {
                    "id_tiket": id_tiket,
                    "no_plat": no_plat,
                    "jenis": jenis,
                    "slot": nomor_slot,
                    "waktu_masuk": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                }

                slot_parkir[nomor_slot] = data_kendaraan

                return {
                    "status": True,
                    "pesan": "Kendaraan berhasil masuk",
                    "data": data_kendaraan
                }

        return {
            "status": False,
            "pesan": "Parkir penuh"
        }


# =========================
# KENDARAAN KELUAR
# =========================

def kendaraan_keluar(no_plat):

    with lock:

        for nomor_slot, data in slot_parkir.items():

            if data is not None and data["no_plat"] == no_plat:

                waktu_masuk = datetime.strptime(
                    data["waktu_masuk"],
                    "%Y-%m-%d %H:%M:%S"
                )

                waktu_keluar = datetime.now()

                durasi = (
                    waktu_keluar - waktu_masuk
                ).total_seconds() / 3600

                durasi_jam = max(1, int(durasi + 0.999))

                if data["jenis"].lower() == "motor":
                    tarif = 2000
                else:
                    tarif = 5000

                total_bayar = durasi_jam * tarif

                transaksi = {
                    "id_transaksi": str(uuid.uuid4())[:8],
                    "no_plat": data["no_plat"],
                    "jenis": data["jenis"],
                    "slot": nomor_slot,
                    "durasi": durasi_jam,
                    "total_bayar": total_bayar,
                    "waktu_keluar": waktu_keluar.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                }

                riwayat.append(transaksi)

                slot_parkir[nomor_slot] = None

                return {
                    "status": True,
                    "pesan": "Kendaraan berhasil keluar",
                    "data": transaksi
                }

        return {
            "status": False,
            "pesan": "Nomor plat tidak ditemukan"
        }


# =========================
# LIHAT SLOT
# =========================

def lihat_slot():

    with lock:

        hasil = {}

        for nomor_slot, data in slot_parkir.items():

            if data is None:
                hasil[nomor_slot] = "KOSONG"
            else:
                hasil[nomor_slot] = (
                    "TERISI - " + data["no_plat"]
                )

        return hasil


# =========================
# STATUS PARKIR
# =========================

def get_status_parkir():

    with lock:

        total = len(slot_parkir)

        terisi = 0

        for data in slot_parkir.values():

            if data is not None:
                terisi += 1

        kosong = total - terisi

        return {
            "total_slot": total,
            "terisi": terisi,
            "kosong": kosong
        }


# =========================
# RIWAYAT
# =========================

def get_riwayat():

    with lock:
        return riwayat


# =========================
# SERVER XML RPC
# =========================

class ThreadedXMLRPCServer(
    ThreadingMixIn,
    SimpleXMLRPCServer
):

    pass


server = ThreadedXMLRPCServer(
    (IP_SERVER, PORT_SERVER),
    allow_none=True
)


# =========================
# REGISTER FUNCTION
# =========================

server.register_function(
    kendaraan_masuk,
    "kendaraan_masuk"
)

server.register_function(
    kendaraan_keluar,
    "kendaraan_keluar"
)

server.register_function(
    lihat_slot,
    "lihat_slot"
)

server.register_function(
    get_status_parkir,
    "get_status_parkir"
)

server.register_function(
    get_riwayat,
    "get_riwayat"
)


print("===================================")
print("     SERVER SISTEM PARKIR")
print("===================================")
print("Server berjalan pada:")
print("0.0.0.0:8000")
print("")
print("Method XML-RPC:")
print("- kendaraan_masuk")
print("- kendaraan_keluar")
print("- lihat_slot")
print("- get_status_parkir")
print("- get_riwayat")
print("")
print("Server siap menerima client...")
print("===================================")


server.serve_forever()