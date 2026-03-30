from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# In-memory "database"
todos = []

# Serve HTML page
@app.route("/")
def home():
    return render_template("week3.html")

# GET all todos
@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify(todos)

# POST a new todo
@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.get_json()
    task = data.get("task")
    if not task:
        return jsonify({"error": "Task cannot be empty"}), 400

    # Assign a unique ID
    next_id = max([todo["id"] for todo in todos], default=0) + 1
    todo = {
        "id": next_id,
        "task": task,
        "done": False
    }
    todos.append(todo)
    return jsonify(todo), 201

# PUT – edit todo text or mark done
@app.route("/todos/<int:id>", methods=["PUT"])
def update_todo(id):
    data = request.get_json()
    for todo in todos:
        if todo["id"] == id:
            if "task" in data:
                todo["task"] = data["task"]
            if "done" in data:
                todo["done"] = data["done"]
            return jsonify(todo)
    return jsonify({"error": "Not found"}), 404

# DELETE a todo
@app.route("/todos/<int:id>", methods=["DELETE"])
def delete_todo(id):
    for todo in todos:
        if todo["id"] == id:
            todos.remove(todo)
            return jsonify({"message": "Deleted"})
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)