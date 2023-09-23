from pydantic import BaseModel, Field

from commons.constants import ALLOWED_ITEMS, ORDER_CRITERION

allowed_items_regex: str = f"^({'|'.join(str(item) for item in ALLOWED_ITEMS)})"
allowed_criterion_regex: str = (
    f"^({'|'.join(str(status) for status in ORDER_CRITERION)})"
)


class OrderBase(BaseModel):
    item: str = Field(..., title="Item name.", pattern=allowed_items_regex)
    quantity: int = Field(..., title="How many items.", gt=0)
    price: float = Field(..., title="Item price.", gt=0.0)
    status: str = Field(..., title="Order status.", pattern=allowed_criterion_regex)


class OrderToCreate(OrderBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "item": "Laptop",
                    "quantity": 2,
                    "price": 1.5,
                    "status": "pending",
                }
            ]
        }
    }


class OrderCreated(OrderBase):
    id: int = Field(..., title="Order id.", ge=0)
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "item": "Laptop",
                    "quantity": 2,
                    "price": 1.5,
                    "status": "pending",
                }
            ]
        }
    }
