from xmlrpc.client import ServerProxy


IP_SERVER = "localhost"

server = ServerProxy(
    f"http://{IP_SERVER}:8000",
    allow_none=True
)


print("====================================")
print("        MONITORING PARKIR")
print("====================================")

slot = server.lihat_slot()

for nomor_slot, status in slot.items():

    print(
        nomor_slot,
        "->",
        status
    )

print("------------------------------------")

laporan = server.laporan()

print("Slot Terisi :", laporan["slot_terisi"])
print("Slot Kosong :", laporan["slot_kosong"])