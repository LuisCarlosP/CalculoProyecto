from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router
from app.infrastructure.logging_config import configure_logging

configure_logging()

app = FastAPI(
    title="Lagrange Interpolation - Derivative Calculator",
    description="Numerical differentiation using Lagrange interpolation polynomials",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
