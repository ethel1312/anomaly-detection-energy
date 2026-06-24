from flask import Blueprint, render_template

from services.reporte_service import (
    obtener_resumen,
    obtener_alertas_prioridad,
    obtener_patrones,
    obtener_top_riesgo
)

reporte_bp = Blueprint(
    "reporte",
    __name__
)


@reporte_bp.route("/reportes")
def reportes():

    resumen = obtener_resumen()

    prioridades = obtener_alertas_prioridad()

    patrones = obtener_patrones()

    top_riesgo = obtener_top_riesgo()

    alertas_alta = 0
    alertas_media = 0
    alertas_baja = 0

    for item in prioridades:

        if item["prioridad"] == "ALTA":

            alertas_alta = item["cantidad"]

        elif item["prioridad"] == "MEDIA":

            alertas_media = item["cantidad"]

        elif item["prioridad"] == "BAJA":

            alertas_baja = item["cantidad"]

    return render_template(
        "reportes.html",

        total_analisis=resumen["total_analisis"],
        total_anomalias=resumen["total_anomalias"],
        total_normales=resumen["total_normales"],
        promedio_riesgo=resumen["promedio_riesgo"],

        alertas_alta=alertas_alta,
        alertas_media=alertas_media,
        alertas_baja=alertas_baja,

        patrones=patrones,
        top_riesgo=top_riesgo,

        active_page="reportes"
    )