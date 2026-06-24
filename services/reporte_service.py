from bd import obtenerconexion

def obtener_resumen():
    
    connection = obtenerconexion()

    with connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT COUNT(*)
                AS total_analisis
                FROM analisis
            """)
            total_analisis = cursor.fetchone()["total_analisis"]

            cursor.execute("""
                SELECT COUNT(*)
                AS total_anomalias
                FROM resultado_prediccion
                WHERE estado='ANOMALO'
            """)
            total_anomalias = cursor.fetchone()["total_anomalias"]

            cursor.execute("""
                SELECT COUNT(*)
                AS total_normales
                FROM resultado_prediccion
                WHERE estado='NORMAL'
            """)
            total_normales = cursor.fetchone()["total_normales"]

            cursor.execute("""
                SELECT ROUND(AVG(probabilidad),2)
                AS promedio
                FROM resultado_prediccion
            """)
            promedio = cursor.fetchone()["promedio"] or 0

    return {
        "total_analisis": total_analisis,
        "total_anomalias": total_anomalias,
        "total_normales": total_normales,
        "promedio_riesgo": promedio
    }
    
def obtener_alertas_prioridad():

    connection = obtenerconexion()

    with connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT
                    prioridad,
                    COUNT(*) AS cantidad
                FROM alerta
                GROUP BY prioridad
            """)

            return cursor.fetchall()

def obtener_patrones():

    connection = obtenerconexion()

    with connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT
                    patron,
                    COUNT(*) cantidad
                FROM resultado_prediccion
                WHERE patron IS NOT NULL
                AND patron <> ''
                GROUP BY patron
                ORDER BY cantidad DESC
            """)

            return cursor.fetchall()
        
def obtener_top_riesgo():

    connection = obtenerconexion()

    with connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT
                    cons_no,
                    MAX(probabilidad) AS probabilidad,
                    'ANOMALO' AS estado
                FROM resultado_prediccion
                GROUP BY cons_no
                ORDER BY probabilidad DESC
                LIMIT 10
            """)

            return cursor.fetchall()
        
