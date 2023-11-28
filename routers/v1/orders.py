import logging

from fastapi import APIRouter, Body, HTTPException, Request
from starlette.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                              HTTP_412_PRECONDITION_FAILED)

from commons.cripto_manager import CriptoManager
from commons.redis_manager import RedisManager
from controllers.orders import OrdersController
from requests.orders import RequestProcessOrders
from responses.orders import ResponseProcessOrders

router = APIRouter()


@router.post("/solution", response_model=ResponseProcessOrders, status_code=HTTP_200_OK)
async def process_orders(
    request: Request,
    body: RequestProcessOrders = Body(
        ...,
        title="Process orders body.",
    ),
):
    if not body.orders:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Orders list is empty.",
        )
    criterion_set = {order.status for order in body.orders}
    criterion_set.add("all")
    if body.criterion not in criterion_set:
        raise HTTPException(
            status_code=HTTP_412_PRECONDITION_FAILED,
            detail=f"Criterion '{body.criterion}' is not present in orders request.",
        )

    redis_manager = RedisManager()
    query_crc = CriptoManager().compute_crc(data=await request.body())
    if redis_manager.enabled():
        total = redis_manager.get(key=query_crc)
        if total is not None:
            total = float(total)
            logging.info(f"Redis hit for query: {query_crc}. Total: {total}")
            return ResponseProcessOrders(
                total=total,
            )
    total = OrdersController().process_orders(
        orders=body.orders,
        criterion=body.criterion,
    )
    if redis_manager.enabled():
        logging.info(f"Redis set for query: {query_crc}")
        redis_manager.set(key=query_crc, value=total)

    return ResponseProcessOrders(
        total=total,
    )
