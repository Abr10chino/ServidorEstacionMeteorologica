from database import getConnection, releaseConnection

def insertarLecturas(datos):

    conn = getConnection()

    if conn is None:
        print(f"No se pudo obtener la conexión a la base de datos.")
        return False
    
    try:

        cursor = conn.cursor()
        timestamp = f"{datos['Fecha']} {datos['Hora']}"

        query = """
            INSERT INTO lectura (sensor_id, timestamp, valor, id_medicion_tipo_sensor, estacion_id)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (2, timestamp, datos["temperatura"], 1, datos["estacion"]))
        cursor.execute(query, (2, timestamp, datos["presion"], 3, datos["estacion"]))
        cursor.execute(query, (2, timestamp, datos["altitud"], 4, datos["estacion"]))
        cursor.execute(query, (3, timestamp, datos["calidadAire"], 6, datos["estacion"]))

        conn.commit()

        print("Lecturas insertadas correctamente.")
        return True

    except Exception as e:
        print(f"Error al insertar lecturas: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        releaseConnection(conn)

def obtenerLecturas(limit=10):

    conn = getConnection()

    if conn is None:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM vista_lecturas_completas
            ORDER BY timestamp DESC
            LIMIT %s;
        """, (limit,))
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print("❌ Error al obtener lecturas:", e)
        return []
    finally:
        cursor.close()
        releaseConnection(conn)