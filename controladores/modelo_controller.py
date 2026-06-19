from flask import Blueprint, render_template

from services.modelo_service import (
    obtener_metricas_modelo
)

modelo_bp = Blueprint(
    "modelo",
    __name__
)

@modelo_bp.route("/rendimiento")
def rendimiento():

    metricas = obtener_metricas_modelo()

    return render_template(
        "rendimiento.html",
        metricas=metricas,
        active_page="rendimiento"
    )
    
@modelo_bp.route("/reentrenamiento")
def reentrenamiento():

    return render_template(
        "reentrenamiento.html",
        active_page="reentrenamiento"
    )