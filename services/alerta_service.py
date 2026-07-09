from bd import obtenerconexion


def obtener_alertas(
    prioridad="",
    estado="",
    limite=10,
    offset=0
):

    conexion = obtenerconexion()

    with conexion:
        with conexion.cursor() as cursor:

            sql = """
            SELECT
                a.idalerta,
                a.prioridad,
                a.estado,
                a.fecha_alerta,
                r.probabilidad,
                r.cons_no
            FROM alerta a
            INNER JOIN resultado_prediccion r
                ON a.idresultado = r.idresultado
            WHERE 1=1
            """

            parametros = []

            if prioridad:

                sql += """
                AND a.prioridad = %s
                """

                parametros.append(prioridad)

            if estado:

                sql += """
                AND a.estado = %s
                """

                parametros.append(estado)

            sql += """
            ORDER BY a.fecha_alerta DESC
            LIMIT %s
            OFFSET %s
            """

            parametros.append(limite)
            parametros.append(offset)

            cursor.execute(
                sql,
                parametros
            )

            return cursor.fetchall()
        
def contar_alertas(
    prioridad="",
    estado=""
):

    conexion = obtenerconexion()

    with conexion:
        with conexion.cursor() as cursor:

            sql = """
            SELECT COUNT(*) AS total
            FROM alerta
            WHERE 1=1
            """

            parametros=[]

            if prioridad:

                sql += """
                AND prioridad=%s
                """

                parametros.append(prioridad)

            if estado:

                sql += """
                AND estado=%s
                """

                parametros.append(estado)

            cursor.execute(
                sql,
                parametros
            )

            return cursor.fetchone()["total"]

def obtener_alerta_por_id(idalerta):

    connection = obtenerconexion()

    with connection:

        with connection.cursor() as cursor:

            sql = """
            SELECT
                a.*,
                r.cons_no,
                r.probabilidad,
                r.patron,
                r.consumo_promedio,
                r.consumo_ratio,
                r.consumo_desviacion
            FROM alerta a
            INNER JOIN resultado_prediccion r
                ON a.idresultado = r.idresultado
            WHERE a.idalerta = %s
            """

            cursor.execute(
                sql,
                (idalerta,)
            )

            return cursor.fetchone()

def registrar_alerta(
    idresultado,
    prioridad,
    descripcion
):

    connection = obtenerconexion()

    with connection:

        with connection.cursor() as cursor:

            sql = """
                INSERT INTO alerta(
                    idresultado,
                    prioridad,
                    descripcion
                )
                VALUES(
                    %s,%s,%s
                )
            """

            cursor.execute(
                sql,
                (
                    idresultado,
                    prioridad,
                    descripcion
                )
            )

            connection.commit()
            
def existe_alerta_pendiente(cons_no):

    connection = obtenerconexion()

    with connection:

        with connection.cursor() as cursor:

            sql = """
            SELECT COUNT(*) AS total
            FROM alerta a
            INNER JOIN resultado_prediccion r
                ON a.idresultado = r.idresultado
            WHERE r.cons_no = %s
            AND a.estado = 'PENDIENTE'
            """

            cursor.execute(
                sql,
                (cons_no,)
            )

            row = cursor.fetchone()

    return row["total"] > 0

def actualizar_alerta(
    idalerta,
    resultado_revision
):

    connection = obtenerconexion()

    with connection:

        with connection.cursor() as cursor:

            sql = """
            UPDATE alerta
            SET
                estado='REVISADA',
                resultado_revision=%s
            WHERE idalerta=%s
            """

            cursor.execute(
                sql,
                (
                    resultado_revision,
                    idalerta
                )
            )

            connection.commit()
            
def contar_alertas_pendientes(
    prioridad=""
):

    conexion = obtenerconexion()

    with conexion:
        with conexion.cursor() as cursor:

            sql = """
                SELECT COUNT(*) AS total
                FROM alerta
                WHERE estado='PENDIENTE'
            """

            parametros = []

            if prioridad:

                sql += """
                AND prioridad=%s
                """

                parametros.append(prioridad)

            cursor.execute(
                sql,
                parametros
            )

            return cursor.fetchone()["total"]
