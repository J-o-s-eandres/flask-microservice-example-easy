from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid 

# Crear la base de datos antes de definir la aplicación Flask
db = SQLAlchemy()

# Definir el modelo de datos
class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

# Luego, definir la aplicación Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Asociar la aplicación Flask con la base de datos
db.init_app(app)

# Crear todas las tablas en la base de datos
with app.app_context():
    db.create_all()

# Definir las rutas después de la creación de la base de datos
@app.route('/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])
    elif request.method == 'POST':
        new_user = request.json
        user = User(username=new_user['username'], email=new_user['email'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email}), 201
    elif request.method == 'PUT':
        updated_user = request.json
        user = User.query.get(updated_user['id'])
        if user:
            user.username = updated_user['username']
            user.email = updated_user['email']
            db.session.commit()
            return jsonify({'id': user.id, 'username': user.username, 'email': user.email})
        return jsonify({'error': 'User not found'}), 404
    elif request.method == 'DELETE':
        user_to_delete = request.json
        user = User.query.get(user_to_delete['id'])
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'id': user.id, 'username': user.username, 'email': user.email})
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(port=5001, debug=True)
