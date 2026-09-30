from flask import Flask, render_template
from xmlrpc.client import ServerProxy


app = Flask(__name__)


IP_SERVER = "192.168.137.254"
PORT_SERVER = 8000


server = ServerProxy(
    f"http://{IP_SERVER}:{PORT_SERVER}",
    allow_none=True
)


@app.route("/")
def manajer():

    try:

        laporan = server.laporan()

        riwayat = server.riwayat_transaksi()

        return render_template(
            "manajer.html",
            laporan=laporan,
            riwayat=riwayat
        )

    except Exception as e:

        return render_template(
            "manajer.html",
            laporan={},
            riwayat=[],
            error=str(e)
        )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5004,
        debug=True
    )