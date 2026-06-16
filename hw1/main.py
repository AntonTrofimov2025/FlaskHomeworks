from flask import Flask

app = Flask(__name__)

@app.route('/')
def hey_flask():
    return "Hello, Flask!"

@app.route('/user/<user_name>')
def hey_user(user_name):
    return f"Hello, {user_name}!! :)"

if __name__ == "__main__":
    app.run()