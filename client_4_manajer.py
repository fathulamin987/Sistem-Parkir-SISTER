from flask import Flask, render_template
import xmlrpc.client


app = Flask(__name__)

IP_SERVER = "localhost"
PORT_SERVER = 8000

server = xmlrpc.client.ServerProxy(
    f"http://{IP_SERVER}:{PORT_SERVER}",
    allow_none=True
)


@app.route("/")
def manajer():

    laporan = server.get_laporan()

    return render_template(
        "manajer.html",
        laporan=laporan
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5004,
        debug=True
    )