from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from services.auth_service import (
    registrar_usuario,
    validar_login,
    obtener_usuario_por_id,
    cambiar_password
)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login")
def login():
    return render_template("login.html")


@auth_bp.route("/home")
def home():
    return render_template("home.html")


@auth_bp.route("/api")
def api_inicio():
    return jsonify({
        "message": "API funcionando"
    })


@auth_bp.route("/api/register", methods=["POST"])
def api_register():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": 0,
                "message": "No se enviaron datos"
            }), 400

        nombre = data.get("nombre")
        correo = data.get("correo")
        password = data.get("password")

        if not nombre or not correo or not password:
            return jsonify({
                "status": 0,
                "message": "Faltan datos obligatorios"
            }), 400

        resultado, error = registrar_usuario(nombre, correo, password)

        if error:
            return jsonify({
                "status": 0,
                "message": error
            }), 409

        return jsonify({
            "status": 1,
            "message": "Usuario registrado correctamente"
        }), 201

    except Exception as e:
        return jsonify({
            "status": 0,
            "message": f"Error al registrar usuario: {str(e)}"
        }), 500


@auth_bp.route("/api/login", methods=["POST"])
def api_login():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": 0,
                "message": "No se enviaron datos"
            }), 400

        correo = data.get("correo")
        password = data.get("password")

        if not correo or not password:
            return jsonify({
                "status": 0,
                "message": "Debes enviar correo y password"
            }), 400

        usuario, error = validar_login(correo, password)

        if error:
            return jsonify({
                "status": 0,
                "message": error
            }), 401

        token = create_access_token(
            identity=str(usuario.idusuario),
            additional_claims={
                "nombre": usuario.nombre,
                "correo": usuario.correo
            }
        )

        return jsonify({
            "status": 1,
            "message": "Login correcto",
            "access_token": token,
            "user": {
                "idusuario": usuario.idusuario,
                "nombre": usuario.nombre,
                "correo": usuario.correo
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": 0,
            "message": f"Error en login: {str(e)}"
        }), 500

@auth_bp.route("/api/cambiar-password", methods=["POST"])
def api_cambiar_password():
    try:
        data = request.get_json()

        correo = data.get("correo")
        password_actual = data.get("password_actual")
        password_nueva = data.get("password_nueva")

        if not correo or not password_actual or not password_nueva:
            return jsonify({
                "status": 0,
                "message": "Faltan datos"
            }), 400

        error = cambiar_password(correo, password_actual, password_nueva)

        if error:
            return jsonify({
                "status": 0,
                "message": error
            }), 400

        return jsonify({
            "status": 1,
            "message": "Contraseña actualizada correctamente"
        })

    except Exception as e:
        return jsonify({
            "status": 0,
            "message": str(e)
        }), 500

@auth_bp.route("/api/perfil", methods=["GET"])
@jwt_required()
def api_perfil():
    try:
        idusuario = get_jwt_identity()
        usuario = obtener_usuario_por_id(idusuario)

        if not usuario:
            return jsonify({
                "status": 0,
                "message": "Usuario no encontrado"
            }), 404

        return jsonify({
            "status": 1,
            "data": {
                "idusuario": usuario.idusuario,
                "nombre": usuario.nombre,
                "correo": usuario.correo,
                "estado": usuario.estado
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": 0,
            "message": f"Error al obtener perfil: {str(e)}"
        }), 500
        
        
