from pydantic import BaseModel, Field


class ResponseProcessOrders(BaseModel):
    total: float = Field(..., title="Total amount of money.", gt=0.0)
    model_config = {"json_schema_extra": {"examples": [{"total": 10.0}]}}
