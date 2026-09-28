from flask import Flask, render_template, request
import xmlrpc.client


app = Flask(__name__)

IP_SERVER = "10.164.164.29"
PORT_SERVER = 8000


server = xmlrpc.client.ServerProxy(
    f"http://{IP_SERVER}:{PORT_SERVER}",
    allow_none=True
)


@app.route("/", methods=["GET", "POST"])
def masuk():

    hasil = None

    if request.method == "POST":

        no_plat = request.form["no_plat"]
        jenis = request.form["jenis"]

        try:

            hasil = server.kendaraan_masuk(
                no_plat,
                jenis
            )

            # Memastikan nomor plat ikut ditampilkan
            if hasil and hasil.get("status"):

                if "data" not in hasil:
                    hasil["data"] = {}

                hasil["data"]["no_plat"] = no_plat

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