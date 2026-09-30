from flask import Flask, render_template
from xmlrpc.client import ServerProxy, Fault
import socket


app = Flask(__name__)


IP_SERVER = "192.168.137.254"
PORT_SERVER = 8000


server = ServerProxy(
    f"http://{IP_SERVER}:{PORT_SERVER}",
    allow_none=True
)


@app.route("/")
def petugas():

    try:

        slot = server.lihat_slot()

        return render_template(
            "petugas.html",
            slot=slot,
            error=None
        )

    except Fault as e:

        return render_template(
            "petugas.html",
            slot={},
            error=f"XML-RPC Error: {e}"
        )

    except Exception as e:

        return render_template(
            "petugas.html",
            slot={},
            error=f"Koneksi ke server gagal: {e}"
        )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5003,
        debug=True
    )