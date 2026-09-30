from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
from datetime import datetime
import uuid
import threading


# =========================
# KONFIGURASI SERVER
# =========================

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


kendaraan_parkir = {}
riwayat_transaksi = []

lock = threading.Lock()


# =========================
# SERVER MULTI CLIENT
# =========================

class ThreadedXMLRPCServer(
    ThreadingMixIn,
    SimpleXMLRPCServer
):
    pass


# =========================
# KENDARAAN MASUK
# =========================

def kendaraan_masuk(no_plat, jenis):

    with lock:

        if no_plat in kendaraan_parkir:

            return {
                "status": False,
                "pesan": "Kendaraan masih berada di dalam parkir."
            }


        slot_kosong = None

        for nomor_slot, data in slot_parkir.items():

            if data is None:

                slot_kosong = nomor_slot
                break


        if slot_kosong is None:

            return {
                "status": False,
                "pesan": "Parkiran penuh."
            }


        id_tiket = str(uuid.uuid4())[:8]

        waktu_masuk = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


        data = {
            "id_tiket": id_tiket,
            "no_plat": no_plat,
            "jenis": jenis,
            "slot": slot_kosong,
            "waktu_masuk": waktu_masuk
        }


        slot_parkir[slot_kosong] = data

        kendaraan_parkir[no_plat] = data


        return {
            "status": True,
            "pesan": "Kendaraan berhasil masuk.",
            "data": data
        }


# =========================
# KENDARAAN KELUAR
# =========================

def kendaraan_keluar(no_plat):

    with lock:

        if no_plat not in kendaraan_parkir:

            return {
                "status": False,
                "pesan": "Kendaraan tidak ditemukan."
            }


        data = kendaraan_parkir[no_plat]


        waktu_masuk = datetime.strptime(
            data["waktu_masuk"],
            "%Y-%m-%d %H:%M:%S"
        )

        waktu_keluar = datetime.now()


        durasi = (
            waktu_keluar - waktu_masuk
        ).total_seconds() / 3600


        durasi_bayar = max(
            1,
            int(durasi + 0.9999)
        )


        if data["jenis"].lower() == "motor":

            tarif = 2000

        else:

            tarif = 5000


        total_bayar = durasi_bayar * tarif


        id_transaksi = str(
            uuid.uuid4()
        )[:8]


        transaksi = {

            "id_transaksi": id_transaksi,

            "no_plat": no_plat,

            "jenis": data["jenis"],

            "slot": data["slot"],

            "durasi": durasi_bayar,

            "total_bayar": total_bayar,

            "waktu_masuk": data["waktu_masuk"],

            "waktu_keluar":
                waktu_keluar.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
        }


        slot_parkir[data["slot"]] = None

        del kendaraan_parkir[no_plat]

        riwayat_transaksi.append(transaksi)


        return {

            "status": True,

            "pesan":
                "Kendaraan berhasil keluar.",

            "data": transaksi
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
                    "TERISI - "
                    + data["no_plat"]
                )


        return hasil


# =========================
# LAPORAN
# =========================

def laporan():

    with lock:

        total_pendapatan = 0

        for transaksi in riwayat_transaksi:

            total_pendapatan += (
                transaksi["total_bayar"]
            )


        jumlah_terisi = 0

        for data in slot_parkir.values():

            if data is not None:

                jumlah_terisi += 1


        jumlah_kosong = (
            len(slot_parkir)
            - jumlah_terisi
        )


        return {

            "total_pendapatan":
                total_pendapatan,

            "jumlah_kendaraan":
                len(kendaraan_parkir),

            "jumlah_transaksi":
                len(riwayat_transaksi),

            "jumlah_slot":
                len(slot_parkir),

            "jumlah_terisi":
                jumlah_terisi,

            "jumlah_kosong":
                jumlah_kosong
        }


# =========================
# RIWAYAT
# =========================

def get_riwayat():

    with lock:

        return riwayat_transaksi[-10:]


# =========================
# CEK SERVER
# =========================

def cek_server():

    return {

        "status": True,

        "pesan":
            "Server parkir aktif.",

        "port": PORT_SERVER
    }


# =========================
# BUAT SERVER
# =========================

server = ThreadedXMLRPCServer(
    (IP_SERVER, PORT_SERVER),
    allow_none=True
)


# =========================
# DAFTARKAN METHOD RPC
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
    laporan,
    "laporan"
)

server.register_function(
    get_riwayat,
    "get_riwayat"
)

server.register_function(
    cek_server,
    "cek_server"
)


# =========================
# JALANKAN SERVER
# =========================

print()
print("=" * 50)
print("        SISTEM PARKIR XML-RPC")
print("=" * 50)
print("Server aktif")
print("Listen    : 0.0.0.0")
print("Port      : 8000")
print()
print("Method RPC:")
print("- kendaraan_masuk")
print("- kendaraan_keluar")
print("- lihat_slot")
print("- laporan")
print("- get_riwayat")
print("- cek_server")
print("=" * 50)
print()


server.serve_forever()