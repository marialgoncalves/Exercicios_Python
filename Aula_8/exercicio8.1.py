from flask import Flask, request, redirect, url_for, render_template_string
from markupsafe import escape

app = Flask(__name__)

alertas = []

HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Dashboard de Alertas</title>
</head>
<body>
    <h1>Dashboard de Alertas</h1>

    <form method="POST" action="/alertas">
        <label>Título:</label>
        <input type="text" name="titulo" required>

        <label>Descrição:</label>
        <textarea name="descricao" required></textarea>

        <button type="submit">Cadastrar alerta</button>
    </form>

    <h2>Alertas cadastrados</h2>

    {% for alerta in alertas %}
        <div>
            <h3>{{ alerta.titulo }}</h3>
            <p>{{ alerta.descricao }}</p>
        </div>
    {% endfor %}
</body>
</html>
"""


@app.route("/", methods=["GET"])
def dashboard():
    return render_template_string(HTML, alertas=alertas)


@app.route("/alertas", methods=["POST"])
def cadastrar_alerta():
    titulo = request.form.get("titulo", "").strip()
    descricao = request.form.get("descricao", "").strip()

    if not titulo or not descricao:
        return "Título e descrição são obrigatórios.", 400

    alertas.append({
        "titulo": titulo,
        "descricao": descricao
    })

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)