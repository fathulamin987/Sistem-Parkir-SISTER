from xmlrpc.client import ServerProxy


IP_SERVER = "localhost"

server = ServerProxy(
    f"http://{IP_SERVER}:8000",
    allow_none=True
)


print("====================================")
print("       PINTU MASUK PARKIR")
print("====================================")

nomor_plat = input("Nomor Plat : ")
jenis = input("Jenis Kendaraan (Motor/Mobil) : ")

hasil = server.kendaraan_masuk(
    nomor_plat,
    jenis
)

print()

if hasil["status"]:

    data = hasil["data"]

    print("Kendaraan berhasil masuk.")
    print("------------------------------------")
    print("ID Tiket    :", data["id_tiket"])
    print("Nomor Plat  :", data["nomor_plat"])
    print("Jenis       :", data["jenis"])
    print("Slot        :", data["slot"])
    print("Waktu Masuk :", data["waktu_masuk"])
    print("------------------------------------")

else:

    print("Gagal:", hasil["pesan"])