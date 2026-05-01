from pydantic import BaseModel, ConfigDict
import uuid


class ResponsePlaces(BaseModel):
    id: uuid.UUID
    name: str
    city: str
    address: str

    model_config = ConfigDict(from_attributes=True)
