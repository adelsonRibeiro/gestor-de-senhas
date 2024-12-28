from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
from servicos import Connection
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
nova_senha=True
caminho_banco = os.getenv("caminho_banco", "database/db.db")


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/gera_senha_normal')
def gera_senha_normal():
    global nova_senha
    conexao = Connection(caminho_banco)
    senha = conexao.gera_senha('N')
    print(senha)
    nova_senha=True
    return str(senha)


@app.route('/gera_senha_prioridade')
def gera_senha_prioritaria():
    global nova_senha
    conexao = Connection(caminho_banco)
    senha = conexao.gera_senha('P')
    print(senha)
    nova_senha=True
    return str(senha)


@app.route('/chama_cliente')
def chamar_cliente():
    global nova_senha
    try:
        conexao = Connection(caminho_banco)
        cliente_atual = conexao.chama_cliente()
        nova_senha=True
        return cliente_atual
    except Exception:
        return 'Não foi encontrado nenhuma senha'


@app.route('/finalizar')
def finalizar():
    global nova_senha
    try:
        conexao = Connection(caminho_banco)
        conexao.finaliza_atendimento()
        nova_senha=True
        return 'ok'
    except Exception as e:
        return e


@app.route('/ausente')
def ausente():
    global nova_senha
    try:
        conexao = Connection(caminho_banco)
        conexao.marca_ausente()
        nova_senha=True
        return 'ok'
    except Exception as e:
        return e
    

@socketio.on('message', namespace="/clientes")
def mensagem(lista):
    global nova_senha
    if lista == 'sim':
        nova_senha = True
    if nova_senha:
        conexao = Connection(caminho_banco)
        ativos = conexao.consulta_ativos()
        nova_senha = False
        send(ativos)
    else:
        send(None)


@socketio.on('message', namespace="/senha-painel")
def mensagem(msg):
    send(msg, broadcast=True)


@app.route('/recepcao')
def recepcao():
    return render_template("recepcao.html")


@app.route('/atendimento')
def atendimento():
    return render_template("atendimento.html")


@app.route('/painel')
def painel():
    return render_template("painel.html")


if __name__ == "__main__":
    socketio.run(app, debug=True)
