from fastapi import APIRouter, Header
from app.models.data import useData
from app.core.config import settings
import httpx
import json
import jwt
from jwt import PyJWTError
from datetime import datetime, timezone

router = APIRouter()

def is_token_valid(token: str) -> bool:
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        exp = payload.get("exp")
        if exp is None:
            return False
        now = datetime.now(timezone.utc).timestamp()
        if now > exp:
            return False
        return True
    except PyJWTError:
        return False

@router.post("/data_send")
async def receive_data(data: useData, authorization: str = Header(default=None)):

    json_data = data.dict()
    print("Datos recibidos:\n" + json.dumps(json_data, indent=4))

    headers = {}
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        if is_token_valid(token):
            headers["Authorization"] = authorization
            print(f"Authorization header enviada: {authorization}")
        else:
            print("Token inválido o expirado, no se envía cabecera Authorization")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(settings.FORWARD_URL, json=json_data, headers=headers)

        try:
            forwarded_response = response.json()
        except json.JSONDecodeError:
            forwarded_response = {"raw_text": response.text}

        print("Respuesta del servidor externo:\n" + json.dumps(forwarded_response, indent=4) if isinstance(forwarded_response, dict) else str(forwarded_response))

        return {
            "message": "Datos de la encuesta recibidos y reenviados correctamente",
            "status_code": response.status_code,
            "forwarded_response": forwarded_response,
        }

    except httpx.RequestError as exc:
        print(f"Error al reenviar los datos: {str(exc)}")
        return {
            "message": "Error al reenviar los datos",
            "error": str(exc)
        }
