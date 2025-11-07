from database import getConnection, releaseConnection
import json

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

def generarLecturas(limit=None, batch_size=10000):

    conn = getConnection()
    if conn is None:
        return

    try:
        cursor = conn.cursor(name="lecturas_cursor")
        query = "SELECT * FROM vista_lecturas_completas ORDER BY timestamp DESC"
        if limit:
            query += f" LIMIT {limit}"
        cursor.execute(query)

        yield "["
        first = True
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            for row in batch:
                item = {
                    "lecturaId": row[0],
                    "valor": row[1],
                    "timestamp": row[2].isoformat(),
                    "sensorNombre": row[3],
                    "tipoSensor": row[4],
                    "unidadMedicion": row[5],
                    "estacionNombre": row[6],
                    "estacionUbicacion": row[7]
                }
                if not first:
                    yield ","
                else:
                    first = False
                yield json.dumps(item)
        yield "]"
    finally:
        cursor.close()
        releaseConnection(conn)