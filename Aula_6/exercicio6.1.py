from flask import Flask, jsonify, request

app = Flask(__name__)

usuarios = []
proximo_id = 1


@app.route("/api/usuarios", methods=["GET"])
def listar_usuarios():
    return jsonify(usuarios), 200


@app.route("/api/usuarios/<int:id>", methods=["GET"])
def buscar_usuario(id):
    usuario = next(
        (u for u in usuarios if u["id"] == id),
        None
    )

    if usuario is None:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    return jsonify(usuario), 200


@app.route("/api/usuarios", methods=["POST"])
def cadastrar_usuario():
    global proximo_id

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Corpo JSON inválido"}), 400

    nome = dados.get("nome")
    email = dados.get("email")
    nivel = dados.get("nivel")

    if not nome or not isinstance(nome, str):
        return jsonify({"erro": "Nome obrigatório"}), 400

    if not email or not isinstance(email, str):
        return jsonify({"erro": "E-mail obrigatório"}), 400

    if any(u["email"].lower() == email.lower() for u in usuarios):
        return jsonify({"erro": "email já existe"}), 400

    if isinstance(nivel, bool) or not isinstance(nivel, int) or not 1 <= nivel <= 5:
        return jsonify({"erro": "nível inválido"}), 400

    usuario = {
        "id": proximo_id,
        "nome": nome,
        "email": email,
        "nivel": nivel
    }

    usuarios.append(usuario)
    proximo_id += 1

    return jsonify(usuario), 201


@app.route("/api/usuarios/<int:id>", methods=["PUT"])
def atualizar_usuario(id):
    usuario = next(
        (u for u in usuarios if u["id"] == id),
        None
    )

    if usuario is None:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Corpo JSON inválido"}), 400

    nome = dados.get("nome", usuario["nome"])
    email = dados.get("email", usuario["email"])
    nivel = dados.get("nivel", usuario["nivel"])

    if not isinstance(nome, str) or not nome.strip():
        return jsonify({"erro": "Nome inválido"}), 400

    if not isinstance(email, str) or not email.strip():
        return jsonify({"erro": "E-mail inválido"}), 400

    if any(
        u["id"] != id and u["email"].lower() == email.lower()
        for u in usuarios
    ):
        return jsonify({"erro": "email já existe"}), 400

    if isinstance(nivel, bool) or not isinstance(nivel, int) or not 1 <= nivel <= 5:
        return jsonify({"erro": "nível inválido"}), 400

    usuario.update({
        "nome": nome,
        "email": email,
        "nivel": nivel
    })

    return jsonify(usuario), 200


@app.route("/api/usuarios/<int:id>", methods=["DELETE"])
def remover_usuario(id):
    usuario = next(
        (u for u in usuarios if u["id"] == id),
        None
    )

    if usuario is None:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    usuarios.remove(usuario)

    return jsonify({"mensagem": "Removido"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)