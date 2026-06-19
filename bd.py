import pymysql

def obtenerconexion():
    return pymysql.connect(host='127.0.0.1',
                                user='root',
                                db='bd_anomaly',
                                cursorclass=pymysql.cursors.DictCursor)