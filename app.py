from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import csv
import os
from datetime import datetime
def carregar_solicitacoes():
solicitacoes = []
if os.path.exists(ARQUIVO):
with open(
ARQUIVO, "r", newline="", encoding="utf-8"
) as arquivo:
leitor = csv.DictReader(arquivo)
solicitacoes.extend(leitor)
return solicitacoes
import csv
from datetime import datetime
import os
from flask import Flask, redirect, render_template, request

# Inicialização do app
app = Flask(__name__)

# Configuração de caminhos e constantes
PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))
ARQUIVO = os.path.join(PASTA_PROJETO, "solicitacoes.csv")

CAMPOS = [
    "id",
    "nome",
    "tipo_usuario",
    "sala",
    "equipamento",
    "descricao",
    "data",
    "status",
]


def carregar_solicitacoes():
    """Lê e retorna a lista de solicitações cadastradas no CSV."""
    solicitacoes = []
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", newline="", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)
            solicitacoes.extend(leitor)
    return solicitacoes


def salvar_solicitacoes(solicitacoes):
    """Sobrescreve o arquivo CSV com a lista atualizada de solicitações."""
    with open(ARQUIVO, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS)
        escritor.writeheader()
        escritor.writerows(solicitacoes)


def gerar_novo_id(solicitacoes):
    """Gera um ID numérico sequencial baseado no maior ID existente."""
    ids = []
    for solicitacao in solicitacoes:
        try:
            ids.append(int(solicitacao["id"]))
        except (ValueError, KeyError):
            pass
    return str(max(ids, default=0) + 1)


@app.route("/")
def inicio():
    """Rota principal: carrega as solicitações e renderiza a página."""
    solicitacoes = carregar_solicitacoes()
    return render_template("index.html", solicitacoes=solicitacoes)


@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    """Rota para processar o envio do formulário."""
    solicitacoes = carregar_solicitacoes()

    nova_solicitacao = {
        "id": gerar_novo_id(solicitacoes),
        "nome": request.form.get("nome", "").strip(),
        "tipo_usuario": request.form.get("tipo_usuario", "").strip(),
        "sala": request.form.get("sala", "").strip(),
        "equipamento": request.form.get("equipamento", "").strip(),
        "descricao": request.form.get("descricao", "").strip(),
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "status": "Pendente",
    }

    campos_obrigatorios = [
        "nome",
        "tipo_usuario",
        "sala",
        "equipamento",
        "descricao",
    ]

    # Validação no Python para garantir que nada vá em branco
    if all(nova_solicitacao[campo] for campo in campos_obrigatorios):
        solicitacoes.append(nova_solicitacao)
        salvar_solicitacoes(solicitacoes)

    return redirect("/")


@app.route("/concluir/<id_solicitacao>")
def concluir(id_solicitacao):
    """Rota para alterar o status de uma solicitação para Concluído."""
    solicitacoes = carregar_solicitacoes()
    for solicitacao in solicitacoes:
        if solicitacao.get("id") == id_solicitacao:
            solicitacao["status"] = "Concluído"
            break
    salvar_solicitacoes(solicitacoes)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
