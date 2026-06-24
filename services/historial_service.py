from bd import obtenerconexion


def listar_analisis():

    connection = obtenerconexion()

    with connection:

        with connection.cursor() as cursor:

            sql = """
                SELECT
                    idanalisis,
                    nombre_archivo,
                    total_registros,
                    total_anomalias,
                    porcentaje_anomalias,
                    fecha_proceso
                FROM analisis
                ORDER BY fecha_proceso DESC
            """

            cursor.execute(sql)

            datos = cursor.fetchall()

    return datos


def obtener_analisis_por_id(idanalisis):

    connection = obtenerconexion()

    with connection:

        with connection.cursor() as cursor:

            sql = """
                SELECT *
                FROM analisis
                WHERE idanalisis = %s
            """

            cursor.execute(sql, (idanalisis,))

            dato = cursor.fetchone()

    return dato


def obtener_resultados_por_analisis(idanalisis):

    connection = obtenerconexion()

    with connection:

        with connection.cursor() as cursor:

            sql = """
                SELECT
                    cons_no,
                    probabilidad,
                    estado,
                    patron,
                    consumo_promedio,
                    consumo_ratio,
                    consumo_desviacion,
                    fecha_registro
                FROM resultado_prediccion
                WHERE idanalisis = %s
                ORDER BY probabilidad DESC
            """

            cursor.execute(sql, (idanalisis,))

            datos = cursor.fetchall()

    return datos

# REGISTRAR ANÁLISIS ===============================================

def registrar_analisis(
    idusuario,
    nombre_archivo,
    total_registros,
    total_anomalias,
    porcentaje_anomalias
):

    connection = obtenerconexion()

    with connection:

        with connection.cursor() as cursor:

            sql = """
                INSERT INTO analisis(
                    idusuario,
                    nombre_archivo,
                    total_registros,
                    total_anomalias,
                    porcentaje_anomalias
                )
                VALUES(
                    %s,%s,%s,%s,%s
                )
            """

            cursor.execute(
                sql,
                (
                    idusuario,
                    nombre_archivo,
                    total_registros,
                    total_anomalias,
                    porcentaje_anomalias
                )
            )

            connection.commit()

            return cursor.lastrowid
        
# REGISTRAR RESULTADO ===============================================

def registrar_resultado(
    idanalisis,
    cons_no,
    probabilidad,
    estado,
    patron,
    consumo_promedio,
    consumo_ratio,
    consumo_desviacion
):

    connection = obtenerconexion()

    with connection:

        with connection.cursor() as cursor:

            sql = """
                INSERT INTO resultado_prediccion(
                    idanalisis,
                    cons_no,
                    probabilidad,
                    estado,
                    patron,
                    consumo_promedio,
                    consumo_ratio,
                    consumo_desviacion
                )
                VALUES(
                    %s,%s,%s,%s,%s,%s,%s,%s
                )
            """

            cursor.execute(
                sql,
                (
                    idanalisis,
                    cons_no,
                    probabilidad,
                    estado,
                    patron,
                    consumo_promedio,
                    consumo_ratio,
                    consumo_desviacion
                )
            )

            connection.commit()
            return cursor.lastrowid