import hashlib
from bd import obtenerconexion
from models.usuario import Usuario


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def obtener_usuario_por_correo(correo):
    connection = obtenerconexion()

    with connection:
        with connection.cursor() as cursor:
            sql = """
                SELECT idusuario, nombre, correo, password, estado
                FROM usuario
                WHERE correo = %s
            """
            cursor.execute(sql, (correo,))
            row = cursor.fetchone()

    if row:
        return Usuario(
            row["idusuario"],
            row["nombre"],
            row["correo"],
            row["password"],
            row["estado"]
        )

    return None


def obtener_usuario_por_id(idusuario):
    connection = obtenerconexion()

    with connection:
        with connection.cursor() as cursor:
            sql = """
                SELECT idusuario, nombre, correo, password, estado
                FROM usuario
                WHERE idusuario = %s
            """
            cursor.execute(sql, (idusuario,))
            row = cursor.fetchone()

    if row:
        return Usuario(
            row["idusuario"],
            row["nombre"],
            row["correo"],
            row["password"],
            row["estado"]
        )

    return None


def registrar_usuario(nombre, correo, password):
    usuario_existente = obtener_usuario_por_correo(correo)

    if usuario_existente:
        return None, "El usuario ya existe"

    password_hash = hash_password(password)

    connection = obtenerconexion()

    with connection:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO usuario (nombre, correo, password, estado)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (nombre, correo, password_hash, 1))
            connection.commit()

    return True, None


def validar_login(correo, password):
    usuario = obtener_usuario_por_correo(correo)

    if not usuario:
        return None, "Usuario no encontrado"

    if usuario.estado != 1:
        return None, "Usuario inactivo"

    password_hash = hash_password(password)

    if usuario.password != password_hash:
        return None, "Credenciales incorrectas"

    return usuario, None

def cambiar_password(correo, password_actual, password_nueva):
    usuario = obtener_usuario_por_correo(correo)

    if not usuario:
        return "Usuario no encontrado"

    if usuario.password != hash_password(password_actual):
        return "Contraseña actual incorrecta"

    nueva_hash = hash_password(password_nueva)

    connection = obtenerconexion()

    with connection:
        with connection.cursor() as cursor:
            sql = """
                UPDATE usuario
                SET password = %s
                WHERE correo = %s
            """
            cursor.execute(sql, (nueva_hash, correo))
            connection.commit()

    return None