from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from app.models.user_model import User

user_bp = Blueprint("user", __name__)


@user_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")
    role = data.get("role")

    if not name or not password or not email or not phone:
        return jsonify({"error": "Se requieren datos de usuario"}), 400

    existing_user = User.find_by_username(name)
    if existing_user:
        return jsonify({"error": "El nombre de usuario ya está en uso"}), 400

    new_user = User(name, email, password, phone, role)
    new_user.save()

    return jsonify({"message": "Usuario creado exitosamente"}), 201


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    name = data.get("name")
    password = data.get("password")

    user = User.find_by_username(name)
    if user and check_password_hash(user.password_hash, password):
        # Si las credenciales son válidas, genera un token JWT
        access_token = create_access_token(
            identity={"name": name, "role": user.role}
        )
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401