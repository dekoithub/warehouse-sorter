from fastapi import FastAPI

from api.routers.destinations import router as destinations_router


app = FastAPI(
    title="Warehouse Sorter API",
    version="1.0.0",
)


app.include_router(destinations_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
    }