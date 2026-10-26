import json
import time
import requests

BASE_URL = "https://api.github.com"
resultados = {}


def requisicao(url, params=None):
    """Faz requisições com tratamento de erros e rate limit."""
    for tentativa in range(3):
        try:
            resposta = requests.get(
                url,
                params=params,
                timeout=20,
                headers={"Accept": "application/vnd.github+json"}
            )

            if resposta.status_code in (403, 429):
                restante = resposta.headers.get("X-RateLimit-Remaining")
                if resposta.status_code == 429 or restante == "0":
                    espera = min(2 ** tentativa, 30)
                    print(f"Limite de requisições atingido. Aguardando {espera}s...")
                    time.sleep(espera)
                    continue

                print("Acesso negado pela API do GitHub (403).")
                return None

            resposta.raise_for_status()
            return resposta.json()

        except requests.Timeout:
            print("Tempo limite excedido.")
        except requests.ConnectionError:
            print("Erro de conexão com o GitHub.")
            return None
        except requests.HTTPError as erro:
            if erro.response is not None and erro.response.status_code == 404:
                print("Usuário ou repositório não encontrado.")
            else:
                print(f"Erro HTTP: {erro}")
            return None
        except requests.RequestException as erro:
            print(f"Erro na requisição: {erro}")
            return None

        if tentativa < 2:
            time.sleep(2 ** tentativa)

    print("Não foi possível concluir a requisição.")
    return None


def buscar_usuario():
    usuario = input("Nome do usuário GitHub: ").strip()
    dados = requisicao(f"{BASE_URL}/users/{usuario}")

    if not dados:
        return

    resultados["perfil"] = dados

    print(f"\n=== Perfil: {dados.get('login')} ===")
    print(f"Nome: {dados.get('name') or 'Não informado'}")
    print(f"Repos públicos: {dados.get('public_repos', 0)}")
    print(f"Seguidores: {dados.get('followers', 0)}")


def listar_repositorios():
    usuario = input("Nome do usuário GitHub: ").strip()
    repositorios = []
    pagina = 1

    while True:
        lote = requisicao(
            f"{BASE_URL}/users/{usuario}/repos",
            params={
                "page": pagina,
                "per_page": 100,
                "sort": "updated"
            }
        )

        if lote is None:
            return

        if not lote:
            break

        repositorios.extend(lote)
        pagina += 1

    resultados["repositorios"] = repositorios

    print(f"\n=== Repositórios de {usuario} ===")

    for i, repo in enumerate(repositorios, start=1):
        print(
            f"{i}. {repo['name']} | "
            f"★ {repo.get('stargazers_count', 0)} | "
            f"{repo.get('language') or 'Não informado'}"
        )

    print(f"\nTotal: {len(repositorios)} repositórios.")


def detalhar_repositorio():
    usuario = input("Nome do usuário GitHub: ").strip()
    nome_repo = input("Nome do repositório: ").strip()

    dados = requisicao(
        f"{BASE_URL}/repos/{usuario}/{nome_repo}"
    )

    if not dados:
        return

    resultados["detalhe_repositorio"] = dados

    print(f"\nRepositório: {dados.get('full_name')}")
    print(f"Descrição: {dados.get('description') or 'Sem descrição'}")
    print(f"Linguagem: {dados.get('language') or 'Não informada'}")
    print(f"Estrelas: {dados.get('stargazers_count', 0)}")
    print(f"Forks: {dados.get('forks_count', 0)}")
    print(f"URL: {dados.get('html_url')}")


def salvar_json():
    if not resultados:
        print("Nenhum resultado para salvar. Consulte algo primeiro.")
        return

    nome_arquivo = input(
        "Nome do arquivo [github_resultados.json]: "
    ).strip() or "github_resultados.json"

    if not nome_arquivo.endswith(".json"):
        nome_arquivo += ".json"

    try:
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(resultados, arquivo, ensure_ascii=False, indent=4)

        print(f"Resultados salvos em {nome_arquivo}")

    except OSError as erro:
        print(f"Erro ao salvar o arquivo: {erro}")


def menu():
    while True:
        print("\n=== EXPLORADOR DO GITHUB ===")
        print("1. Buscar usuário")
        print("2. Listar repositórios")
        print("3. Detalhar repositório")
        print("4. Salvar resultados em JSON")
        print("0. Sair")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            buscar_usuario()
        elif opcao == "2":
            listar_repositorios()
        elif opcao == "3":
            detalhar_repositorio()
        elif opcao == "4":
            salvar_json()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()