import mysql.connector
from mysql.connector import IntegrityError, Error
from flask import Flask, jsonify, request

app = Flask(__name__)

CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "27072007",
    "database": "seguranca"
}


def get_db():
    return mysql.connector.connect(**CONFIG)


def erro_banco():
    return jsonify({"erro": "serviço indisponível"}), 500


def validar_usuario(dados, exigir_email=True):
    if not isinstance(dados, dict):
        return False

    if not dados.get("nome") or not dados.get("email"):
        return False

    if not isinstance(dados["nome"], str):
        return False

    if not isinstance(dados["email"], str):
        return False

    if "@" not in dados["email"]:
        return False

    if "nivel_acesso" in dados:
        try:
            nivel = int(dados["nivel_acesso"])
        except (ValueError, TypeError):
            return False

        if not 1 <= nivel <= 5:
            return False

    return True


@app.route("/api/usuarios", methods=["GET"])
def listar_usuarios():
    conexao = None

    try:
        conexao = get_db()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, nome, email, nivel_acesso
            FROM usuarios
            ORDER BY id
        """)

        usuarios = cursor.fetchall()

        return jsonify(usuarios), 200

    except Error:
        return erro_banco()

    finally:
        if conexao is not None and conexao.is_connected():
            conexao.close()


@app.route("/api/usuarios/<int:id>", methods=["GET"])
def obter_usuario(id):
    conexao = None

    try:
        conexao = get_db()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, nome, email, nivel_acesso
            FROM usuarios
            WHERE id = %s
            """,
            (id,)
        )

        usuario = cursor.fetchone()

        if usuario is None:
            return jsonify({"erro": "usuário não encontrado"}), 404

        return jsonify(usuario), 200

    except Error:
        return erro_banco()

    finally:
        if conexao is not None and conexao.is_connected():
            conexao.close()


@app.route("/api/usuarios", methods=["POST"])
def criar_usuario():
    dados = request.get_json(silent=True)

    if not validar_usuario(dados):
        return jsonify({
            "erro": "nome e email são obrigatórios e devem ser válidos"
        }), 400

    nivel = int(dados.get("nivel_acesso", 1))
    conexao = None

    try:
        conexao = get_db()
        cursor = conexao.cursor()

        cursor.execute(
            """
            INSERT INTO usuarios (nome, email, nivel_acesso)
            VALUES (%s, %s, %s)
            """,
            (dados["nome"], dados["email"], nivel)
        )

        conexao.commit()
        novo_id = cursor.lastrowid

        return jsonify({"id": novo_id}), 201

    except IntegrityError:
        return jsonify({"erro": "email já cadastrado"}), 409

    except Error:
        return erro_banco()

    finally:
        if conexao is not None and conexao.is_connected():
            conexao.close()


@app.route("/api/usuarios/<int:id>", methods=["PUT"])
def atualizar_usuario(id):
    dados = request.get_json(silent=True)

    if not validar_usuario(dados):
        return jsonify({
            "erro": "nome e email são obrigatórios e devem ser válidos"
        }), 400

    nivel = int(dados.get("nivel_acesso", 1))
    conexao = None

    try:
        conexao = get_db()
        cursor = conexao.cursor()

        cursor.execute(
            """
            UPDATE usuarios
            SET nome = %s, email = %s, nivel_acesso = %s
            WHERE id = %s
            """,
            (dados["nome"], dados["email"], nivel, id)
        )

        if cursor.rowcount == 0:
            cursor.execute(
                "SELECT id FROM usuarios WHERE id = %s",
                (id,)
            )

            if cursor.fetchone() is None:
                return jsonify({
                    "erro": "usuário não encontrado"
                }), 404

        conexao.commit()

        return jsonify({"mensagem": "Usuário atualizado"}), 200

    except IntegrityError:
        return jsonify({"erro": "email já cadastrado"}), 409

    except Error:
        return erro_banco()

    finally:
        if conexao is not None and conexao.is_connected():
            conexao.close()


@app.route("/api/usuarios/<int:id>", methods=["DELETE"])
def excluir_usuario(id):
    conexao = None

    try:
        conexao = get_db()
        cursor = conexao.cursor()

        cursor.execute(
            "DELETE FROM usuarios WHERE id = %s",
            (id,)
        )

        if cursor.rowcount == 0:
            return jsonify({
                "erro": "usuário não encontrado"
            }), 404

        conexao.commit()

        return jsonify({"mensagem": "Usuário removido"}), 200

    except Error:
        return erro_banco()

    finally:
        if conexao is not None and conexao.is_connected():
            conexao.close()


if __name__ == "__main__":
    app.run(debug=True, port=5000)