from flask import Flask, render_template
from xmlrpc.client import ServerProxy

app = Flask(__name__)

IP_SERVER = "10.164.164.29"

server = ServerProxy(
    f"http://{IP_SERVER}:8000",
    allow_none=True
)


@app.route("/")
def manajer():

    laporan = server.laporan()

    riwayat = server.riwayat_transaksi()

    return render_template(
        "manajer.html",
        laporan=laporan,
        riwayat=riwayat
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5004,
        debug=True
    )