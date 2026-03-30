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

    todo = {
        "id": len(todos) + 1,
        "task": task,
        "done": False
    }
    todos.append(todo)
    return jsonify(todo), 201

# PUT – mark todo as done
@app.route("/todos/<int:id>", methods=["PUT"])
def update_todo(id):
    data = request.get_json()
    for todo in todos:
        if todo["id"] == id:
            todo["done"] = data.get("done", todo["done"])
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