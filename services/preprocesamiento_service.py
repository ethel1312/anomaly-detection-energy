import pandas as pd


def generar_variables(df):

    # Guardar identificador
    cons_no = None

    if "CONS_NO" in df.columns:
        cons_no = df["CONS_NO"]

    # Eliminar columnas que no usa el modelo
    columnas_eliminar = []

    if "CONS_NO" in df.columns:
        columnas_eliminar.append("CONS_NO")

    if "FLAG" in df.columns:
        columnas_eliminar.append("FLAG")

    X = df.drop(columns=columnas_eliminar)

    # ==========================
    # VARIABLES DERIVADAS
    # ==========================

    # Promedio histórico
    consumo_promedio = X.mean(axis=1)

    # Ratio
    consumo_ratio = (
        X.iloc[:, -1] /
        (consumo_promedio + 1e-5)
    )

    # Tendencia
    consumo_tendencia = (
        X.diff(axis=1).sum(axis=1)
    )

    # Máximo
    consumo_maximo = X.max(axis=1)

    # Mínimo
    consumo_minimo = X.min(axis=1)

    # Desviación estándar
    consumo_desviacion = X.std(axis=1)

    # Dataset final
    df_features = pd.concat([
        X,
        pd.DataFrame({
            'consumo_promedio': consumo_promedio,
            'consumo_ratio': consumo_ratio,
            'consumo_tendencia': consumo_tendencia,
            'consumo_maximo': consumo_maximo,
            'consumo_minimo': consumo_minimo,
            'consumo_desviacion': consumo_desviacion,
        })
    ], axis=1)

    # Volver a agregar identificador
    if cons_no is not None:
        df_features["CONS_NO"] = cons_no.values

    return df_features