from flask import Flask, render_template
from xmlrpc.client import ServerProxy, Fault

app = Flask(__name__)

IP_SERVER = "localhost"
PORT_SERVER = 8000

server = ServerProxy(
    f"http://{IP_SERVER}:{PORT_SERVER}",
    allow_none=True
)


@app.route("/")
def manajer():

    try:
        laporan = server.get_riwayat()

        return render_template(
            "manajer.html",
            laporan=laporan,
            error=None
        )

    except Exception as e:

        return render_template(
            "manajer.html",
            laporan=[],
            error=str(e)
        )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5004,
        debug=True
    )