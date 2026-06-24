from flask import Flask, redirect, url_for, render_template, request
from flask_jwt_extended import JWTManager
from controladores.auth_controller import auth_bp
from controladores.prediccion_controller import prediccion_bp
from controladores.historial_controller import historial_bp
from controladores.modelo_controller import modelo_bp
from controladores.alerta_controller import alerta_bp
from controladores.reporte_controller import reporte_bp
from controladores.dashboard_controller import dashboard_bp
import pandas as pd
import joblib
import os

#### SEGURIDAD - INICIO ####

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-cambia-esto"
jwt = JWTManager(app)


app.register_blueprint(auth_bp)
app.register_blueprint(prediccion_bp)
app.register_blueprint(historial_bp)
app.register_blueprint(modelo_bp)
app.register_blueprint(alerta_bp)
app.register_blueprint(reporte_bp)
app.register_blueprint(dashboard_bp)

# Cargar modelo y columnas
RUTA_MODELO = os.path.join("modelos", "modelo_xgboost.pkl")
RUTA_COLUMNAS = os.path.join("modelos", "columnas_modelo.pkl")

# Página principal
@app.route('/')
def home():
    return redirect(url_for('auth.login'))
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
