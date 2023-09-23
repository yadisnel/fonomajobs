import os

from fastapi import FastAPI

from routers.v1.orders import router as orders_router_v1

commit_hash = os.environ.get("COMMIT_HASH")
if not commit_hash:
    commit_hash = "local"


app = FastAPI(
    title="FONOMA JOBS API",
    version=f"1.0 build: {commit_hash}",
)

app_v1 = FastAPI(
    title="FONOMA JOBS API",
    version=f"1.0 build: {commit_hash}",
)

app_v1.include_router(orders_router_v1, tags=["orders"])

app.mount("/v1", app_v1)


@app.get("/")
async def root_info():
    return {"1": "Please check the documentation at v1/docs."}


@app.get("/health")
async def health():
    return {"message": "ok."}
