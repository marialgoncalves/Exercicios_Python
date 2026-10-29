import os
from openai import OpenAI, OpenAIError

api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    raise ValueError("Configure a variável de ambiente OPENAI_API_KEY.")

client = OpenAI(api_key=api_key)

historico = [
    {
        "role": "system",
        "content": (
            "Você é um assistente especializado em segurança cibernética. "
            "Responda em português, com clareza e foco educacional."
        )
    }
]


def conversar(pergunta):
    historico.append({"role": "user", "content": pergunta})

    try:
        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=historico,
            temperature=0.3
        )

        texto = resposta.choices[0].message.content
        historico.append({"role": "assistant", "content": texto})
        return texto

    except OpenAIError as erro:
        # Remove a pergunta que não recebeu resposta para manter
        # o histórico consistente.
        historico.pop()
        return f"Erro ao consultar a API: {erro}"


def main():
    print("Chatbot de Segurança — digite /sair para encerrar.")

    while True:
        pergunta = input("\nVocê: ").strip()

        if pergunta.lower() == "/sair":
            print("Assistente: Até logo!")
            break

        if not pergunta:
            continue

        print("Assistente:", conversar(pergunta))


if __name__ == "__main__":
    main()