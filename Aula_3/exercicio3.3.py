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
        CREATE TABLE IF NOT EXISTS alertas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tipo VARCHAR(50) NOT NULL,
            descricao TEXT,
            ip_origem VARCHAR(45) NOT NULL,
            severidade ENUM('baixa', 'media', 'alta', 'critica')
                NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conexao.commit()
    cursor.close()
    return conexao


def inserir_dados_teste(conexao):
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM alertas")
    total = cursor.fetchone()[0]

    if total == 0:
        dados = [
            ("BRUTE_FORCE", "Múltiplas falhas de login", "185.220.101.1", "critica"),
            ("BRUTE_FORCE", "Tentativas de acesso", "185.220.101.1", "critica"),
            ("BRUTE_FORCE", "Tentativas contra SSH", "185.220.101.1", "alta"),
            ("BRUTE_FORCE", "Tentativas contra conta admin", "185.220.101.1", "alta"),
            ("PORT_SCAN", "Varredura de portas", "45.33.32.156", "critica"),
            ("PORT_SCAN", "Portas abertas detectadas", "45.33.32.156", "alta"),
            ("PORT_SCAN", "Nova varredura detectada", "45.33.32.156", "media"),
            ("XSS", "Possível script na URL", "192.168.1.50", "alta"),
            ("XSS", "Entrada suspeita em formulário", "192.168.1.51", "media"),
            ("SQLI", "Possível SQL Injection", "10.0.0.15", "baixa")
        ]

        cursor.executemany(
            """
            INSERT INTO alertas
                (tipo, descricao, ip_origem, severidade)
            VALUES (%s, %s, %s, %s)
            """,
            dados
        )

        conexao.commit()
        print("10 alertas de teste inseridos.")

    else:
        print(
            f"A tabela já possui {total} alertas. "
            "Mantendo os registros existentes."
        )

    cursor.close()


def relatorio_severidade(conexao):
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT severidade, COUNT(*) AS total
        FROM alertas
        GROUP BY severidade
        ORDER BY FIELD(
            severidade, 'critica', 'alta', 'media', 'baixa'
        )
    """)

    print("\n=== Por severidade ===")

    for severidade, total in cursor.fetchall():
        print(f"{severidade}: {total}")

    cursor.close()


def relatorio_tipo(conexao):
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT tipo, COUNT(*) AS total
        FROM alertas
        GROUP BY tipo
        ORDER BY total DESC, tipo ASC
    """)

    print("\n=== Por tipo ===")

    for tipo, total in cursor.fetchall():
        print(f"{tipo}: {total}")

    cursor.close()


def top_ips(conexao):
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT ip_origem, COUNT(*) AS total
        FROM alertas
        GROUP BY ip_origem
        ORDER BY total DESC, ip_origem ASC
        LIMIT 5
    """)

    print("\n=== Top IPs de origem ===")

    for ip, total in cursor.fetchall():
        print(f"{ip} -> {total} alertas")

    cursor.close()


if __name__ == "__main__":
    conexao = None

    try:
        conexao = conectar()
        print("Conectado ao MySQL!")

        inserir_dados_teste(conexao)
        relatorio_severidade(conexao)
        relatorio_tipo(conexao)
        top_ips(conexao)

    except Error as erro:
        print(f"Erro no MySQL: {erro}")

    finally:
        if conexao and conexao.is_connected():
            conexao.close()