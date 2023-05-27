from flask import Flask
import requests
import json

app = Flask(__name__)


@app.route('/tipo', methods=["GET"])
def home():
    api_url = "https://jsonplaceholder.typicode.com/todos/1"
    response = requests.get(api_url)
    return response.json()


@app.route('/tipo/v1', methods=["POST"])
def cadastrar():
    api_url = "https://jsonplaceholder.typicode.com/todos"
    enviar = {"userId": 1, "title": "Buy milk", "completed": True}
    response = requests.post(api_url, json=enviar)
    return response.json()


@app.route('/tipo/v1', methods=["DELETE"])
def apagar():
    api_url = "https://jsonplaceholder.typicode.com/todos/1"
    response = requests.delete(api_url)
    return response.json()


if __name__ == '__main__':
    app.run(debug=True)
