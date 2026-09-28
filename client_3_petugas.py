from flask import Flask, render_template
import xmlrpc.client


app = Flask(__name__)

IP_SERVER = "10.164.164.29"
PORT_SERVER = 8000


server = xmlrpc.client.ServerProxy(
    f"http://{IP_SERVER}:{PORT_SERVER}",
    allow_none=True
)


@app.route("/")
def petugas():

    data = server.get_status_parkir()

    terisi = 0
    kosong = 0

    for item in data:

        if item["status"] == "TERISI":
            terisi += 1
        else:
            kosong += 1

    return render_template(
        "petugas.html",
        data=data,
        terisi=terisi,
        kosong=kosong
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5003,
        debug=True
    )