from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from crud import generarLecturas

router = APIRouter()

@router.get("/lecturas")
def getLecturas(limit: int = None):
    return StreamingResponse(generarLecturas(limit), media_type="application/json")