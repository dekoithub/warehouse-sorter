from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RouteCreate(BaseModel):
    barcode: str = Field(min_length=1)
    destination_code: int = Field(gt=0)


class RouteActiveUpdate(BaseModel):
    is_active: bool


class RouteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    barcode: str
    destination_id: int
    is_active: bool
    created_at: datetime
