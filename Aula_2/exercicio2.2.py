from datetime import datetime
from pathlib import Path
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["seguranca"]
eventos = db["eventos"]


def processar_linha(linha):
    partes = linha.strip().split()

    if len(partes) < 5:
        return None

    try:
        timestamp = datetime.strptime(
            f"{partes[0]} {partes[1]}",
            "%Y-%m-%d %H:%M:%S"
        )

        tipo = partes[2]

        dados = {}
        for parte in partes[3:]:
            if "=" in parte:
                chave, valor = parte.split("=", 1)
                dados[chave] = valor

        usuario = dados.get("usuario")
        ip = dados.get("ip")

        if not usuario or not ip:
            return None

        return {
            "timestamp": timestamp,
            "fonte": "auth",
            "tipo": tipo,
            "usuario": usuario,
            "ip": ip
        }

    except ValueError:
        return None


def importar_logs():
    caminho = Path("auth.log")

    if not caminho.exists():
        print("Erro: arquivo auth.log não encontrado!")
        return

    documentos = []

    with caminho.open("r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            documento = processar_linha(linha)

            if documento is not None:
                documentos.append(documento)

    if not documentos:
        print("Nenhum evento válido encontrado.")
        return

    resultado = eventos.insert_many(documentos)

    print(f"Total de eventos inseridos: {len(resultado.inserted_ids)}")

    pipeline = [
        {"$match": {"tipo": "FAIL"}},
        {
            "$group": {
                "_id": "$ip",
                "total": {"$sum": 1}
            }
        },
        {"$sort": {"total": -1, "_id": 1}},
        {"$limit": 5}
    ]

    print("\n=== Top IPs por falhas de login ===")

    resultados = list(eventos.aggregate(pipeline))

    if not resultados:
        print("Nenhuma falha de login encontrada.")
    else:
        for resultado in resultados:
            print(
                f"{resultado['_id']} -> "
                f"{resultado['total']} falhas"
            )


if __name__ == "__main__":
    try:
        client.admin.command("ping")
        print("Conectado ao MongoDB!")
        importar_logs()
    except Exception as erro:
        print(f"Erro: {erro}")
    finally:
        client.close()