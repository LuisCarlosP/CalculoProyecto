from fastapi import APIRouter, HTTPException
from app.application.dto.lagrange_dto import (
    EvaluateRequest,
    EvaluateResponse,
    ExperimentRequest,
    ExperimentResponse,
    FunctionsListResponse,
    StepsRequest,
    StepsResponse,
)
from app.application.use_cases import lagrange_usecase

router = APIRouter(prefix="/lagrange", tags=["Lagrange Interpolation"])


@router.get("/functions", response_model=FunctionsListResponse)
def list_functions():
    functions = lagrange_usecase.get_available_functions()
    return FunctionsListResponse(functions=functions)


@router.post("/evaluate", response_model=EvaluateResponse)
def evaluate_derivative_endpoint(request: EvaluateRequest):
    try:
        return lagrange_usecase.evaluate(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/experiment", response_model=ExperimentResponse)
def run_experiment_endpoint(request: ExperimentRequest):
    try:
        return lagrange_usecase.experiment(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/steps", response_model=StepsResponse)
def compute_steps_endpoint(request: StepsRequest):
    try:
        return lagrange_usecase.compute_steps(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ZeroDivisionError as e:
        raise HTTPException(status_code=400, detail="Division by zero - check for duplicate x values")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
