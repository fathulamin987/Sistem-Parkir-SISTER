from xmlrpc.client import ServerProxy


IP_SERVER = "localhost"

server = ServerProxy(
    f"http://{IP_SERVER}:8000",
    allow_none=True
)


print("====================================")
print("       PINTU KELUAR PARKIR")
print("====================================")

nomor_plat = input("Nomor Plat : ")

hasil = server.kendaraan_keluar(
    nomor_plat
)

print()

if hasil["status"]:

    data = hasil["data"]

    print("Kendaraan berhasil keluar.")
    print("------------------------------------")
    print("ID Tiket    :", data["id_tiket"])
    print("Nomor Plat  :", data["nomor_plat"])
    print("Jenis       :", data["jenis"])
    print("Slot        :", data["slot"])
    print("Waktu Masuk :", data["waktu_masuk"])
    print("Waktu Keluar:", data["waktu_keluar"])
    print("Durasi      :", data["durasi_jam"], "jam")
    print("Total Bayar : Rp", format(data["total_bayar"], ","))
    print("------------------------------------")

else:

    print("Gagal:", hasil["pesan"])