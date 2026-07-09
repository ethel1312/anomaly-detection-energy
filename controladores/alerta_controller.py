from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect

from services.alerta_service import (
    obtener_alertas,
    contar_alertas,
    contar_alertas_pendientes,
    obtener_alerta_por_id,
    actualizar_alerta
)

alerta_bp = Blueprint(
    "alerta",
    __name__
)

@alerta_bp.route("/alertas")
def alertas():

    pagina = int(
        request.args.get(
            "pagina",
            1
        )
    )
    
    prioridad = request.args.get(
        "prioridad",
        ""
    )

    estado = request.args.get(
        "estado",
        ""
    )

    registros_por_pagina = 8

    offset = (
        pagina - 1
    ) * registros_por_pagina

    total_registros = contar_alertas(
        prioridad,
        estado
    )
    
    pendientes = contar_alertas_pendientes(
        prioridad
    )

    revisadas = (
        total_registros -
        pendientes
    )

    total_paginas = (
        total_registros + registros_por_pagina - 1
    ) // registros_por_pagina

    alertas = obtener_alertas(
        prioridad,
        estado,
        registros_por_pagina,
        offset
    )

    return render_template(
        "alertas.html",

        alertas=alertas,

        pagina=pagina,
        total_paginas=total_paginas,

        total_registros=total_registros,
        registros_por_pagina=registros_por_pagina,
        
        prioridad=prioridad,
        estado=estado,
        
        pendientes=pendientes,
        revisadas=revisadas,

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