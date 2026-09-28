from xmlrpc.client import ServerProxy


IP_SERVER = "localhost"

server = ServerProxy(
    f"http://{IP_SERVER}:8000",
    allow_none=True
)


print("====================================")
print("       LAPORAN MANAJEMEN PARKIR")
print("====================================")


laporan = server.laporan()

print("Total Transaksi        :", laporan["total_transaksi"])
print("Total Pendapatan       : Rp",
      format(laporan["total_pendapatan"], ","))

print("Kendaraan Sedang Parkir:",
      laporan["kendaraan_sedang_parkir"])

print("Slot Terisi            :",
      laporan["slot_terisi"])

print("Slot Kosong            :",
      laporan["slot_kosong"])


print()
print("====================================")
print("       5 TRANSAKSI TERAKHIR")
print("====================================")


riwayat = server.riwayat_transaksi()

if len(riwayat) == 0:

    print("Belum ada transaksi.")

else:

    for data in riwayat:

        print("------------------------------------")
        print("ID Tiket   :", data["id_tiket"])
        print("Nomor Plat :", data["nomor_plat"])
        print("Jenis      :", data["jenis"])
        print("Durasi     :", data["durasi_jam"], "jam")
        print("Total      : Rp",
              format(data["total_bayar"], ","))

print("------------------------------------")