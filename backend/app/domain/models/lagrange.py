from dataclasses import dataclass, field
from typing import Callable, List, Optional, Tuple


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass
class LagrangeResult:
    x_eval: float
    interpolated_value: float
    derivative_approx: float
    derivative_exact: float
    absolute_error: float
    relative_error: float
    execution_time: float
    num_points: int


@dataclass
class ExperimentResult:
    n: int
    result: float
    exact_value: float
    absolute_error: float
    relative_error: float
    execution_time: float
    iterations: int


@dataclass
class ExperimentReport:
    function_name: str
    a: float
    b: float
    x_eval: float
    results: List[ExperimentResult] = field(default_factory=list)
    plot_data: List[Tuple[float, float, float]] = field(default_factory=list)
    interpolation_points: List[Point] = field(default_factory=list)


@dataclass
class EvaluatedFunction:
    name: str
    expression: str
    func: Optional[Callable[[float], float]]
    derivative: Optional[Callable[[float], float]]
