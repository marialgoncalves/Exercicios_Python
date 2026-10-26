import mysql.connector
from mysql.connector import Error, IntegrityError

CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "SUA_SENHA"
}


def conectar():
    conexao = mysql.connector.connect(**CONFIG)
    cursor = conexao.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS seguranca")
    cursor.close()
    conexao.database = "seguranca"

    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(150) NOT NULL UNIQUE,
            nivel_acesso INT NOT NULL CHECK (nivel_acesso BETWEEN 1 AND 5)
        )
    """)
    conexao.commit()
    cursor.close()

    return conexao


def cadastrar(conexao):
    nome = input("Nome: ")
    email = input("E-mail: ")

    try:
        nivel = int(input("Nível de acesso (1 a 5): "))
        if not 1 <= nivel <= 5:
            print("Erro: nível deve estar entre 1 e 5.")
            return
    except ValueError:
        print("Erro: informe um nível numérico.")
        return

    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO usuarios (nome, email, nivel_acesso)
            VALUES (%s, %s, %s)
            """,
            (nome, email, nivel)
        )
        conexao.commit()
        print("Usuário cadastrado!")

    except IntegrityError:
        conexao.rollback()
        print("Erro: email já existe ou os dados são inválidos.")

    finally:
        cursor.close()


def listar(conexao):
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT nome, email, nivel_acesso FROM usuarios ORDER BY nome"
    )

    usuarios = cursor.fetchall()

    if not usuarios:
        print("Nenhum usuário cadastrado.")

    for nome, email, nivel in usuarios:
        print(f"{nome} | {email} | nível {nivel}")

    cursor.close()


def buscar_por_email(conexao):
    email = input("E-mail do usuário: ")

    cursor = conexao.cursor()
    cursor.execute(
        "SELECT nome, email, nivel_acesso FROM usuarios WHERE email = %s",
        (email,)
    )

    usuario = cursor.fetchone()

    if usuario:
        print(
            f"{usuario[0]} | {usuario[1]} | "
            f"nível {usuario[2]}"
        )
    else:
        print("Usuário não encontrado.")

    cursor.close()


def atualizar_nivel(conexao):
    email = input("E-mail do usuário: ")

    try:
        nivel = int(input("Novo nível (1 a 5): "))
        if not 1 <= nivel <= 5:
            print("Erro: nível deve estar entre 1 e 5.")
            return
    except ValueError:
        print("Erro: informe um nível numérico.")
        return

    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE usuarios SET nivel_acesso = %s WHERE email = %s",
        (nivel, email)
    )

    conexao.commit()

    if cursor.rowcount > 0:
        print("Nível atualizado!")
    else:
        print("Usuário não encontrado ou nível sem alteração.")

    cursor.close()


def remover(conexao):
    email = input("E-mail do usuário que deseja remover: ")

    cursor = conexao.cursor()
    cursor.execute(
        "DELETE FROM usuarios WHERE email = %s",
        (email,)
    )

    conexao.commit()

    if cursor.rowcount > 0:
        print("Usuário removido!")
    else:
        print("Usuário não encontrado.")

    cursor.close()


def popular_dados(conexao):
    usuarios = [
        ("Carlos Silva", "carlos@empresa.com", 3),
        ("Ana Costa", "ana@empresa.com", 5),
        ("Bruno Lima", "bruno@empresa.com", 1)
    ]

    cursor = conexao.cursor()

    cursor.executemany(
        """
        INSERT IGNORE INTO usuarios (nome, email, nivel_acesso)
        VALUES (%s, %s, %s)
        """,
        usuarios
    )

    conexao.commit()
    cursor.close()


def menu(conexao):
    while True:
        print("\n=== GERENCIAMENTO DE USUÁRIOS ===")
        print("1 - Cadastrar usuário")
        print("2 - Listar usuários")
        print("3 - Buscar por e-mail")
        print("4 - Alterar nível de acesso")
        print("5 - Remover usuário")
        print("6 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar(conexao)
        elif opcao == "2":
            listar(conexao)
        elif opcao == "3":
            buscar_por_email(conexao)
        elif opcao == "4":
            atualizar_nivel(conexao)
        elif opcao == "5":
            remover(conexao)
        elif opcao == "6":
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    conexao = None

    try:
        conexao = conectar()
        print("Conectado ao MySQL!")

        popular_dados(conexao)
        menu(conexao)

    except Error as erro:
        print(f"Erro no MySQL: {erro}")

    finally:
        if conexao and conexao.is_connected():
            conexao.close()