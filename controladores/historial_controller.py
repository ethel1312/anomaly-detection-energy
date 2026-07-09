from flask import Blueprint, render_template, request
from services.historial_service import (
    listar_analisis,
    contar_analisis,
    obtener_promedio_probabilidad,
    obtener_analisis_por_id,
    obtener_resultados_por_analisis,
    contar_resultados_por_analisis
)

historial_bp = Blueprint(
    "historial",
    __name__
)

@historial_bp.route("/historial")
def historial():

    buscar = request.args.get(
        "buscar",
        ""
    )

    fecha = request.args.get(
        "fecha",
        ""
    )

    pagina = int(
        request.args.get(
            "pagina",
            1
        )
    )

    registros_por_pagina = 8

    offset = (
        pagina - 1
    ) * registros_por_pagina

    total_registros = contar_analisis(
        buscar,
        fecha
    )
    

    total_paginas = (
        total_registros + registros_por_pagina - 1
    ) // registros_por_pagina

    analisis = listar_analisis(
        buscar,
        fecha,
        registros_por_pagina,
        offset
    )

    return render_template(
        "historial.html",

        analisis=analisis,

        buscar=buscar,
        fecha=fecha,

        pagina=pagina,
        total_paginas=total_paginas,

        total_registros=total_registros,
        registros_por_pagina=registros_por_pagina,

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
        
    pagina = int(
        request.args.get(
            "pagina",
            1
        )
    )

    registros_por_pagina = 8

    offset = (
        pagina - 1
    ) * registros_por_pagina

    resultados = obtener_resultados_por_analisis(
        idanalisis,
        registros_por_pagina,
        offset
    )
    
    total_registros = contar_resultados_por_analisis(
        idanalisis
    )
    
    total_paginas = (
        total_registros +
        registros_por_pagina - 1
    ) // registros_por_pagina

    total = analisis["total_registros"]

    anomalos = analisis["total_anomalias"]

    normales = total - anomalos

    promedio = obtener_promedio_probabilidad(
        idanalisis
    )

    return render_template(
        "resultados.html",
        analisis=analisis, 
        resultados=resultados,
        total=total,
        anomalos=anomalos,
        normales=normales,
        promedio=promedio,
        
        pagina=pagina,
        total_paginas=total_paginas,
        total_registros=total_registros,
        registros_por_pagina=registros_por_pagina,
        active_page="historial"
    )