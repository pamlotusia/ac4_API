from flask import Flask, jsonify, request
import json
import requests
import mysql.connector

app = Flask(__name__)

bancoDeDados = mysql.connector.connect(
    host="localhost", user="root", password="pamela22", database="ac3")


@app.route('/v1/funcionarios', methods=["GET"])
def listar():
    selectAllSql = f"select * from funcionarios"
    cursor = bancoDeDados.cursor()
    cursor.execute(selectAllSql)
    resultado = cursor.fetchall()
    bancoDeDados.close()
    if resultado is None:
        api_url = "http://127.0.0.1:5000/tipo"
        response = requests.get(api_url)
        retornaApi = response.json()
    else:
        retornaApi = resultado

    return jsonify(retornaApi)


@app.route('/funcionarios/registrar', methods=["POST"])
def registrar():
    data = request.get_json()

    nome = data['nome']
    sobrenome = data['sobrenome']
    funcao = data['funcao']

    insertSql = f"INSERT INTO funcionarios (nome, sobrenome, funcao) VALUES ('{nome}', {sobrenome}, '{funcao}')"
    cursor = bancoDeDados.cursor()
    cursor.execute(insertSql)
    bancoDeDados.commit()
    bancoDeDados.close()

    api_url = "http://127.0.0.1:5000/tipo/v1"
    valores = {
        'nome': nome,
        'sobrenome': sobrenome,
        'funcao': funcao
    }
    response = requests.post(api_url, json=valores)

    # Verificar a resposta da API externa
    if response.status_code == 200:
        return jsonify({'message': 'Dados inseridos com sucesso!'})
    else:
        return jsonify({'message': 'Erro ao inserir dados na API externa.'}), 500


@app.route('/funcionarios/deletar', methods=["DELETE"])
def deletar():
    deleteSql = f"DELETE FROM funcionarios WHERE nome = 'Marcelo'"
    cursor = bancoDeDados.cursor()
    cursor.execute(deleteSql)
    bancoDeDados.commit()
    bancoDeDados.close()

    api_url = "http://127.0.0.1:5000/tipo/v1"
    response = requests.post(api_url)
    return response


if __name__ == '__main__':
    app.run(debug=True, port=5002)
