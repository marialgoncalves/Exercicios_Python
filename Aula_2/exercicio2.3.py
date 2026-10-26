from datetime import datetime
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["seguranca"]
eventos = db["eventos"]


def consultar(fonte=None, tipo=None, ip=None, desde=None):
    filtro = {}

    if fonte is not None:
        filtro["fonte"] = fonte

    if tipo is not None:
        filtro["tipo"] = tipo

    if ip is not None:
        filtro["ip"] = ip

    if desde is not None:
        filtro["timestamp"] = {"$gte": desde}

    resultados = eventos.find(filtro).sort("timestamp", 1)

    return list(resultados)


def exibir_resultados(resultados):
    if not resultados:
        print("Nenhum evento encontrado.")
        return

    for evento in resultados:
        print(
            f"Data: {evento.get('timestamp')} | "
            f"Fonte: {evento.get('fonte')} | "
            f"Tipo: {evento.get('tipo')} | "
            f"IP: {evento.get('ip')} | "
            f"Usuário: {evento.get('usuario', 'N/A')}"
        )


if __name__ == "__main__":
    try:
        client.admin.command("ping")
        print("Conectado ao MongoDB!")

        print("\n=== Falhas do IP 185.220.101.1 ===")
        resultado = consultar(
            tipo="FAIL",
            ip="185.220.101.1"
        )
        exibir_resultados(resultado)

        print("\n=== Todos os eventos da fonte auth ===")
        resultado = consultar(fonte="auth")
        exibir_resultados(resultado)

        print("\n=== Eventos a partir de 20/02/2025 ===")
        resultado = consultar(
            desde=datetime(2025, 2, 20, 0, 0, 0)
        )
        exibir_resultados(resultado)

    except Exception as erro:
        print(f"Erro: {erro}")

    finally:
        client.close()