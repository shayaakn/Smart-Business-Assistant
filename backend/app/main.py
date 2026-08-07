from fastapi import FastAPI
from app.core.logging import logger

app = FastAPI(
    title="Smart Business Assistant API",
    description="Production-quality AI-powered business assistant backend",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Smart Business Assistant API...")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include API routers
from app.api.customers import router as customers_router
app.include_router(customers_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)