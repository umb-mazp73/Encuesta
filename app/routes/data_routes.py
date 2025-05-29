from fastapi import APIRouter, Header
from app.models.data import useData
from app.core.config import settings
import httpx
import json

router = APIRouter()

@router.post("/data_send")
async def receive_data(
    data: useData,
    authorization: str = Header(default=None)
):
    json_data = data.dict()
    print("Datos recibidos:\n" + json.dumps(json_data, indent=4))
    print(f"Authorization header: {authorization}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(settings.FORWARD_URL, json=json_data)
        return {
            "message": "Datos de la encuesta recibidos y reenviados correctamente",
            "forwarded_response": response.json(),
            "calculo":response
        }
    except httpx.RequestError as exc:
        return {
            "message": "Error al reenviar los datos",
            "error": str(exc)
        }
