# backend-python/api/server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router as main_router

app = FastAPI(title="Blood Flow Simulation API")

# Allow frontend (localhost:3000) to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)
