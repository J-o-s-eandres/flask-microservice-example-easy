from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Conectar a la base de datos MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['todo_db']
tasks_collection = db['tasks']

@app.route('/tasks', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_tasks():
    if request.method == 'GET':
        tasks = list(tasks_collection.find({}, {'_id': False}))  # Obtener todas las tareas
        return jsonify(tasks), 200
    elif request.method == 'POST':
        new_task = request.json
        task_id = tasks_collection.insert_one(new_task).inserted_id
        new_task['_id'] = str(task_id)
        return jsonify(new_task), 201
    elif request.method == 'PUT':
        updated_task = request.json
        task_id = updated_task.get('id')
        if task_id:
            result = tasks_collection.update_one({'_id': task_id}, {'$set': updated_task})
            if result.modified_count == 1:
                updated_task['_id'] = task_id
                return jsonify(updated_task), 200
            else:
                return jsonify({'error': 'Task not found'}), 404
        else:
            return jsonify({'error': 'Missing task id'}), 400
    elif request.method == 'DELETE':
        task_id = request.json.get('id')
        if task_id:
            result = tasks_collection.delete_one({'_id': task_id})
            if result.deleted_count == 1:
                return jsonify({'id': task_id}), 200
            else:
                return jsonify({'error': 'Task not found'}), 404
        else:
            return jsonify({'error': 'Missing task id'}), 400

if __name__ == '__main__':
    app.run(port=5002, debug=True)



