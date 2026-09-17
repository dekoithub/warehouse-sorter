from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ItemStatus = Literal[
    "CREATED",
    "SCANNING",
    "ROUTING",
    "MOVING",
    "BUFFERED",
    "SORTED",
    "MANUAL_PROCESSING",
    "ERROR",
]


class ItemCreate(BaseModel):
    barcode: str = Field(min_length=1)
    weight: Decimal = Field(gt=0)
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    length: int = Field(gt=0)
    category: str = Field(min_length=1)
    delivery_type: str = Field(min_length=1)
    status: ItemStatus = "CREATED"
    location: str = Field(min_length=1)
    destination_code: int | None = Field(default=None, gt=0)


class ItemStateUpdate(BaseModel):
    status: ItemStatus
    location: str = Field(min_length=1)


class ItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    barcode: str
    weight: Decimal
    width: int
    height: int
    length: int
    category: str
    delivery_type: str
    is_flammable: bool
    status: str
    destination_id: int | None
    location: str
    created_at: datetime
