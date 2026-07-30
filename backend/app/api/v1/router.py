from fastapi import APIRouter
from CalculoProyecto.backend.app.api.v1.endpoints import lagrange

router = APIRouter(prefix="/api/v1")
router.include_router(lagrange.router)
