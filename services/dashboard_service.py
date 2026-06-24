from bd import obtenerconexion


def obtener_resumen_dashboard():

    connection = obtenerconexion()

    with connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT COUNT(*) total
                FROM resultado_prediccion
            """)
            total = cursor.fetchone()["total"]

            cursor.execute("""
                SELECT COUNT(*) total
                FROM resultado_prediccion
                WHERE estado='ANOMALO'
            """)
            anomalos = cursor.fetchone()["total"]

            cursor.execute("""
                SELECT COUNT(*) total
                FROM resultado_prediccion
                WHERE estado='NORMAL'
            """)
            normales = cursor.fetchone()["total"]

            cursor.execute("""
                SELECT ROUND(AVG(probabilidad),2) promedio
                FROM resultado_prediccion
            """)
            promedio = cursor.fetchone()["promedio"] or 0

    return {
        "total_analisis": total,
        "total_anomalias": anomalos,
        "total_normales": normales,
        "promedio_riesgo": promedio
    }
    
def obtener_alertas_dashboard():

    connection = obtenerconexion()

    with connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT prioridad,
                       COUNT(*) cantidad
                FROM alerta
                GROUP BY prioridad
            """)

            return cursor.fetchall()
        
def obtener_ultimos_analisis():

    connection = obtenerconexion()

    with connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT
                    cons_no,
                    probabilidad,
                    estado
                FROM resultado_prediccion
                ORDER BY idresultado DESC
                LIMIT 10
            """)

            return cursor.fetchall()