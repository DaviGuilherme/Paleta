from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from database import Database
from chat import chat

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

database = Database()

@app.route('/chat', methods=['GET'])
@cross_origin()
def get_message():
    data = request.args
    query = data.get('query')
    categoria = data.get('categoria')
    chat_id = data.get('id')

    perguntas = database.ler_perguntas(categoria)
    response_body = {}

    try:
        response = chat(chat_id, perguntas, query)
        response_body = {
            'response': response
        }
        
    except Exception as e:
        print(e)
        # response_body = {
        #     'response': f'{{ "categoria": "{categoria}", "cor": ["vermelho", "verde", "azul", "amarelo"], "prazo": "24/11/2023", "resolucao": "2480x3508", "titulo": "Programa de televisão de variedades", "publico-alvo": "jovens" }}'
        # }

    print(response_body)
    return jsonify(response_body)

@app.route('/salvar_respostas', methods=['POST'])
@cross_origin()
def salvar_respostas():
    dados = request.json

    response = database.salvar_respostas(dados)
    return jsonify({'idPedido': response})

@app.route('/pedidos/detalhes', methods=['GET'])
@cross_origin()
def recuperar_detalhes():
    data = request.args
    id_pedido = data.get('id_pedido')

    response = database.recuperar_pedido(id_pedido)
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3031, debug=True)