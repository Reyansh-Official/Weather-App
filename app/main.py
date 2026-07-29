from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import weather
from app.core.config import CORS_ORIGINS


app = FastAPI(title="My Weather Monitoring App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(weather.router)

@app.get("/")
def home():
    return {"status": "online"}



