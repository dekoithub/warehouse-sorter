from pydantic import BaseModel, ConfigDict, Field


class DestinationCreate(BaseModel):
    code: int = Field(gt=0)
    name: str = Field(min_length=1)


class DestinationActiveUpdate(BaseModel):
    is_active: bool


class DestinationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: int
    name: str
    is_active: bool