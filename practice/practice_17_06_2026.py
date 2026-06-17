import os

from flask import Flask, jsonify
import json

app = Flask(__name__)

# users_json = os.path.dirname(os.path.abspath(__file__))
# # abspath - полный путь к скрипту (__file__),
# # затем отрезаем имя скрипта и оставляем только путь (dirname)

@app.route('/')
def hello_world():
    return "Hello, World! :D"

@app.route('/hello/<name>')
def hello_friend(name):
    return f'Hello, {name.title()}!'

@app.route('/double/<int:value>')
def double(value):
    return f'Number {value}, Doubled: {value * 2}'

@app.route('/square/<float:number>')
def float_square(number):
    return f"Float number: {number}, squared: {pow(number, 2)}"

@app.route('/<path:your_path>')
def reversed_path(your_path):
    return f'Your reversed path: {your_path[::-1]}'

# @app.route('/users')
# def users():
#     file_path = os.path.join(users_json, 'users.json')
#     with open(file_path, 'r', encoding='utf8') as f:
#         return jsonify(json.load(f))

@app.route('/users')
def users():
    print(f"JSON Path: {os.path.abspath('./practice/users.json')}")
    with open(os.path.abspath('./practice/users.json'), 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))

if __name__ == "__main__":
    app.run(debug=True)