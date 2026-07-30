from pydantic import BaseModel, Field
from typing import List, Optional


class PointDTO(BaseModel):
    x: float
    y: float


class EvaluateRequest(BaseModel):
    func: str = Field(..., description="Function name: x3, sin, exp, ln, cos, sqrt, invsq")
    points_type: str = Field("equispaced", description="equispaced or custom")
    a: float = Field(0.0, description="Left bound")
    b: float = Field(1.0, description="Right bound")
    n: int = Field(5, description="Number of points", ge=2, le=200)
    x_eval: float = Field(0.5, description="Point where derivative is evaluated")
    custom_points: Optional[List[PointDTO]] = Field(None, description="Custom points if points_type=custom")


class StepsRequest(BaseModel):
    points: List[PointDTO] = Field(..., description="Custom points table", min_length=2)
    x_eval: float = Field(..., description="Point where derivative is evaluated")


class BasisStep(BaseModel):
    i: int
    basis_term: str
    basis_simplified: str
    contribution: str


class StepsResponse(BaseModel):
    points: List[PointDTO]
    steps: List[BasisStep]
    polynomial: str
    derivative: str
    evaluated: float
    x_eval: float


class EvaluateResponse(BaseModel):
    x_eval: float
    interpolated_value: float
    derivative_approx: float
    derivative_exact: Optional[float]
    absolute_error: Optional[float]
    relative_error: Optional[float]
    execution_time: float
    num_points: int


class ExperimentRequest(BaseModel):
    func: str = Field(..., description="Function name")
    a: float = Field(0.0)
    b: float = Field(1.0)
    x_eval: float = Field(0.5)
    n_values: List[int] = Field(default_factory=lambda: [2, 3, 4, 5, 10, 15, 20, 30, 50, 100])
    plot_n: Optional[int] = Field(None, description="Number of points for the function plot (uses user's n)")


class ExperimentResultDTO(BaseModel):
    n: int
    result: float
    exact_value: Optional[float]
    absolute_error: Optional[float]
    relative_error: Optional[float]
    execution_time: float
    iterations: int


class FunctionPlotPoint(BaseModel):
    x: float
    f_x: float
    p_x: float


class ExperimentResponse(BaseModel):
    function_name: str
    a: float
    b: float
    x_eval: float
    results: List[ExperimentResultDTO]
    function_plot_data: List[FunctionPlotPoint]
    interpolation_points: List[PointDTO]


class FunctionInfo(BaseModel):
    name: str
    expression: str
    label: str


class FunctionsListResponse(BaseModel):
    functions: List[FunctionInfo]
