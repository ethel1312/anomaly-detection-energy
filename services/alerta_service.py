from bd import obtenerconexion


def obtener_alertas():

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
            ORDER BY a.fecha_alerta DESC
            """

            cursor.execute(sql)

            alertas = cursor.fetchall()

    return alertas

def obtener_alerta_por_id(idalerta):

    connection = obtenerconexion()

    with connection:

        with connection.cursor() as cursor:

            sql = """
            SELECT
                a.*,
                r.cons_no,
                r.probabilidad
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
            SELECT COUNT(*)
            FROM alerta a
            INNER JOIN resultado_prediccion r
                ON a.idresultado = r.idresultado
            WHERE r.cons_no = %s
            AND a.estado = 'PENDIENTE'
            """

            cursor.execute(sql, (cons_no,))

            total = cursor.fetchone()[0]

    return total > 0

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
