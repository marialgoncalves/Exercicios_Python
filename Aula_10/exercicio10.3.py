import ipaddress
import time
import requests
import json

CACHE = {}
URL_BASE = "https://ipinfo.io"


def classificar_ip(ip):
    try:
        endereco = ipaddress.ip_address(ip)

        if endereco.is_private:
            return "Privado"
        return "Público"

    except ValueError:
        return "IP inválido"


def consultar_ip(ip, tentativas=3):
    # Utiliza o cache para evitar consultas repetidas
    if ip in CACHE:
        return CACHE[ip]

    classificacao = classificar_ip(ip)

    if classificacao == "IP inválido":
        resultado = {
            "ip": ip,
            "classificacao": classificacao,
            "informacoes": None
        }
        CACHE[ip] = resultado
        return resultado

    if classificacao == "Privado":
        resultado = {
            "ip": ip,
            "classificacao": classificacao,
            "informacoes": {
                "observacao": "IP privado; não consultado na API externa."
            }
        }
        CACHE[ip] = resultado
        return resultado

    # Consulta externa somente para IPs públicos
    for tentativa in range(tentativas):
        try:
            resposta = requests.get(
                f"{URL_BASE}/{ip}/json",
                timeout=10
            )

            if resposta.status_code == 429:
                espera = 2 ** tentativa
                print(
                    f"Limite da API atingido. "
                    f"Aguardando {espera}s..."
                )
                time.sleep(espera)
                continue

            resposta.raise_for_status()
            dados = resposta.json()

            resultado = {
                "ip": ip,
                "classificacao": classificacao,
                "informacoes": {
                    "hostname": dados.get("hostname"),
                    "cidade": dados.get("city"),
                    "regiao": dados.get("region"),
                    "pais": dados.get("country"),
                    "organizacao": dados.get("org")
                }
            }

            CACHE[ip] = resultado
            return resultado

        except requests.Timeout:
            print(f"Timeout ao consultar {ip}.")

        except requests.RequestException as erro:
            print(f"Erro ao consultar {ip}: {erro}")
            return {
                "ip": ip,
                "classificacao": classificacao,
                "erro": str(erro)
            }

        if tentativa < tentativas - 1:
            time.sleep(2 ** tentativa)

    return {
        "ip": ip,
        "classificacao": classificacao,
        "erro": "Número máximo de tentativas excedido."
    }


def gerar_relatorio(lista_ips):
    relatorio = []

    for ip in lista_ips:
        ip = ip.strip()

        if not ip:
            continue

        resultado = consultar_ip(ip)
        relatorio.append(resultado)

        print(f"\nIP: {resultado['ip']}")
        print(f"Classificação: {resultado['classificacao']}")

        if resultado.get("informacoes"):
            for chave, valor in resultado["informacoes"].items():
                print(f"{chave.capitalize()}: {valor}")

        elif resultado.get("erro"):
            print(f"Erro: {resultado['erro']}")

    with open("relatorio_ips.json", "w", encoding="utf-8") as arquivo:
        json.dump(relatorio, arquivo, ensure_ascii=False, indent=4)

    print("\nRelatório salvo em relatorio_ips.json")


if __name__ == "__main__":
    entrada = input(
        "Digite os IPs separados por vírgula: "
    )

    lista_ips = entrada.split(",")
    gerar_relatorio(lista_ips)