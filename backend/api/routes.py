from fastapi import APIRouter, HTTPException
from .controllers import run_simulation_by_name, list_simulations, run_simulation_raw

router = APIRouter()

@router.get("/simulations")
def get_simulation_list():
    return list_simulations()

@router.get("/simulation/{name}")
def get_simulation(
    name: str,
    T_FINAL: float | None = None,
    A0: float | None = None,
    Q0: float | None = None,
):
    try:
        return run_simulation_by_name(
            name,
            T_FINAL=T_FINAL,
            A0=A0,
            Q0=Q0,
        )
    except KeyError:
        raise HTTPException(status_code=404, detail="Simulation not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/simulation-raw/{name}")
def get_simulation_raw(name: str):
    try:
        return run_simulation_raw(name)
    except KeyError:
        raise HTTPException(status_code=404, detail="Simulation not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
