# Relatório de Auditoria de Segurança

## 1. SQL Injection — OWASP A05: Injection

**Trecho vulnerável:**
```python
cur.execute("SELECT * FROM users WHERE nome='" + nome + "'")
```

**Vulnerabilidade:** a entrada do usuário é concatenada diretamente à consulta SQL. Um atacante pode alterar a consulta executada pelo banco.

**Correção:** utilizar consultas parametrizadas.

```python
cur.execute(
    "SELECT * FROM users WHERE nome = %s",
    (nome,)
)
```

## 2. Cross-Site Scripting (XSS) — OWASP A05: Injection

**Trecho vulnerável:**
```python
return f"<h1>Bem-vindo {nome}</h1>" + str(dados)
```

**Vulnerabilidade:** os dados são inseridos diretamente no HTML. Uma entrada maliciosa pode fazer o navegador executar JavaScript.

**Correção:** escapar os dados apresentados na página ou utilizar templates Jinja2 com escape automático habilitado.

```python
from markupsafe import escape

return f"<h1>Bem-vindo {escape(nome)}</h1>"
```

Os dados retornados pelo banco também devem ser tratados adequadamente antes de serem inseridos no HTML.

## 3. Configuração insegura — OWASP A02: Security Misconfiguration

**Trecho vulnerável:**
```python
app.run(debug=True, host="0.0.0.0")
```

**Vulnerabilidade:** o modo de depuração pode expor informações internas e recursos interativos de diagnóstico. O endereço `0.0.0.0` permite que o servidor escute em todas as interfaces de rede disponíveis.

**Correção:** desativar o modo de depuração em produção e utilizar um servidor WSGI apropriado.

```python
app.run(debug=False)
```

## 4. Segredo exposto no código — OWASP A04/A02

**Trecho vulnerável:**
```python
SENHA_DB = "123456"
```

**Vulnerabilidade:** a senha está escrita diretamente no código e é fraca. Ela pode ser exposta por meio do repositório, dos arquivos compartilhados ou do acesso ao código-fonte.

**Correção:** armazenar a credencial em uma variável de ambiente e utilizar uma senha forte.

```python
import os

SENHA_DB = os.getenv("DB_PASSWORD")
```

Também é necessário restringir as permissões do usuário do banco de dados e evitar o compartilhamento de credenciais.

## 5. Ausência de logs e monitoramento — OWASP A09: Security Logging and Alerting Failures

**Problema:** a aplicação não registra acessos nem tentativas de erro.

**Vulnerabilidade:** atividades suspeitas e tentativas de exploração podem passar despercebidas, dificultando a investigação de incidentes.

**Correção:** implementar registros de eventos relevantes, como falhas de autenticação, erros da aplicação e tentativas de acesso indevido.

```python
import logging

logging.basicConfig(
    filename="seguranca.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logging.info("Aplicação iniciada")
logging.warning("Tentativa de acesso suspeita")
logging.error("Erro durante o processamento")
```

Os logs não devem registrar senhas, tokens ou outros segredos. Também devem ter acesso restrito e ser monitorados.

## Conclusão

A auditoria identificou cinco problemas: SQL Injection, XSS, configuração insegura, exposição de credenciais e ausência de registros de segurança. A aplicação dessas correções reduz os riscos de exploração e melhora a proteção dos dados e a capacidade de detectar incidentes.