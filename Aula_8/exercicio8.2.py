import os
import time

import mysql.connector
from mysql.connector import Error
from flask import Flask, jsonify, request
from werkzeug.security import check_password_hash

app = Flask(__name__)

CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.getenv("27072007"),
    "database": "seguranca"
}

MAX_TENTATIVAS = 5
TEMPO_BLOQUEIO = 300

tentativas = {}


def get_db():
    return mysql.connector.connect(**CONFIG)


@app.route("/login", methods=["POST"])
def login():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "corpo JSON inválido"}), 400

    usuario = dados.get("usuario")
    senha = dados.get("senha")

    if (
        not isinstance(usuario, str)
        or not isinstance(senha, str)
        or not usuario.strip()
        or not senha
    ):
        return jsonify({"erro": "usuário e senha são obrigatórios"}), 400

    ip = request.remote_addr or "desconhecido"
    agora = time.time()

    registro = tentativas.get(ip, {
        "quantidade": 0,
        "bloqueado_ate": 0
    })

    if agora < registro["bloqueado_ate"]:
        return jsonify({"erro": "Muitas tentativas. Tente mais tarde."}), 429

    conexao = None

    try:
        conexao = get_db()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute(
            "SELECT senha_hash FROM login_usuarios WHERE usuario = %s",
            (usuario,)
        )

        resultado = cursor.fetchone()

        if (
            resultado
            and check_password_hash(resultado["senha_hash"], senha)
        ):
            tentativas.pop(ip, None)
            return jsonify({"mensagem": "Login OK"}), 200

        registro["quantidade"] += 1

        if registro["quantidade"] >= MAX_TENTATIVAS:
            registro["bloqueado_ate"] = agora + TEMPO_BLOQUEIO
            registro["quantidade"] = 0

        tentativas[ip] = registro

        return jsonify({"erro": "Credenciais inválidas"}), 401

    except Error:
        app.logger.exception("Falha ao consultar o banco de login")
        return jsonify({"erro": "serviço indisponível"}), 500

    finally:
        if conexao is not None and conexao.is_connected():
            conexao.close()


if __name__ == "__main__":
    app.run(debug=False, port=5000)