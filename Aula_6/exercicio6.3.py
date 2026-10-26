import ipaddress
from flask import Flask, jsonify

app = Flask(__name__)

blacklist = {
    "185.220.101.1",
    "45.33.32.156",
    "91.240.118.172"
}


@app.route("/api/checar-ip/<ip>", methods=["GET"])
def checar_ip(ip):
    try:
        endereco = ipaddress.ip_address(ip)

    except ValueError:
        return jsonify({"erro": "IP inválido"}), 400

    return jsonify({
        "ip": str(endereco),
        "na_blacklist": str(endereco) in blacklist,
        "tipo": "privado" if endereco.is_private else "publico"
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)