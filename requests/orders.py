from typing import List

from pydantic import BaseModel, Field

from commons.constants import ORDER_CRITERION
from models.orders import OrderCreated

criterion_values: str = "|".join(str(criterion) for criterion in ORDER_CRITERION)
allowed_criterion_regex: str = f"^({criterion_values})"


class RequestProcessOrders(BaseModel):
    orders: List[OrderCreated] = Field(..., title="List of orders.")
    criterion: str = Field(
        ...,
        title=f"Criterion to process orders. Allowed values: {criterion_values}",
        pattern=allowed_criterion_regex,
    )
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "orders": [
                        {
                            "id": 1,
                            "item": "Laptop",
                            "quantity": 2,
                            "price": 1.5,
                            "status": "pending",
                        },
                        {
                            "id": 2,
                            "item": "Mouse",
                            "quantity": 3,
                            "price": 2.5,
                            "status": "completed",
                        },
                        {
                            "id": 3,
                            "item": "Laptop",
                            "quantity": 1,
                            "price": 2.5,
                            "status": "completed",
                        },
                    ],
                    "criterion": "completed",
                }
            ]
        }
    }
