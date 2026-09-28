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
def keluar():

    hasil = None

    if request.method == "POST":

        no_plat = request.form["no_plat"]

        hasil = server.kendaraan_keluar(
            no_plat
        )

    return render_template(
        "keluar.html",
        hasil=hasil
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5002,
        debug=True
    )