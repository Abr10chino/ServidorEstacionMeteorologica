from fastapi import APIRouter
from crud import obtenerLecturas

router = APIRouter()

@router.get("/lecturas")
def getLecturas(limit: int = 10):
    data = obtenerLecturas(limit)

    return [
        {
            "lecturaId": row[0],
            "valor": row[1],
            "timestamp": row[2],
            "sensorNombre": row[3],
            "tipoSensor": row[4],
            "unidadMedicion": row[5],
            "estacionNombre": row[6],
            "estacionUbicacion": row[7]
        } for row in data
    ]