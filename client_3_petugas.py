from flask import Flask, render_template
from xmlrpc.client import ServerProxy

app = Flask(__name__)

IP_SERVER = "10.164.164.29"

server = ServerProxy(
    f"http://{IP_SERVER}:8000",
    allow_none=True
)


@app.route("/")
def petugas():

    slot = server.lihat_slot()

    return render_template(
        "petugas.html",
        slot=slot
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5003,
        debug=True
    )