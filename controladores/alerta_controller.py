from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect

from services.alerta_service import (
    obtener_alertas,
    obtener_alerta_por_id,
    actualizar_alerta
)

alerta_bp = Blueprint(
    "alerta",
    __name__
)


@alerta_bp.route("/alertas")
def alertas():

    alertas = obtener_alertas()

    return render_template(
        "alertas.html",
        alertas=alertas,
        active_page="alertas"
    )
    
@alerta_bp.route(
    "/alertas/revisar/<int:idalerta>",
    methods=["GET", "POST"]
)
def revisar_alerta(idalerta):

    if request.method == "POST":

        resultado_revision = request.form.get(
            "resultado_revision"
        )

        actualizar_alerta(
            idalerta,
            resultado_revision
        )

        return redirect("/alertas")

    alerta = obtener_alerta_por_id(
        idalerta
    )

    return render_template(
        "revisar_alerta.html",
        alerta=alerta,
        active_page="alertas"
    )
    
@alerta_bp.route(
    "/alertas/ver/<int:idalerta>"
)
def ver_alerta(idalerta):

    alerta = obtener_alerta_por_id(
        idalerta
    )

    return render_template(
        "ver_alerta.html",
        alerta=alerta,
        active_page="alertas"
    )