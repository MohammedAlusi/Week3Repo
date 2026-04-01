from flask import Flask, request, jsonify, render_template
import psycopg2

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    "dbname": "todo_db",
    "user": "postgres",
    "password": "123456",  # replace with your PostgreSQL password
    "host": "localhost",
    "port": 5432
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Serve HTML page
@app.route("/")
def home():
    return render_template("week3.html")

# GET all todos
@app.route("/todos", methods=["GET"])
def get_todos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, task, description, done FROM todos ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    todos = [{"id": r[0], "task": r[1], "description": r[2], "done": r[3]} for r in rows]
    return jsonify(todos)

# POST a new todo
@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.get_json()
    task = data.get("task")
    description = data.get("description", "")
    if not task:
        return jsonify({"error": "Task cannot be empty"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO todos (task, description) VALUES (%s, %s) RETURNING id, task, description, done;",
        (task, description)
    )
    new_todo = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": new_todo[0], "task": new_todo[1], "description": new_todo[2], "done": new_todo[3]}), 201

# PUT – edit todo text, description or mark done
@app.route("/todos/<int:id>", methods=["PUT"])
def update_todo(id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()

    if "task" in data:
        cur.execute("UPDATE todos SET task=%s WHERE id=%s;", (data["task"], id))
    if "description" in data:
        cur.execute("UPDATE todos SET description=%s WHERE id=%s;", (data["description"], id))
    if "done" in data:
        cur.execute("UPDATE todos SET done=%s WHERE id=%s;", (data["done"], id))

    conn.commit()
    cur.execute("SELECT id, task, description, done FROM todos WHERE id=%s;", (id,))
    updated = cur.fetchone()
    cur.close()
    conn.close()

    if not updated:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"id": updated[0], "task": updated[1], "description": updated[2], "done": updated[3]})

# DELETE a todo
@app.route("/todos/<int:id>", methods=["DELETE"])
def delete_todo(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM todos WHERE id=%s RETURNING id;", (id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not deleted:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"message": "Deleted"})

if __name__ == "__main__":
    app.run(debug=True)
    #1