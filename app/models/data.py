from pydantic import BaseModel
from typing import Dict
from datetime import datetime

class useData(BaseModel):
    date: str = datetime.now().isoformat()
    energy: Dict[str, int]
    food: Dict[str, int]
    transport: Dict[str, int]
    waste: Dict[str, int]
