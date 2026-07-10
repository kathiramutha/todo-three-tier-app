from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os

app = Flask(__name__)

# Enable CORS
CORS(app)

# Connect to RDS
connection = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database="todo",   # Your RDS database name
    cursorclass=pymysql.cursors.DictCursor
)

@app.route("/")
def home():
    return "Todo API Running"

# Get all todos
@app.route("/todos", methods=["GET"])
def get_todos():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM todos")
    result = cursor.fetchall()
    return jsonify(result), 200

# Add a new todo
@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.get_json()

    if not data or "task" not in data:
        return jsonify({"error": "Task is required"}), 400

    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO todos (task) VALUES (%s)",
        (data["task"],)
    )
    connection.commit()

    return jsonify({"message": "Todo added"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
