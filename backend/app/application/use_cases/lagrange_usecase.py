import math
import time
from typing import Callable, Dict, List, Optional, Tuple

from CalculoProyecto.backend.app.application.dto.lagrange_dto import (
    BasisStep,
    EvaluateRequest,
    EvaluateResponse,
    ExperimentRequest,
    ExperimentResponse,
    ExperimentResultDTO,
    FunctionInfo,
    FunctionPlotPoint,
    PointDTO,
    StepsRequest,
    StepsResponse,
)
from CalculoProyecto.backend.app.domain.models.lagrange import EvaluatedFunction, Point
from CalculoProyecto.backend.app.domain.services.lagrange_service import (
    compute_polynomial_coeffs,
    differentiate_poly,
    evaluate_derivative,
    expand_lagrange_basis_coeffs,
    format_polynomial,
    generate_equispaced_points,
    lagrange_derivative,
    lagrange_interpolate,
    run_experiment,
)


DOMAIN_RESTRICTIONS = {
    "ln": {"min_x": 0.0, "exclusive_min": True},
    "sqrt": {"min_x": 0.0, "exclusive_min": False},
}


def validate_domain(name: str, value: float):
    if name in DOMAIN_RESTRICTIONS:
        r = DOMAIN_RESTRICTIONS[name]
        if r.get("exclusive_min", False):
            if value <= r["min_x"]:
                raise ValueError(f"{name}(x) requires x > {r['min_x']}, got {value}")
        else:
            if value < r["min_x"]:
                raise ValueError(f"{name}(x) requires x >= {r['min_x']}, got {value}")


def _safe_ln(x: float) -> float:
    if x <= 0:
        raise ValueError(f"ln(x) requires x > 0, got {x}")
    return math.log(x)


def _safe_ln_deriv(x: float) -> float:
    if x <= 0:
        raise ValueError(f"ln'(x) requires x > 0, got {x}")
    return 1.0 / x


def _safe_sqrt(x: float) -> float:
    if x < 0:
        raise ValueError(f"sqrt(x) requires x >= 0, got {x}")
    return math.sqrt(x)


def _safe_sqrt_deriv(x: float) -> float:
    if x <= 0:
        raise ValueError(f"sqrt'(x) requires x > 0, got {x}")
    return 1.0 / (2.0 * math.sqrt(x))


def _get_function(name: str) -> EvaluatedFunction:
    registry: Dict[str, Tuple[str, Optional[Callable[[float], float]], Optional[Callable[[float], float]]]] = {
        "x3": (
            "f(x) = x^3",
            lambda x: x ** 3,
            lambda x: 3 * x ** 2,
        ),
        "sin": (
            "f(x) = sin(x)",
            lambda x: math.sin(x),
            lambda x: math.cos(x),
        ),
        "exp": (
            "f(x) = e^x",
            lambda x: math.exp(x),
            lambda x: math.exp(x),
        ),
        "ln": (
            "f(x) = ln(x)",
            _safe_ln,
            _safe_ln_deriv,
        ),
        "cos": (
            "f(x) = cos(x)",
            lambda x: math.cos(x),
            lambda x: -math.sin(x),
        ),
        "sqrt": (
            "f(x) = sqrt(x)",
            _safe_sqrt,
            _safe_sqrt_deriv,
        ),
        "invsq": (
            "f(x) = 1/(1+x^2)",
            lambda x: 1.0 / (1.0 + x ** 2),
            lambda x: -2.0 * x / ((1.0 + x ** 2) ** 2),
        ),
        "none": (
            "Ninguna (puntos arbitrarios)",
            None,
            None,
        ),
    }
    if name not in registry:
        raise ValueError(f"Unknown function '{name}'. Available: {list(registry.keys())}")
    expr, f, df = registry[name]
    return EvaluatedFunction(name=name, expression=expr, func=f, derivative=df)


def get_available_functions() -> List[FunctionInfo]:
    names = ["none", "x3", "sin", "exp", "ln", "cos", "sqrt", "invsq"]
    return [
        FunctionInfo(name=name, expression=_get_function(name).expression, label=name)
        for name in names
    ]


def _validate_points(points: List[Point]):
    xs = [p.x for p in points]
    if len(xs) != len(set(xs)):
        raise ValueError("Duplicate x values found in custom points")


def _validate_bounds(ef: EvaluatedFunction, a: float, b: float):
    validate_domain(ef.name, a)
    validate_domain(ef.name, b)


