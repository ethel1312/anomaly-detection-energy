from flask import Blueprint, render_template, request
import os

from services.prediccion_service import procesar_archivo
from services.historial_service import (
    registrar_analisis,
    registrar_resultado
)
from services.alerta_service import (
    registrar_alerta,
    existe_alerta_pendiente
)

prediccion_bp = Blueprint(
    "prediccion",
    __name__
)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@prediccion_bp.route("/cargar", methods=["GET", "POST"])
def cargar_archivo():

    if request.method == "POST":

        archivo = request.files.get("archivo")

        if not archivo:
            return render_template(
                "cargar_archivo.html",
                error="Debe seleccionar un archivo",
                active_page="cargar_archivo"
            )

        ruta = os.path.join(
            UPLOAD_FOLDER,
            archivo.filename
        )

        archivo.save(ruta)

        resultado = procesar_archivo(ruta)

        if "error" in resultado:
            return render_template(
                "cargar_archivo.html",
                error=resultado["error"]
            )
            
        # RESULTADOS

        datos = resultado["data"]

        total = len(datos)

        anomalos = len(
            [r for r in datos
            if r["estado"] == "ANOMALO"]
        )

        normales = total - anomalos

        promedio = round(
            sum(r["probabilidad"] for r in datos)
            / total,
            2
        )
        
        porcentaje_anomalias = round(
            (anomalos / total) * 100,
            2
        )

        # Registrar el análisis
        idanalisis = registrar_analisis(
            idusuario=1,  # Reemplazar con el ID del usuario autenticado
            nombre_archivo=archivo.filename,
            total_registros=total,
            total_anomalias=anomalos,
            porcentaje_anomalias=porcentaje_anomalias
        )

        # Registrar los resultados
        for fila in datos:
            idresultado = registrar_resultado(
                idanalisis=idanalisis,
                cons_no=fila["cons_no"],
                probabilidad=fila["probabilidad"],
                estado=fila["estado"],
                patron=fila["patron"],
                consumo_promedio=fila["consumo_promedio"],
                consumo_ratio=fila["consumo_ratio"],
                consumo_desviacion=fila["consumo_desviacion"]
            )
            
            # Generar alerta solamente si es ANÓMALO

            if fila["estado"] == "ANOMALO":
                
                if existe_alerta_pendiente(
                        fila["cons_no"]
                    ):
                    
                    continue  # Ya existe una alerta pendiente para este cons_no

                if fila["probabilidad"] >= 95:

                    prioridad = "ALTA"

                elif fila["probabilidad"] >= 80:

                    prioridad = "MEDIA"

                else:

                    continue  # No generar alerta para probabilidades menores a 80%

                registrar_alerta(
                    idresultado=idresultado,
                    prioridad=prioridad,
                    descripcion="Consumo anómalo detectado por el modelo predictivo"
                )
        

        return render_template(
            "resultados.html",
            resultados=datos,
            total=total,
            anomalos=anomalos,
            normales=normales,
            promedio=promedio,
            active_page="resultados"
        )

    return render_template("cargar_archivo.html", active_page="cargar_archivo")

