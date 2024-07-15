from fastapi import FastAPI
from api.v1.endpoints import router as api_router
from models.pokemon import Base
from db.session import engine
from fastapi.middleware.cors import CORSMiddleware

# Create the FastAPI instance
app = FastAPI()

# Add the middleware to allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the tables in the database
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Drop the tables in the database
@app.on_event("shutdown")
async def shutdown_event():
    await engine.dispose()

# Include the API router
app.include_router(api_router, prefix="/api/v1")

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)