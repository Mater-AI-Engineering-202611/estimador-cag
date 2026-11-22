from fastapi import FastAPI
from app.routers.estimations import router as estimations_router

app = FastAPI(
    title="Estimador CAG",
    description="API para estimaciones de software mediante IA",
    version="1.0.0"
)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(estimations_router)
