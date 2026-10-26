import mysql.connector
from mysql.connector import Error

CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "SUA_SENHA",
    "database": "seguranca"
}


def conectar():
    conexao = mysql.connector.connect(**CONFIG)
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(150) NOT NULL UNIQUE,
            nivel_acesso INT NOT NULL
        )
    """)

    cursor.executemany(
        """
        INSERT IGNORE INTO usuarios (nome, email, nivel_acesso)
        VALUES (%s, %s, %s)
        """,
        [
            ("Carlos Silva", "carlos@empresa.com", 3),
            ("Ana Costa", "ana@empresa.com", 5),
            ("Bruno Lima", "bruno@empresa.com", 1)
        ]
    )

    conexao.commit()
    cursor.close()
    return conexao


def buscar_inseguro(conexao, nome):
    cursor = conexao.cursor()

    # Demonstração intencionalmente vulnerável: somente no laboratório local.
    query = f"SELECT id, nome, email FROM usuarios WHERE nome = '{nome}'"
    cursor.execute(query)

    resultados = cursor.fetchall()
    cursor.close()
    return resultados


def buscar_seguro(conexao, nome):
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id, nome, email FROM usuarios WHERE nome = %s",
        (nome,)
    )

    resultados = cursor.fetchall()
    cursor.close()
    return resultados


if __name__ == "__main__":
    conexao = None

    try:
        conexao = conectar()
        print("Conectado ao MySQL!")

        entrada_maliciosa = "' OR '1'='1"

        resultado_inseguro = buscar_inseguro(
            conexao,
            entrada_maliciosa
        )

        resultado_seguro = buscar_seguro(
            conexao,
            entrada_maliciosa
        )

        print(f"\nEntrada de teste: {entrada_maliciosa}")

        print(
            f"[INSEGURO] -> {len(resultado_inseguro)} "
            "usuários retornados (VAZAMENTO!)"
        )

        print(
            f"[SEGURO] -> {len(resultado_seguro)} "
            "usuários retornados (defesa OK)"
        )

        print(
            "\nConclusão: a consulta parametrizada trata "
            "a entrada como texto literal."
        )

    except Error as erro:
        print(f"Erro no MySQL: {erro}")

    finally:
        if conexao and conexao.is_connected():
            conexao.close()