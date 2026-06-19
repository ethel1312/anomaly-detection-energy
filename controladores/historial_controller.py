from flask import Blueprint, render_template
from services.historial_service import (
    listar_analisis,
    obtener_analisis_por_id,
    obtener_resultados_por_analisis
)

historial_bp = Blueprint(
    "historial",
    __name__
)

@historial_bp.route("/historial")
def historial():

    analisis = listar_analisis()

    return render_template(
        "historial.html",
        analisis=analisis,
        active_page="historial"
    )
    
    
@historial_bp.route("/historial/<int:idanalisis>")
def detalle_analisis(idanalisis):

    analisis = obtener_analisis_por_id(
        idanalisis
    )

    if not analisis:

        return render_template(
            "historial.html",
            error="Análisis no encontrado",
            active_page="historial"
        )

    resultados = obtener_resultados_por_analisis(
        idanalisis
    )

    total = analisis["total_registros"]

    anomalos = analisis["total_anomalias"]

    normales = total - anomalos

    promedio = 0

    if len(resultados) > 0:

        promedio = round(
            sum(
                r["probabilidad"]
                for r in resultados
            ) / len(resultados),
            2
        )

    return render_template(
        "resultados.html",
        resultados=resultados,
        total=total,
        anomalos=anomalos,
        normales=normales,
        promedio=promedio,
        active_page="historial"
    )