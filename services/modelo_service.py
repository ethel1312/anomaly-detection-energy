import json

def obtener_metricas_modelo():

    with open(
        "modelos/metricas_modelo.json",
        "r",
        encoding="utf-8"
    ) as archivo:

        return json.load(archivo)