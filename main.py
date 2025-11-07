from fastapi import FastAPI
from api import routes
from mqtt_client import startMqtt
import threading

app = FastAPI(title="Servidor IoT UMES", version="1.0.0")

threading.Thread(target=startMqtt, daemon=True).start()

app.include_router(routes.router)

@app.get("/")
def root():
    return {"message": "Servidor IoT UMES está en funcionamiento."}