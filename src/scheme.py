from pydantic import BaseModel
from datetime import datetime

class RollScheme(BaseModel):
    id_from: int | None = None
    id_to: int | None = None
    length_from: int | None = None
    length_to: int | None = None
    weight_from: int | None = None
    weight_to: int | None = None
    created_at: datetime | None = None
    deleted_at: datetime | None = None