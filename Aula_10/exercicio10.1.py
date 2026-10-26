import requests

URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


def consultar_cve(cve_id):
    try:
        resposta = requests.get(
            URL,
            params={"cveId": cve_id},
            timeout=30
        )

        resposta.raise_for_status()
        dados = resposta.json()

        vulnerabilidades = dados.get("vulnerabilities", [])

        if not vulnerabilidades:
            print("CVE não encontrada.")
            return

        cve = vulnerabilidades[0]["cve"]

        # Extrai a descrição em inglês
        descricao = next(
            (
                item["value"]
                for item in cve.get("descriptions", [])
                if item.get("lang") == "en"
            ),
            "Descrição não disponível."
        )

        # Extrai CVSS e severidade
        metricas = cve.get("metrics", {})
        cvss = None
        severidade = "Não disponível"

        for tipo in ("cvssMetricV40", "cvssMetricV31",
                     "cvssMetricV30", "cvssMetricV2"):
            if metricas.get(tipo):
                dados_cvss = metricas[tipo][0]["cvssData"]
                cvss = dados_cvss.get("baseScore")
                severidade = dados_cvss.get(
                    "baseSeverity",
                    "Não informada"
                )
                break

        print(f"\nCVE: {cve_id}")
        print(f"CVSS: {cvss if cvss is not None else 'Não disponível'}")
        print(f"Severidade: {severidade}")
        print(f"Descrição: {descricao}")

    except requests.Timeout:
        print("Tempo limite excedido ao consultar o NVD.")

    except requests.HTTPError as erro:
        if erro.response is not None and erro.response.status_code == 404:
            print("CVE não encontrada.")
        else:
            print(f"Erro HTTP: {erro}")

    except requests.RequestException as erro:
        print(f"Erro de conexão: {erro}")

    except (ValueError, KeyError, IndexError) as erro:
        print(f"Erro ao interpretar a resposta da API: {erro}")


if __name__ == "__main__":
    identificador = input("Digite a CVE (ex.: CVE-2021-44228): ").strip().upper()
    consultar_cve(identificador)