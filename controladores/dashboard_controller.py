from flask import Blueprint, render_template

from services.dashboard_service import (
    obtener_resumen_dashboard,
    obtener_alertas_dashboard,
    obtener_ultimos_analisis
)

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/home")
def dashboard():

    resumen = obtener_resumen_dashboard()

    alertas = obtener_alertas_dashboard()

    alta = 0
    media = 0
    baja = 0

    for alerta in alertas:

        prioridad = alerta["prioridad"]

        if prioridad == "ALTA":
            alta = alerta["cantidad"]

        elif prioridad == "MEDIA":
            media = alerta["cantidad"]

        elif prioridad == "BAJA":
            baja = alerta["cantidad"]

    ultimos = obtener_ultimos_analisis()

    return render_template(
        "dashboard.html",

        active_page="dashboard",

        total_analisis=resumen["total_analisis"],
        total_anomalias=resumen["total_anomalias"],
        total_normales=resumen["total_normales"],
        promedio_riesgo=resumen["promedio_riesgo"],

        alertas_alta=alta,
        alertas_media=media,
        alertas_baja=baja,

        ultimos_analisis=ultimos
    )