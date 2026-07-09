from bd import obtenerconexion


def listar_analisis(
    buscar="",
    fecha="",
    limite=10,
    offset=0
):

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
                WHERE 1=1
            """

            parametros = []

            if buscar:

                sql += """
                    AND nombre_archivo LIKE %s
                """

                parametros.append(
                    f"%{buscar}%"
                )

            if fecha:

                sql += """
                    AND DATE(fecha_proceso) = %s
                """

                parametros.append(
                    fecha
                )

            sql += """
                ORDER BY fecha_proceso DESC
                LIMIT %s
                OFFSET %s
            """
            
            parametros.append(limite)
            parametros.append(offset)

            cursor.execute(
                sql,
                parametros
            )

            datos = cursor.fetchall()

    return datos

def contar_analisis(
    buscar="",
    fecha=""
):

    connection = obtenerconexion()

    with connection:

        with connection.cursor() as cursor:

            sql = """
                SELECT COUNT(*) AS total
                FROM analisis
                WHERE 1=1
            """

            parametros = []

            if buscar:

                sql += """
                    AND nombre_archivo LIKE %s
                """

                parametros.append(
                    f"%{buscar}%"
                )

            if fecha:

                sql += """
                    AND DATE(fecha_proceso)=%s
                """

                parametros.append(fecha)

            cursor.execute(
                sql,
                parametros
            )

            return cursor.fetchone()["total"]


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


def obtener_resultados_por_analisis(
    idanalisis,
    limite=10,
    offset=0
):

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
                WHERE idanalisis=%s
                ORDER BY probabilidad DESC
                LIMIT %s
                OFFSET %s
            """

            cursor.execute(
                sql,
                (
                    idanalisis,
                    limite,
                    offset
                )
            )

            datos = cursor.fetchall()

    return datos

def contar_resultados_por_analisis(
    idanalisis
):

    connection = obtenerconexion()

    with connection:

        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT COUNT(*) total
                FROM resultado_prediccion
                WHERE idanalisis=%s
                """,
                (idanalisis,)
            )

            return cursor.fetchone()["total"]
        
def obtener_promedio_probabilidad(idanalisis):

    connection = obtenerconexion()

    with connection:

        with connection.cursor() as cursor:

            sql = """
                SELECT AVG(probabilidad) AS promedio
                FROM resultado_prediccion
                WHERE idanalisis = %s
            """

            cursor.execute(
                sql,
                (idanalisis,)
            )

            dato = cursor.fetchone()

    return round(
        dato["promedio"] or 0,
        2
    )

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