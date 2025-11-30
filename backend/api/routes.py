# backend-python/api/routes.py
from fastapi import APIRouter
from .controllers import get_simulation, get_artery_simulation

router = APIRouter()

@router.get("/simulation")
def simulation_endpoint():
    """
    First simulation (dimensionless PDE) for Three.js frontend.
    """
    return get_simulation()

@router.get("/artery-sim")
def artery_simulation_endpoint():
    """
    Second simulation (artery + Windkessel) for Plotly dashboard.
    """
    return get_artery_simulation()
