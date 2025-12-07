from flask import Blueprint, request, jsonify
from ..models import User 

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"message": "Faltan datos (email y password son requeridos)"}), 400

    if User.objects(email=email).first():
        return jsonify({"message": "El usuario con ese email ya existe"}), 409

    try:
        new_user = User(email=email)
        new_user.set_password(password)
        new_user.role = 'cliente' 
        new_user.save()
        
        return jsonify({
            "message": "Usuario registrado exitosamente",
            "user": new_user.email,
            "role": new_user.role
        }), 201 

    except Exception as e:
        return jsonify({"message": f"Error al registrar usuario: {str(e)}"}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"message": "Email y password son requeridos"}), 400

    user = User.objects(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"message": "Credenciales inválidas"}), 401 
    
    return jsonify({
        "message": "Inicio de sesión exitoso",
        "user_id": str(user.id),
        "role": user.role,
        "email": user.email
    }), 200