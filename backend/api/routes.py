from fastapi import APIRouter, HTTPException
from .controllers import run_simulation_by_name, list_simulations

router = APIRouter()

@router.get("/simulations")
def get_simulation_list():
    return list_simulations()

@router.get("/simulation/{name}")
def get_simulation(name: str):
    try:
        return run_simulation_by_name(name)
    except KeyError:
        raise HTTPException(status_code=404, detail="Simulation not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
