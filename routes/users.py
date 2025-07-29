from flask import Blueprint, request, jsonify
from firebase_config import db
from utils.user_validator import UserValidator
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

users_bp = Blueprint("users", __name__)
validator = UserValidator(db)

# Obtener todos los usuarios
@users_bp.route("/", methods=["GET"])
@jwt_required()
def get_users():
    users_ref = db.collection("user")
    docs = users_ref.stream()
    users = [{**doc.to_dict(), "id": doc.id} for doc in docs]
    return jsonify(users)


# Registro de usuario
@users_bp.route("/", methods=["POST"])
def add_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    if not validator.is_valid_email(email):
        return jsonify({"error": "Invalid email format"}), 400
    
    if not validator.is_strong_password(password):
        return jsonify({"error": "Password too weak"}), 400
    
    if validator.is_email_registered(email):
        return jsonify({"error": "Email already registered"}), 409

    doc_ref = db.collection("user").add(data)
    return jsonify({"message": "User added", "id": doc_ref[1].id}), 201


# Eliminar usuario
@users_bp.route("/<user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    try:
        db.collection("user").document(user_id).delete()
        return jsonify({"message": "User deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Actualizar usuario
@users_bp.route("/<user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
    data = request.get_json()
    try:
        db.collection("user").document(user_id).update(data)
        return jsonify({"message": "User updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Login con generación de token
@users_bp.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    try:
        users = db.collection("user").where("email", "==", email).stream()
        user = next(users, None)

        if user is None:
            return jsonify({"error": "User not found"}), 404

        user_data = user.to_dict()
        if user_data["password"] != password:
            return jsonify({"error": "Invalid password"}), 401

        # Crear token usando el ID como identidad
        access_token = create_access_token(identity=user.id)

        # No enviar la contraseña
        user_data.pop("password", None)

        return jsonify({
            "access_token": access_token,
            "user": {**user_data, "id": user.id}
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Obtener datos del usuario logueado
@users_bp.route("/me", methods=["GET"])
@jwt_required()
def get_logged_user():
    user_id = get_jwt_identity()
    try:
        user_doc = db.collection("user").document(user_id).get()
        if not user_doc.exists:
            return jsonify({"error": "User not found"}), 404
        user_data = user_doc.to_dict()
        user_data.pop("password", None)
        return jsonify({**user_data, "id": user_doc.id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
