from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProcessingEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    item_id: int
    event_type: str
    location: str
    created_at: datetime
