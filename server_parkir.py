from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
from datetime import datetime
import threading
import uuid


HOST = "0.0.0.0"
PORT = 8000


# ==============================
# DATA PARKIR
# ==============================

slot_parkir = {
    "A01": None,
    "A02": None,
    "A03": None,
    "A04": None,
    "A05": None,
    "A06": None,
    "B01": None,
    "B02": None,
    "B03": None,
    "B04": None,
    "B05": None,
    "B06": None
}

riwayat = []

lock = threading.Lock()


# ==============================
# SERVER TEST
# ==============================

def cek_server():

    return {
        "status": True,
        "pesan": "Server parkir aktif"
    }


# ==============================
# KENDARAAN MASUK
# ==============================

def kendaraan_masuk(no_plat, jenis):

    with lock:

        no_plat = no_plat.upper().strip()

        # Cek kendaraan sudah parkir
        for slot, data in slot_parkir.items():

            if data is not None:

                if data["no_plat"] == no_plat:

                    return {
                        "status": False,
                        "pesan": "Kendaraan tersebut masih berada di parkir."
                    }

        # Cari slot kosong
        slot_ditemukan = None

        for slot, data in slot_parkir.items():

            if data is None:

                slot_ditemukan = slot
                break

        if slot_ditemukan is None:

            return {
                "status": False,
                "pesan": "Parkir penuh."
            }

        # Buat ID tiket
        id_tiket = str(uuid.uuid4())[:8].upper()

        waktu_masuk = datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

        data_kendaraan = {

            "id_tiket": id_tiket,

            "no_plat": no_plat,

            "jenis": jenis,

            "slot": slot_ditemukan,

            "waktu_masuk": waktu_masuk
        }

        # Simpan ke slot
        slot_parkir[slot_ditemukan] = data_kendaraan

        # Simpan riwayat
        riwayat.append({

            "id_tiket": id_tiket,

            "no_plat": no_plat,

            "jenis": jenis,

            "slot": slot_ditemukan,

            "waktu_masuk": waktu_masuk,

            "waktu_keluar": None,

            "durasi_jam": 0,

            "total_bayar": 0
        })

        return {

            "status": True,

            "pesan": "Kendaraan berhasil masuk.",

            "data": data_kendaraan
        }


# ==============================
# KENDARAAN KELUAR
# ==============================

def kendaraan_keluar(no_plat):

    with lock:

        no_plat = no_plat.upper().strip()

        data_kendaraan = None
        slot_ditemukan = None

        # Cari kendaraan
        for slot, data in slot_parkir.items():

            if data is not None:

                if data["no_plat"] == no_plat:

                    data_kendaraan = data
                    slot_ditemukan = slot
                    break

        # Tidak ditemukan
        if data_kendaraan is None:

            return {

                "status": False,

                "pesan": "Kendaraan tidak ditemukan."
            }

        waktu_keluar = datetime.now()

        waktu_masuk = datetime.strptime(
            data_kendaraan["waktu_masuk"],
            "%d-%m-%Y %H:%M:%S"
        )

        durasi = waktu_keluar - waktu_masuk

        durasi_jam = int(
            durasi.total_seconds() / 3600
        )

        if durasi_jam < 1:

            durasi_jam = 1

        # Tarif
        if data_kendaraan["jenis"].lower() == "motor":

            tarif = 2000

        else:

            tarif = 5000

        total_bayar = durasi_jam * tarif

        waktu_keluar_string = waktu_keluar.strftime(
            "%d-%m-%Y %H:%M:%S"
        )

        # Kosongkan slot
        slot_parkir[slot_ditemukan] = None

        # Update riwayat
        for data in riwayat:

            if data["id_tiket"] == data_kendaraan["id_tiket"]:

                data["waktu_keluar"] = waktu_keluar_string

                data["durasi_jam"] = durasi_jam

                data["total_bayar"] = total_bayar

                break

        transaksi = {

            "id_transaksi": str(uuid.uuid4())[:8].upper(),

            "id_tiket": data_kendaraan["id_tiket"],

            "no_plat": data_kendaraan["no_plat"],

            "jenis": data_kendaraan["jenis"],

            "slot": slot_ditemukan,

            "durasi": durasi_jam,

            "total_bayar": total_bayar,

            "waktu_keluar": waktu_keluar_string
        }

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

        for slot, data in slot_parkir.items():

            if data is None:

                hasil[slot] = "KOSONG"

            else:

                hasil[slot] = (
                    "TERISI - "
                    + data["no_plat"]
                )

        return hasil


# ==============================
# LAPORAN
# ==============================

def laporan():

    with lock:

        total_pendapatan = 0

        total_transaksi = 0

        for data in riwayat:

            if data["waktu_keluar"] is not None:

                total_transaksi += 1

                total_pendapatan += data["total_bayar"]

        total_slot = len(slot_parkir)

        slot_terisi = 0

        for data in slot_parkir.values():

            if data is not None:

                slot_terisi += 1

        slot_kosong = total_slot - slot_terisi

        return {

            "total_transaksi": total_transaksi,

            "total_pendapatan": total_pendapatan,

            "kendaraan_sedang_parkir": slot_terisi,

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
# SERVER XML-RPC
# ==============================

class ThreadedXMLRPCServer(
    ThreadingMixIn,
    SimpleXMLRPCServer
):

    pass


server = ThreadedXMLRPCServer(
    (HOST, PORT),
    allow_none=True
)


# Aktifkan introspection
server.register_introspection_functions()


# Daftarkan semua method
server.register_function(
    cek_server,
    "cek_server"
)

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
    laporan,
    "laporan"
)

server.register_function(
    riwayat_transaksi,
    "riwayat_transaksi"
)


# ==============================
# JALANKAN SERVER
# ==============================

print("=" * 50)
print("       SERVER SISTEM PARKIR")
print("=" * 50)
print("IP Server : 192.168.137.254")
print("Port      : 8000")
print()
print("Method RPC:")

print("- cek_server")
print("- kendaraan_masuk")
print("- kendaraan_keluar")
print("- lihat_slot")
print("- laporan")
print("- riwayat_transaksi")

print()
print("Server siap menerima koneksi...")
print("=" * 50)


server.serve_forever()