import os.path

from flask import Flask, request, jsonify
from pydantic import BaseModel, EmailStr, ValidationError, ConfigDict
import sqlite3

app = Flask(__name__)

folder = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(folder, 'test.db')

def get_db():
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    print("Initializing...")
    with get_db() as conn:
        # Added UNIQIE to avoid duplicates
        conn.execute("""CREATE TABLE IF NOT EXISTS users
                        (
                            id    INTEGER PRIMARY KEY AUTOINCREMENT,
                            name  TEXT    NOT NULL,
                            age   INTEGER NOT NULL,
                            email TEXT    NOT NULL UNIQUE 
                        )""")

class User(BaseModel):
    name: str
    age: int
    email: EmailStr

    model_config = ConfigDict(extra='forbid')

# users
@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        with get_db() as conn:
            data = conn.execute("""SELECT * FROM users""").fetchall()
            return jsonify([dict(row) for row in data]), 200
            # res = []
            # for row in data:
            #     res.append(dict(row))
            # return jsonify(res), 200

    if request.method == 'POST':
        # silent=True prevents from aborting, if received broken JSON (not string)
        try:
            user = User(**request.get_json(silent=True))
        except ValidationError:
            return jsonify({"error": "Wrong user data"}), 400

        try:
            with get_db() as conn:
                conn.execute("""INSERT INTO users (name, age, email)
                                VALUES (?, ?, ?)""",
                             (user.name, user.age, user.email))
                conn.commit()
        except sqlite3.IntegrityError:
            return jsonify({"error": "User with this email already exists"}), 400

        return jsonify({"message": "User created"}), 201


if __name__ == "__main__":
    init_db()
    app.run(debug=True)