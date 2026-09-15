from pydantic import BaseModel, ConfigDict


class DestinationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: int
    name: str
    is_active: bool