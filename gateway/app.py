from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Rutas para manejar las solicitudes de usuarios
@app.route('/api/v1/users', methods=['GET', 'POST', 'PUT'])
def handle_users():
    if request.method == 'GET':
        response = requests.get('http://localhost:5001/users')
        return jsonify(response.json())
    elif request.method == 'POST':
        response = requests.post('http://localhost:5001/users', json=request.json)
        return jsonify(response.json())
    elif request.method == 'PUT':
        response = requests.put('http://localhost:5001/users', json=request.json)
        return jsonify(response.json())

# Rutas para manejar las solicitudes de tareas
@app.route('/api/v1/tasks', methods=['GET', 'POST', 'PUT'])
def handle_tasks():
    if request.method == 'GET':
        response = requests.get('http://localhost:5002/tasks')
        return jsonify(response.json())
    elif request.method == 'POST':
        response = requests.post('http://localhost:5002/tasks', json=request.json)
        return jsonify(response.json())
    elif request.method == 'PUT':
        response = requests.put('http://localhost:5002/tasks', json=request.json)
        return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=5000, debug=True)