def evaluate(request: EvaluateRequest) -> EvaluateResponse:
    ef = _get_function(request.func)
    is_none = ef.func is None or ef.derivative is None

    if is_none and request.points_type == "equispaced":
        raise ValueError("Cannot use equispaced points without a function. Select a function or use custom points.")

    if request.points_type == "equispaced":
        _validate_bounds(ef, request.a, request.b)
        points = generate_equispaced_points(ef.func, request.a, request.b, request.n)
    else:
        if not request.custom_points or len(request.custom_points) < 2:
            raise ValueError("Must provide at least 2 custom points")
        points = [Point(x=p.x, y=p.y) for p in request.custom_points]
        _validate_points(points)

    if not is_none:
        validate_domain(ef.name, request.x_eval)

    start = time.perf_counter()
    approx = lagrange_derivative(request.x_eval, points)
    elapsed = time.perf_counter() - start

    if is_none:
        return EvaluateResponse(
            x_eval=request.x_eval,
            interpolated_value=lagrange_interpolate(request.x_eval, points),
            derivative_approx=approx,
            derivative_exact=None,
            absolute_error=None,
            relative_error=None,
            execution_time=elapsed,
            num_points=len(points),
        )

    result = evaluate_derivative(ef.func, ef.derivative, points, request.x_eval)

    return EvaluateResponse(
        x_eval=result.x_eval,
        interpolated_value=result.interpolated_value,
        derivative_approx=result.derivative_approx,
        derivative_exact=result.derivative_exact,
        absolute_error=result.absolute_error,
        relative_error=None if math.isinf(result.relative_error) else result.relative_error,
        execution_time=result.execution_time,
        num_points=result.num_points,
    )


def experiment(request: ExperimentRequest) -> ExperimentResponse:
    ef = _get_function(request.func)
    _validate_bounds(ef, request.a, request.b)
    validate_domain(ef.name, request.x_eval)

    report = run_experiment(
        ef.func,
        ef.derivative,
        request.a,
        request.b,
        request.n_values,
        request.x_eval,
        function_name=ef.expression,
        plot_n=request.plot_n,
    )

    return ExperimentResponse(
        function_name=report.function_name,
        a=report.a,
        b=report.b,
        x_eval=report.x_eval,
        results=[
            ExperimentResultDTO(
                n=r.n,
                result=r.result,
                exact_value=r.exact_value,
                absolute_error=r.absolute_error,
                relative_error=None if math.isinf(r.relative_error) else r.relative_error,
                execution_time=r.execution_time,
                iterations=r.iterations,
            )
            for r in report.results
        ],
        function_plot_data=[
            FunctionPlotPoint(x=x, f_x=f, p_x=p)
            for x, f, p in report.plot_data
        ],
        interpolation_points=[
            PointDTO(x=p.x, y=p.y)
            for p in report.interpolation_points
        ],
    )


def compute_steps(request: StepsRequest) -> StepsResponse:
    points = [Point(x=p.x, y=p.y) for p in request.points]
    _validate_points(points)

    n = len(points)
    coeffs = compute_polynomial_coeffs(points)
    deriv_coeffs = differentiate_poly(coeffs)
    evaluated = lagrange_derivative(request.x_eval, points)

    steps = []
    for i in range(n):
        xi = points[i].x
        yi = points[i].y
        terms = []
        contrib_terms = []
        for j in range(n):
            if j != i:
                xj = points[j].x
                num = f"(x - {xj})" if xj >= 0 else f"(x + {-xj})"
                den = f"({xi} - {xj})" if xi - xj >= 0 else f"({xi} - {xj})"
                den_formatted = f"({xi} - {xj})"
                terms.append(f"{num}/{den_formatted}")
                prod = f"(x - {xj})"
                contrib_terms.append(prod)

        basis_str = " * ".join(terms)
        contrib_str = f"L{i}(x) = " + " * ".join(contrib_terms)

        L_i_coeffs = expand_lagrange_basis_coeffs(i, points)
        L_i_str = format_polynomial(L_i_coeffs, var="x")
        contribution_str = f"y{i} * L{i}(x) = {yi} * ({L_i_str})"

        steps.append(
            BasisStep(
                i=i,
                basis_term=f"L{i}(x) = {basis_str}",
                basis_simplified=f"L{i}(x) = {L_i_str}",
                contribution=contribution_str,
            )
        )

    poly_str = format_polynomial(coeffs, var="x")
    deriv_str = format_polynomial(deriv_coeffs, var="x")

    return StepsResponse(
        points=request.points,
        steps=steps,
        polynomial=f"P(x) = {poly_str}",
        derivative=f"P'(x) = {deriv_str}",
        evaluated=evaluated,
        x_eval=request.x_eval,
    )
