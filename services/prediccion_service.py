import pandas as pd
from pandas.errors import EmptyDataError
import joblib

from services.preprocesamiento_service import generar_variables

modelo = joblib.load(
    "modelos/modelo_xgboost.pkl"
)

columnas_modelo = joblib.load(
    "modelos/columnas_modelo.pkl"
)

if "Unnamed: 0" in columnas_modelo:
    columnas_modelo.remove("Unnamed: 0")

def procesar_archivo(ruta_csv):

    try:

        # Leer CSV
        df = pd.read_csv(ruta_csv)
        
        # VALIDACIONES

        if df.empty:
            return {
                "error": "El archivo está vacío"
            }

        if "CONS_NO" not in df.columns:
            return {
                "error": "Falta la columna CONS_NO"
            }

        # Guardar CONS_NO
        cons_no = None

        if "CONS_NO" in df.columns:
            cons_no = df["CONS_NO"]

        # Generar variables derivadas
        df_features = generar_variables(df)

        # ==========================
        # PATRONES DE CONSUMO
        # ==========================

        patrones = []

        for i in range(len(df_features)):

            ratio = df_features.iloc[i]["consumo_ratio"]
            tendencia = df_features.iloc[i]["consumo_tendencia"]
            desviacion = df_features.iloc[i]["consumo_desviacion"]

            if ratio >= 2:

                patron = (
                    "Consumo significativamente superior "
                    "al promedio histórico"
                )

            elif desviacion >= 30:

                patron = (
                    "Alta variabilidad en el consumo"
                )

            elif tendencia >= 10:

                patron = (
                    "Incremento progresivo del consumo"
                )

            elif tendencia <= -10:

                patron = (
                    "Disminución abrupta del consumo"
                )

            else:

                patron = (
                    "Comportamiento atípico detectado"
                )

            patrones.append(patron)

        # Eliminar CONS_NO antes de predecir
        if "CONS_NO" in df_features.columns:

            df_modelo = df_features.drop(
                columns=["CONS_NO"]
            )

        else:

            df_modelo = df_features

        # Validar columnas
        faltantes = [
            col for col in columnas_modelo
            if col not in df_modelo.columns
        ]

        if faltantes:

            columnas = ", ".join(faltantes)

            return {
                "error":
                f"El archivo no tiene las columnas requeridas: {columnas}"
            }

        # Orden correcto
        X = df_modelo[columnas_modelo]

        # Predicción
        predicciones = modelo.predict(X)

        # Probabilidades
        probabilidades = modelo.predict_proba(X)

        # Resultado final
        resultado = pd.DataFrame()

        if cons_no is not None:

            resultado["cons_no"] = cons_no

        resultado["prediccion"] = predicciones

        resultado["probabilidad"] = (
            probabilidades.max(axis=1) * 100
        ).round(2)

        resultado["patron"] = patrones

        # Etiqueta visual
        resultado["estado"] = resultado[
            "prediccion"
        ].apply(
            lambda x: "ANOMALO"
            if x == 1
            else "NORMAL"
        )
        
        resultado["consumo_promedio"] = (
            df_features["consumo_promedio"]
        ).round(2)

        resultado["consumo_ratio"] = (
            df_features["consumo_ratio"]
        ).round(2)

        resultado["consumo_desviacion"] = (
            df_features["consumo_desviacion"]
        ).round(2)
        
        return {
            "data": resultado.to_dict(
                orient="records"
            )
        }

    except EmptyDataError:

        return {
            "error": "El archivo está vacío"
        }

    except Exception as e:

        return {
            "error": str(e)
        }
