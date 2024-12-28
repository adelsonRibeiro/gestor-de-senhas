from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
from servicos import Connection
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
caminho_banco = os.getenv("caminho_banco", "database/db.db")


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/gera_senha_normal')
def gera_senha_normal():
    conexao = Connection(caminho_banco)
    senha = conexao.gera_senha('N')
    print(senha)
    mensagem()
    return str(senha)


@app.route('/gera_senha_prioridade')
def gera_senha_prioritaria():
    conexao = Connection(caminho_banco)
    senha = conexao.gera_senha('P')
    print(senha)
    mensagem()
    return str(senha)


@app.route('/chama_cliente')
def chamar_cliente():
    try:
        conexao = Connection(caminho_banco)
        cliente_atual = conexao.chama_cliente()
        mensagem()
        return cliente_atual
    except Exception:
        return 'Não foi encontrado nenhuma senha'


@app.route('/finalizar')
def finalizar():
    try:
        conexao = Connection(caminho_banco)
        conexao.finaliza_atendimento()
        mensagem()
        return 'ok'
    except Exception as e:
        return e


@app.route('/ausente')
def ausente():
    try:
        conexao = Connection(caminho_banco)
        conexao.marca_ausente()
        mensagem()
        return 'ok'
    except Exception as e:
        return e
    

@socketio.on('message', namespace="/clientes")
def mensagem():
    conexao = Connection(caminho_banco)
    ativos = conexao.consulta_ativos()
    send(ativos, broadcast=True, namespace='/clientes')


@socketio.on('message', namespace="/senha-painel")
def mensagem_painel(msg):
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
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
