from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId
from flask import Flask, jsonify, request
from pymongo import MongoClient, DESCENDING

app = Flask(__name__)

cliente = MongoClient("mongodb://localhost:27017/")
db = cliente["seguranca"]
incidentes = db["incidentes"]

SEVERIDADES = {"baixa", "media", "alta", "critica"}
STATUS_VALIDOS = {"aberto", "em andamento", "resolvido"}


def serializar(documento):
    documento["_id"] = str(documento["_id"])

    if isinstance(documento.get("criado_em"), datetime):
        documento["criado_em"] = documento["criado_em"].isoformat()

    return documento


def validar_id(id):
    try:
        return ObjectId(id)
    except (InvalidId, TypeError):
        return None


@app.route("/api/incidentes", methods=["POST"])
def criar_incidente():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "corpo JSON inválido"}), 400

    obrigatorios = ["titulo", "severidade", "ip_origem"]

    if any(not dados.get(campo) for campo in obrigatorios):
        return jsonify({
            "erro": "titulo, severidade e ip_origem são obrigatórios"
        }), 400

    severidade = dados["severidade"].lower()

    if severidade not in SEVERIDADES:
        return jsonify({"erro": "severidade inválida"}), 400

    status = dados.get("status", "aberto").lower()

    if status not in STATUS_VALIDOS:
        return jsonify({"erro": "status inválido"}), 400

    incidente = {
        "titulo": dados["titulo"],
        "severidade": severidade,
        "status": status,
        "ip_origem": dados["ip_origem"],
        "criado_em": datetime.now(timezone.utc)
    }

    resultado = incidentes.insert_one(incidente)

    return jsonify({"id": str(resultado.inserted_id)}), 201


@app.route("/api/incidentes", methods=["GET"])
def listar_incidentes():
    try:
        pagina = int(request.args.get("pagina", 1))
        tamanho = int(request.args.get("tamanho", 10))
    except ValueError:
        return jsonify({"erro": "pagina e tamanho devem ser números"}), 400

    if pagina < 1 or tamanho < 1 or tamanho > 100:
        return jsonify({
            "erro": "pagina deve ser >= 1 e tamanho deve estar entre 1 e 100"
        }), 400

    filtro = {}

    severidade = request.args.get("severidade")
    status = request.args.get("status")

    if severidade:
        severidade = severidade.lower()

        if severidade not in SEVERIDADES:
            return jsonify({"erro": "severidade inválida"}), 400

        filtro["severidade"] = severidade

    if status:
        status = status.lower()

        if status not in STATUS_VALIDOS:
            return jsonify({"erro": "status inválido"}), 400

        filtro["status"] = status

    cursor = (
        incidentes.find(filtro)
        .sort("criado_em", DESCENDING)
        .skip((pagina - 1) * tamanho)
        .limit(tamanho)
    )

    resultados = [serializar(doc) for doc in cursor]

    return jsonify({
        "pagina": pagina,
        "tamanho": tamanho,
        "total": incidentes.count_documents(filtro),
        "incidentes": resultados
    }), 200


@app.route("/api/incidentes/<id>", methods=["GET"])
def obter_incidente(id):
    object_id = validar_id(id)

    if object_id is None:
        return jsonify({"erro": "id inválido"}), 400

    incidente = incidentes.find_one({"_id": object_id})

    if incidente is None:
        return jsonify({"erro": "incidente não encontrado"}), 404

    return jsonify(serializar(incidente)), 200


@app.route("/api/incidentes/<id>", methods=["PUT"])
def atualizar_incidente(id):
    object_id = validar_id(id)

    if object_id is None:
        return jsonify({"erro": "id inválido"}), 400

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict) or not dados:
        return jsonify({"erro": "corpo JSON inválido ou vazio"}), 400

    campos_permitidos = {
        "titulo", "severidade", "status", "ip_origem"
    }

    atualizacao = {
        campo: valor
        for campo, valor in dados.items()
        if campo in campos_permitidos
    }

    if not atualizacao:
        return jsonify({"erro": "nenhum campo válido para atualizar"}), 400

    if "severidade" in atualizacao:
        atualizacao["severidade"] = atualizacao["severidade"].lower()

        if atualizacao["severidade"] not in SEVERIDADES:
            return jsonify({"erro": "severidade inválida"}), 400

    if "status" in atualizacao:
        atualizacao["status"] = atualizacao["status"].lower()

        if atualizacao["status"] not in STATUS_VALIDOS:
            return jsonify({"erro": "status inválido"}), 400

    if any(
        not isinstance(valor, str) or not valor.strip()
        for valor in atualizacao.values()
    ):
        return jsonify({"erro": "os campos devem conter textos válidos"}), 400

    resultado = incidentes.update_one(
        {"_id": object_id},
        {"$set": atualizacao}
    )

    if resultado.matched_count == 0:
        return jsonify({"erro": "incidente não encontrado"}), 404

    return jsonify({"mensagem": "Incidente atualizado"}), 200


@app.route("/api/incidentes/<id>", methods=["DELETE"])
def excluir_incidente(id):
    object_id = validar_id(id)

    if object_id is None:
        return jsonify({"erro": "id inválido"}), 400

    resultado = incidentes.delete_one({"_id": object_id})

    if resultado.deleted_count == 0:
        return jsonify({"erro": "incidente não encontrado"}), 404

    return jsonify({"mensagem": "Removido"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)