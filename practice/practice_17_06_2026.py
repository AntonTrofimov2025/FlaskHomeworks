from flask import Flask

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)