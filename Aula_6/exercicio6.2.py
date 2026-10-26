import re
from flask import Flask, jsonify, request

app = Flask(__name__)


def verificar_senha(senha):
    criterios = {
        "tamanho_min": len(senha) >= 8,
        "maiuscula": any(c.isupper() for c in senha),
        "minuscula": any(c.islower() for c in senha),
        "numero": any(c.isdigit() for c in senha),
        "especial": bool(re.search(r"[^a-zA-Z0-9]", senha))
    }

    atendidos = sum(criterios.values())

    if atendidos == 5:
        forca = "Muito forte"
    elif atendidos == 4:
        forca = "Forte"
    elif atendidos == 3:
        forca = "Média"
    elif atendidos == 2:
        forca = "Fraca"
    else:
        forca = "Muito fraca"

    return {
        "forca": forca,
        "criterios": criterios
    }


@app.route("/api/analisar-senha", methods=["POST"])
def analisar_senha():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Corpo JSON inválido"}), 400

    senha = dados.get("senha")

    if not isinstance(senha, str) or not senha:
        return jsonify({
            "erro": "campo 'senha' obrigatório"
        }), 400

    resultado = verificar_senha(senha)

    return jsonify(resultado), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)