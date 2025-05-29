from fastapi import APIRouter, Header
from app.models.data import useData
from app.core.config import settings
import httpx
import json

router = APIRouter()

@router.post("/data_send")
async def receive_data(
    data: useData,
    authorization: str = Header(default="")
):
    json_data = data.dict()
    print("Datos recibidos:\n" + json.dumps(json_data, indent=4))
    print(f"Authorization header: {authorization}")

    bearer_token = f"Bearer {authorization}" if authorization else "Bearer "

    headers = {
        "Authorization": bearer_token
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(settings.FORWARD_URL, json=json_data, headers=headers)
            try:
                forwarded_response = response.json()
            except ValueError:
                forwarded_response = response.text

        return {
            "message": "Datos reenviados correctamente",
            "forwarded_response": forwarded_response,
            "status_code": response.status_code
        }

    except httpx.RequestError as exc:
        return {
            "message": "Error al reenviar los datos",
            "error": str(exc)
        }
