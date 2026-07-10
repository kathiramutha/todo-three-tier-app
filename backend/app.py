from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os

app = Flask(__name__)
CORS(app)

connection = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database="todo",
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True
)

@app.route("/")
def home():
    return "Todo API Running"

# Get all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks")
    result = cursor.fetchall()
    cursor.close()
    return jsonify(result), 200

# Add a new task
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()

    if not data or "task" not in data:
        return jsonify({"error": "Task is required"}), 400

    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO tasks (task) VALUES (%s)",
        (data["task"],)
    )
    cursor.close()

    return jsonify({"message": "Task added"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
