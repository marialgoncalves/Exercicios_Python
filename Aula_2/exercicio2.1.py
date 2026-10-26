from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient("mongodb://localhost:27017/")
db = client["seguranca"]
ativos = db["ativos"]

ativos.create_index("ip", unique=True)

dados_iniciais = [
    {
        "nome": "SRV-WEB01",
        "tipo": "servidor",
        "ip": "192.168.1.10",
        "status": "ativo"
    },
    {
        "nome": "PC-RH03",
        "tipo": "estacao",
        "ip": "192.168.1.45",
        "status": "ativo"
    },
    {
        "nome": "SW-CORE01",
        "tipo": "switch",
        "ip": "192.168.1.1",
        "status": "inativo"
    }
]

for ativo in dados_iniciais:
    ativos.update_one(
        {"ip": ativo["ip"]},
        {"$setOnInsert": ativo},
        upsert=True
    )


def cadastrar():
    nome = input("Nome do ativo: ")
    tipo = input("Tipo do ativo: ")
    ip = input("IP do ativo: ")
    status = input("Status (ativo/inativo): ").lower()

    if status not in ("ativo", "inativo"):
        print("Status inválido!")
        return

    try:
        ativos.insert_one({
            "nome": nome,
            "tipo": tipo,
            "ip": ip,
            "status": status
        })
        print("Ativo cadastrado!")

    except DuplicateKeyError:
        print("Erro: IP já cadastrado!")


def listar():
    print("\n=== Inventário de Ativos ===")

    for ativo in ativos.find().sort("nome", 1):
        print(
            f"Nome: {ativo['nome']} | "
            f"Tipo: {ativo['tipo']} | "
            f"IP: {ativo['ip']} | "
            f"Status: {ativo['status']}"
        )


def buscar():
    ip = input("Digite o IP que deseja buscar: ")
    ativo = ativos.find_one({"ip": ip})

    if ativo:
        print("\nAtivo encontrado:")
        print(f"Nome: {ativo['nome']}")
        print(f"Tipo: {ativo['tipo']}")
        print(f"IP: {ativo['ip']}")
        print(f"Status: {ativo['status']}")
    else:
        print("Ativo não encontrado!")


def atualizar_status():
    ip = input("Digite o IP do ativo: ")
    status = input("Novo status (ativo/inativo): ").lower()

    if status not in ("ativo", "inativo"):
        print("Status inválido!")
        return

    resultado = ativos.update_one(
        {"ip": ip},
        {"$set": {"status": status}}
    )

    if resultado.matched_count:
        print("Status atualizado!")
    else:
        print("Ativo não encontrado!")


def remover():
    ip = input("Digite o IP do ativo que deseja remover: ")

    resultado = ativos.delete_one({"ip": ip})

    if resultado.deleted_count:
        print("Ativo removido!")
    else:
        print("Ativo não encontrado!")


def menu():
    while True:
        print("\n=== MENU DE INVENTÁRIO ===")
        print("1 - Cadastrar ativo")
        print("2 - Listar ativos")
        print("3 - Buscar ativo por IP")
        print("4 - Atualizar status")
        print("5 - Remover ativo")
        print("6 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar()
        elif opcao == "2":
            listar()
        elif opcao == "3":
            buscar()
        elif opcao == "4":
            atualizar_status()
        elif opcao == "5":
            remover()
        elif opcao == "6":
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    try:
        client.admin.command("ping")
        print("Conectado ao MongoDB!")
        menu()
    except Exception as erro:
        print(f"Erro ao conectar ao MongoDB: {erro}")
    finally:
        client.close()