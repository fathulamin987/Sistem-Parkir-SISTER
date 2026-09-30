from flask import Flask, render_template, request
import xmlrpc.client


app = Flask(__name__)


IP_SERVER = "192.168.137.254"
PORT_SERVER = 8000


server = xmlrpc.client.ServerProxy(
    f"http://{IP_SERVER}:{PORT_SERVER}",
    allow_none=True
)


@app.route("/", methods=["GET", "POST"])
def masuk():

    hasil = None

    if request.method == "POST":

        no_plat = request.form["no_plat"].upper().strip()

        jenis = request.form["jenis"]

        try:

            hasil = server.kendaraan_masuk(
                no_plat,
                jenis
            )

        except Exception as e:

            hasil = {

                "status": False,

                "pesan": "Gagal terhubung ke server: " + str(e)
            }

    return render_template(
        "masuk.html",
        hasil=hasil
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )